try:
    import pkg_resources
    print("pkg_resources found")
    try:
        path = pkg_resources.resource_filename('face_recognition_models', 'models')
        print(f"Path found: {path}")
    except Exception as e:
        print(f"Path error: {e}")
except ImportError:
    print("pkg_resources NOT found")

import face_recognition
print("face_recognition imported successfully")
