import os
import sys
import hashlib
import cv2
import face_recognition
import numpy as np
import shutil
import time
import threading
from flask import Flask, render_template, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
from concurrent.futures import ThreadPoolExecutor

# Monkey-patch pkg_resources for Python 3.13 compatibility
try:
    import pkg_resources
except ImportError:
    class MockPkgResources:
        @staticmethod
        def resource_filename(package, resource):
            import face_recognition_models
            return os.path.join(os.path.dirname(face_recognition_models.__file__), resource)
    sys.modules['pkg_resources'] = MockPkgResources()

app = Flask(__name__)

# CONFIGURATIONS
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FINAL_YEAR_DIR = os.path.join(BASE_DIR, 'final_year')
GRADUATION_DIR = os.path.join(BASE_DIR, 'graduation')
OUTPUT_DIR = os.path.join(BASE_DIR, 'output')
UNKNOWN_DIR = os.path.join(BASE_DIR, 'unknown')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

# Globals for caching and progress
cached_encodings = []
cached_roll_numbers = []
process_logs = []
is_processing = False
processed_hashes = set()
stats = {
    "total": 0,
    "matched": 0,
    "unknown": 0,
    "skipped": 0,
    "duplicates": 0,
    "time": 0,
    "status_text": "System Ready"
}

# Ensure directories exist
for folder in [FINAL_YEAR_DIR, GRADUATION_DIR, OUTPUT_DIR, UNKNOWN_DIR]:
    if not os.path.exists(folder):
        os.makedirs(folder)

def get_file_hash(filepath):
    """Generate MD5 hash for duplicate detection."""
    hash_md5 = hashlib.md5()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def log_message(msg, type="info"):
    global process_logs
    timestamp = time.strftime("%H:%M:%S")
    process_logs.append({"time": timestamp, "msg": msg, "type": type})

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload/<target>', methods=['POST'])
def upload_files(target):
    if 'files' not in request.files:
        return jsonify({"error": "No files found"}), 400
    
    files = request.files.getlist('files')
    save_dir = FINAL_YEAR_DIR if target == 'final_year' else GRADUATION_DIR
    
    count = 0
    for file in files:
        if file and allowed_file(file.filename):
            original_filename = os.path.basename(file.filename)
            filename = secure_filename(original_filename)
            file.save(os.path.join(save_dir, filename))
            count += 1
            
    return jsonify({"message": f"Uploaded {count} photos", "count": count}), 200

def load_and_encode_faces():
    """Load and cache faces from final_year folder."""
    global cached_encodings, cached_roll_numbers, stats
    cached_encodings = []
    cached_roll_numbers = []
    stats["status_text"] = "Loading Student Records..."
    log_message("Loading Student Records...", "info")
    
    files = [f for f in os.listdir(FINAL_YEAR_DIR) if allowed_file(f)]
    log_message(f"Initializing Neural Engine with {len(files)} reference records...", "warning")
    
    for filename in files:
        path = os.path.join(FINAL_YEAR_DIR, filename)
        try:
            image = face_recognition.load_image_file(path)
            encodings = face_recognition.face_encodings(image)
            if encodings:
                cached_encodings.append(encodings[0])
                cached_roll_numbers.append(os.path.splitext(filename)[0])
        except Exception as e:
            log_message(f"Failed to encode {filename}: {str(e)}", "danger")
    
    log_message(f"Success: {len(cached_roll_numbers)} neural signatures loaded.", "success")

