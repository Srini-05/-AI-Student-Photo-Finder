# 🚀 AI Student Photo Finder - Launch Guide (GitHub Copilot Edition)

Welcome to the **QuickID AI Engine** setup guide. This document is designed for users who want to run the application with zero technical configuration using **GitHub Copilot**.

---

## 📖 1. Project Overview
This tool uses Artificial Intelligence to identify students from bulk graduation photos by comparing them against reference records.

*   **Reference Input:** Folder containing student photos named by their Roll Numbers (e.g., `101.jpg`).
*   **Target Input:** Folder containing thousands of unsorted graduation event photos.
*   **The AI Process:** Scans each graduation photo, identifies faces, matches them against the reference list, and organizes them.
*   **The Result:** Matched photos are renamed and moved to the **Output** folder. Unmatched photos are safely moved to the **Unknown** folder.

---

## 📁 2. Project Structure
Your project folder contains the following essential files and directories:

```text
ai-photo-finder/
├── app.py                # The main application brain (Flask)
├── requirements.txt      # List of AI libraries needed
├── templates/            # Web interface files (HTML)
├── static/               # Design and icons (CSS/JS)
├── final_year/           # [FOLDER] Place student reference photos here
├── graduation/          # [FOLDER] Place graduation event photos here
├── output/              # [FOLDER] Matches will appear here
├── unknown/             # [FOLDER] Photos with no matches go here
└── RUN_PROJECT...md      # This guide
```

---

## 💻 3. System Requirements
Before starting, ensure your computer has:
1.  **VS Code:** [Download here](https://code.visualstudio.com/)
2.  **Python 3.10+:** [Download here](https://www.python.org/) (Check "Add Python to PATH" during install)
3.  **Extensions:** Install "Python" and "GitHub Copilot" extensions in VS Code.
4.  **Internet:** Required for the one-time installation of AI models.

---

## 🛠️ 4. How to Start (One-Click Experience)

Follow these 5 simple steps:

1.  Open **VS Code**.
2.  Drag and drop the **project folder** into VS Code.
3.  Open the **GitHub Copilot Chat** (Press `Ctrl + Shift + i` or click the chatbot icon on the left).
4.  Keep this file (`RUN_PROJECT_WITH_GITHUB_COPILOT.md`) open in a tab.
5.  In the Chatbox, type:
    > **Start the application**

---

## 🤖 5. What Copilot Will Do
Once you type the command, GitHub Copilot will automatically:
*   Verify if Python is installed correctly.
*   Create a **Virtual Environment (venv)** to keep your computer clean.
*   Install all required libraries from `requirements.txt`.
*   Handle complex installs like `dlib` or `face-recognition`.
*   Start the local server.
*   Provide a clickable link like `http://127.0.0.1:5000`.

---

## ⌨️ 6. Manual Commands Reference
If you prefer manual entry or Copilot asks you to run a command, use these:

| Action | Windows (PowerShell) | Mac / Linux (Terminal) |
| :--- | :--- | :--- |
| **Check Python** | `python --version` | `python3 --version` |
| **Create Environment** | `python -m venv venv` | `python3 -m venv venv` |
| **Activate Environment** | `.\venv\Scripts\activate` | `source venv/bin/activate` |
| **Install Libraries** | `pip install -r requirements.txt` | `pip3 install -r requirements.txt` |
| **Launch App** | `python app.py` | `python3 app.py` |

---

## ⚠️ 7. Automated Error Resolution
If something goes wrong, Copilot is trained to fix these automatically:

*   **"Module Not Found":** Copilot will detect which library is missing and run `pip install` again.
*   **"dlib install failed":** This is common on Windows. Copilot will suggest installing "C++ Build Tools" or downloading a pre-built wheel.
*   **"Port 5000 in use":** Copilot will find the process blocking the port and kill it or change the port to `5001`.
*   **"Python not found":** Copilot will guide you to add Python to your system environment variables.

---

## 🎨 8. Using the Application
Once the URL `http://127.0.0.1:5000` is active:

1.  **Open the link** in Chrome/Edge.
2.  **Upload Reference:** Select the `final_year` folder.
3.  **Upload Event Photos:** Select the `graduation` folder.
4.  **Click "Start Processing":** Watch the real-time logs confirm matches.
5.  **Retrieve Photos:** Check the `output` folder on your computer for organized results.

---

## 🎯 9. Final Prompt for Copilot Chat
If the application is not running yet, copy and paste this into Copilot Chat:

```text
Read this project structure and the RUN_PROJECT_WITH_GITHUB_COPILOT.md document. Install all requirements automatically, create a venv if needed, and fix any installation issues. Run the Flask application locally and continue until the localhost URL is working and accessible.
```

---

## 🛡️ 10. Document Integrity
*This document is a part of the AI Photo Finder Professional Suite. Do not delete this file as it serves as the instructional context for AI-assisted operations.*

**Version 1.0.0** | **© 2026 AI Solutions Lab**
