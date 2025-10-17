# 🧠 Code Review Assistant

## 📋 Overview

**Code Review Assistant** is an AI-powered tool that automates the process of reviewing source code.
It helps developers quickly analyze their code’s **readability, modularity, and potential bugs** using an integrated **LLM (Google Gemini)**.

This project demonstrates how a lightweight backend API can take in source files, process them through an AI model, and return structured review feedback.

---

## 🎯 Objectives

* Automate manual code review steps.
* Identify areas of improvement in code structure and quality.
* Provide actionable feedback on readability, modularity, and potential issues.
* Offer a simple and intuitive web interface for file uploads and report viewing.

---

## ⚙️ Features to be Included

### 1. **Core Functionality**

* Upload source code files (`.py`, `.js`, `.cpp`, `.java`, etc.)
* Backend API processes the file and sends it to the **Gemini AI model**.
* The model returns structured feedback as a JSON object with:

  * ✅ **Summary** – What the code does
  * 📖 **Readability** – Naming conventions, comments, formatting
  * 🧩 **Modularity** – Function/class structure and code organization
  * 🐞 **Potential Bugs** – Likely errors or edge cases
  * 💡 **Suggestions** – Actionable steps to improve the code

---

### 2. **Backend (FastAPI)**

* Built with **FastAPI** for quick API development.
* Integrates **Google Gemini API** for analysis.
* Includes endpoints:

  * `POST /review` — accepts a file and returns the review report.
* Handles errors gracefully (invalid file, decoding issues, oversized uploads).

---

### 3. **Frontend (Optional Dashboard)**

* A simple **HTML/JS interface** to upload files.
* Displays the formatted AI-generated review.
* Can later be expanded into a more interactive dashboard with:

  * Review history
  * Downloadable reports
  * Syntax-highlighted code previews

---

### 4. **Optional Extensions (Future Scope)**

* Store past review reports in a local **SQLite database**.
* Add **user authentication** for personalized dashboards.
* Enable **language-specific checks** (Python, Java, C++).
* Visual indicators for severity (e.g., 🟢 minor, 🔴 major).
* Export reviews as PDF or Markdown reports.

---

## 🧩 Tech Stack

| Layer                     | Technology                            |
| ------------------------- | ------------------------------------- |
| **Backend**               | FastAPI (Python)                      |
| **AI Model**              | Google Gemini 1.5 Flash               |
| **Frontend**              | HTML, CSS, JavaScript                 |
| **Environment**           | Python-dotenv for secrets             |
| **Deployment (optional)** | Render / Vercel / Hugging Face Spaces |

---

## 📦 Input / Output

**Input:**
Source code file uploaded via the `/review` endpoint.

**Output:**
Structured JSON review like:

```json
{
  "summary": "The code implements a basic Flask API for handling user logins.",
  "readability": "- Variable naming is inconsistent.\n- Missing docstrings.",
  "modularity": "Single-file structure; could separate routes and models.",
  "potential_bugs": "No validation on user inputs.",
  "suggestions": "Add input sanitization and comments for each function."
}
```