def process_single_photo(filename, roll_counts, current_index, total_count):
    """Optimized processing with duplicate prevention and best-match logic."""
    global stats, processed_hashes
    path = os.path.join(GRADUATION_DIR, filename)
    
    try:
        # 1. Duplicate Detection (Bit-level hash)
        file_hash = get_file_hash(path)
        if file_hash in processed_hashes:
            log_message(f"Duplicate content detected: {filename}. Skipping...", "warning")
            stats["duplicates"] += 1
            stats["skipped"] += 1
            return
        
        # 2. Image Load & Optimization
        img = cv2.imread(path)
        if img is None: 
            log_message(f"Skipping corrupted file: {filename}", "danger")
            stats["skipped"] += 1
            return
        
        # Scaling for speed (1000px width maintains accuracy vs speed)
        height, width = img.shape[:2]
        target_width = 1000
        scale = target_width / width
        target_height = int(height * scale)
        small_img = cv2.resize(img, (target_width, target_height))
        rgb_small_img = cv2.cvtColor(small_img, cv2.COLOR_BGR2RGB)
        
        # Blur Detection (Laplacian variance)
        laplacian_var = cv2.Laplacian(small_img, cv2.CV_64F).var()
        is_blurry = laplacian_var < 100 # Threshold for "low quality"
        
        # 3. Neural Analysis
        # Use HOG for speed by default.
        face_locations = face_recognition.face_locations(rgb_small_img, model="hog")
        face_encodings = face_recognition.face_encodings(rgb_small_img, face_locations)
        
        found_any_match = False
        
        if not face_encodings:
            log_message(f"No faces identified in {filename} (Blurry: {is_blurry})", "info")
            stats["unknown"] += 1
            # REMOVED: shutil.move to UNKNOWN_DIR. Photos now stay in graduation folder for manual review.
            processed_hashes.add(file_hash)
            return

        for face_encoding in face_encodings:
            # Dynamic matching logic: Get distances to find BEST match
            face_distances = face_recognition.face_distance(cached_encodings, face_encoding)
            
            if len(face_distances) > 0:
                best_idx = np.argmin(face_distances)
                min_distance = face_distances[best_idx]
                
                # Dynamic Threshold: 0.50 is sweet spot, 0.45 is strict
                if min_distance < 0.52:
                    roll = cached_roll_numbers[best_idx]
                    acc_perc = round((1 - min_distance) * 100, 1)
                    
                    # Naming logic: Multiple photos of same student
                    count = roll_counts.get(roll, 0)
                    new_name = f"{roll}.jpg" if count == 0 else f"{roll}_{count}.jpg"
                    roll_counts[roll] = count + 1
                    
                    # 4. Final Output Handling
                    shutil.move(path, os.path.join(OUTPUT_DIR, new_name))
                    log_message(f"MATCH: {filename} -> Student {roll} ({acc_perc}% Confidence)", "success")
                    stats["matched"] += 1
                    found_any_match = True
                    break # Stop looking for other people in this photo for simplicity
        
        if not found_any_match:
            log_message(f"UNKNOWN: {filename} -> Staying in Graduation folder for manual review", "info")
            stats["unknown"] += 1
            # REMOVED: shutil.move to UNKNOWN_DIR.

        processed_hashes.add(file_hash)

    except Exception as e:
        log_message(f"System Error in {filename}: {str(e)}", "danger")

def process_batch():
    global is_processing, stats, process_logs, processed_hashes
    is_processing = True
    processed_hashes = set()
    stats = {"total": 0, "matched": 0, "unknown": 0, "skipped": 0, "duplicates": 0, "time": 0, "status_text": "Starting..."}
    process_logs = []
    
    start_time = time.time()
    
    # 1. Prepare References
    load_and_encode_faces()
    
    # 2. Scan Graduation Folder
    log_message("Scanning Dataset...", "info")
    grad_files = [f for f in os.listdir(GRADUATION_DIR) if allowed_file(f)]
    stats["total"] = len(grad_files)
    
    log_message(f"Found {len(grad_files)} event photos. Initializing matching threads...", "warning")
    stats["status_text"] = "Matching Faces..."
    log_message("Matching Faces...", "info")
    log_message("Neural analysis in progress. Monitor logs for real-time matches.", "warning")
    
    roll_counts = {}
    
    # 3. High Performance Multithreading
    with ThreadPoolExecutor(max_workers=4) as executor:
        for i, filename in enumerate(grad_files, 1):
            executor.submit(process_single_photo, filename, roll_counts, i, len(grad_files))

    duration = round(time.time() - start_time, 2)
    stats["time"] = f"{duration}s"
    stats["status_text"] = "Task Completed"
    log_message(f"BATCH COMPLETE: Processed {stats['total']} items in {stats['time']}.", "success")
    is_processing = False

@app.route('/start_processing', methods=['POST'])
def start_processing():
    global is_processing
    if is_processing:
        return jsonify({"error": "Already processing"}), 400
    
    thread = threading.Thread(target=process_batch)
    thread.start()
    return jsonify({"message": "Neural processing phase started"}), 200

@app.route('/status')
def get_status():
    return jsonify({
        "is_processing": is_processing,
        "logs": process_logs[-15:], 
        "stats": stats
    })

@app.route('/reset', methods=['POST'])
def reset():
    # File deletion disabled for safety: "i don't want to delete any photos automatically"
    # User will handle manual deletion in the file explorer.
    global process_logs, processed_hashes
    process_logs = []
    processed_hashes = set()
    return jsonify({"message": "Neural memory cleared. Files were NOT deleted."})

@app.route('/get_photo/<folder>/<filename>')
def get_photo(folder, filename):
    safe_folder = OUTPUT_DIR if folder == 'output' else UNKNOWN_DIR
    return send_from_directory(safe_folder, filename)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
