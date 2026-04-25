# 🎓 FaceID Pro: AI Student Roll Number Assistant

A sophisticated, AI-driven solution for automated student recognition and photo organization. This system eliminates manual sorting of graduation photos by using advanced facial recognition to match students with their official roll numbers.

---

## 🛠️ Complete Application Flow

To achieve a 100% success rate, follow this exact workflow:

### 1. Preparation of Reference Photos
The AI needs to know who the students are.
*   **Action:** Take one clear photo of each student.
*   **Naming:** Save the file using the **Student's Roll Number** (e.g., `101.jpg`, `102.png`, `CS05.jpg`).
*   **Format:** Place all these photos inside a single folder (e.g., `Students_Database`).

### 2. Preparation of Ceremony Photos
These are the raw photos taken during graduation.
*   **Action:** Keep these in their original format (e.g., `IMG_001.jpg`, `DSC_123.jpg`).
*   **Format:** Place all these photos inside another folder (e.g., `Graduation_2024`).

### 3. Launching the Dashboard
*   Run the application (`python app.py`).
*   Open **`http://localhost:5000`** in your browser.
*   Choose your preferred visual mode (Dark or Light) using the toggle in the top right.

### 4. Uploading Resources
*   **Reference Upload:** Click on **"Choose Folder"** under the **Reference Photos** card. Select your `Students_Database` folder.
*   **Graduation Upload:** Click on **"Choose Folder"** under the **Graduation Photos** card. Select your `Graduation_2024` folder.

### 5. AI Processing (Matching)
*   Click the **"Start Recognition"** button.
*   **What happens internally:**
    1.  **Scanning:** The AI detects faces in every reference photo and creates a "Digital Face Map" (Embedding).
    2.  **Comparison:** The AI scans every graduation photo (including group photos).
    3.  **Matching:** If a face in a graduation photo matches a student map by more than **60%**, a match is confirmed.
    4.  **Auto-Rename:** The graduation photo is copied and renamed to `[RollNumber]_[Count].jpg`.

### 6. Review and Search
*   Watch the **Live Engine Logs** to see matches happening in real-time.
*   Use the **Quick Search** bar to find all photos belonging to a specific roll number.
*   Click the **Eye Icon** in the results table to see a pop-up gallery of that student's matched photos.

### 7. Final Results
*   Open the `output/` folder located in the project directory.
*   You will find neatly organized folders for every student containing their specific graduation photos.
*   Check the `output/assignment_report.csv` for a spreadsheet version of all matches.

---

## 🧪 Requirements for Success
| Requirement | Detail |
| :--- | :--- |
| **Python Version** | 3.8 to 3.13 (Supported) |
| **Reference Photo** | Front-facing, clear lighting, only 1 person in frame. |
| **Graduation Photo** | Can have multiple people; AI will match each face individually. |
| **Accuracy** | Matches are based on high-precision 128D facial embeddings. |

---

## 🚀 Installation & Running

1.  **Clone/Download** this project folder.
2.  **Open Terminal/CMD** in this folder.
3.  **Install Requirements:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Start App:**
    ```bash
    python app.py
    ```
5.  **Visit:** `http://localhost:5000`

---
*Created with ❤️ for college administrators and photographers.*
