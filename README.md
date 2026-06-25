# ResumeParser - Premium Applicant Tracking System

A premium Flask-based resume parsing dashboard that extracts candidate names, contact details, skills, education, and work experience from PDF and DOCX files. Built with Python, spaCy, SQLAlchemy (SQLite), and a modern glassmorphism frontend interface.

## ⚠️ Why are you seeing a "404 File Not Found" on GitHub Pages?

GitHub Pages is designed **exclusively for hosting static websites** (pure HTML, CSS, and client-side JavaScript). 

Because **ResumeParser is a dynamic backend application** written in Python (Flask) and requires a server-side runtime and SQLite database:
1. GitHub Pages cannot run the Python backend code (`app.py`).
2. GitHub Pages attempts to locate a static `index.html` file in the root folder, which does not exist (the dashboard is dynamically served via Flask templates).
3. As a result, accessing the GitHub Pages URL leads directly to a **404 File Not Found** error page.

To run this application, you must either **run it locally** or deploy it to a backend-compatible cloud platform (like Render, Railway, or Heroku).

---

## 💻 Local Setup & Execution

Follow these steps to run the application on your computer:

### 1. Prerequisites
- **Python 3.8 or higher** installed on your system.
- Git (optional, for cloning).

### 2. Set Up Virtual Environment (Recommended)
Open your terminal/command prompt in the project root directory and run:

```bash
# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies
Install all the required Python packages:

```bash
pip install -r requirements.txt
```

*Note: This will install Flask, spaCy, pdfplumber, python-docx, SQLAlchemy, and other helpers.*

### 4. Download NLP Language Model
Download the English language model used by spaCy for named entity recognition (NER):

```bash
python -m spacy download en_core_web_sm
```

### 5. Configure Environment Variables (Optional)
The project comes with a `.env` configuration. You can check or customize settings such as database file, upload folders, and secret keys there.

### 6. Run the Application
Start the Flask development server:

```bash
python app.py
```

Open your browser and navigate to:
👉 **[http://127.0.0.1:5000](http://127.0.0.1:5000)**

---

## 🚀 How to Deploy to the Cloud

To host this project online, use a platform that supports **Python/Flask backends** and **databases**. 

### Recommended Platforms:
- **[Render](https://render.com/)** (Free/Hobby tier available)
- **[Railway](https://railway.app/)**
- **[Heroku](https://www.heroku.com/)**

### Deployment Steps (e.g., Render):
1. **Add Gunicorn**: Install `gunicorn` (production WSGI server) by adding it to your `requirements.txt`:
   ```text
   gunicorn>=21.0.0
   ```
2. **Create a Web Service**: Link your GitHub repository (`Poojitha-Jinkala/project1`) to Render.
3. **Configure Settings**:
   - **Environment**: `Python`
   - **Build Command**: `pip install -r requirements.txt && python -m spacy download en_core_web_sm`
   - **Start Command**: `gunicorn app:app`
4. **Environment Variables**: Add your custom env variables (like `SECRET_KEY`) under the settings page.

---

## 🛠️ Project Structure

- `app.py`: Main Flask application handling routing, upload handlers, and database records.
- `parser.py`: The extraction engine using regex and spaCy to parse name, contact details, skills, and histories.
- `models.py`: Database models defining Candidates, Skills, Education, and Work Experience.
- `verify_parser.py`: Verification tests for checking if the extraction logic functions correctly.
- `templates/`: HTML structures using Jinja2 templates (dashboard, details, uploads).
- `static/`: Custom CSS (`styles.css` with a responsive glassmorphism theme) and client-side JavaScript (`main.js` for dynamic interactions).
