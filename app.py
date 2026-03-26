from flask import Flask, request, render_template, redirect, url_for, session, jsonify
from plagiarism_checker import check_plagiarism
from humanize_text import simple_humanize, estimate_humanization_improvement
import sqlite3
from datetime import datetime
import os
from werkzeug.utils import secure_filename
from PyPDF2 import PdfReader
import docx
import json

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Required for session handling

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'docx'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def extract_content(file_path, extension):
    try:
        if extension == 'txt':
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        elif extension == 'pdf':
            reader = PdfReader(file_path)
            return "\n".join([page.extract_text() or "" for page in reader.pages])
        elif extension == 'docx':
            doc = docx.Document(file_path)
            return "\n".join([para.text for para in doc.paragraphs])
    except Exception as e:
        print("Error extracting content:", e)
        return ""
    return ""

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    input_text = ""

    if request.method == 'POST':
        # File upload
        file = request.files.get('file')
        filename = "Pasted Text"

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_ext = filename.rsplit('.', 1)[1].lower()
            save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(save_path)
            input_text = extract_content(save_path, file_ext)
        else:
            # Fallback to pasted content
            input_text = request.form.get('content', '')

        if input_text.strip():  # Ensure content isn't blank
            result = check_plagiarism(input_text)
            
            # Store the content and result in session for later use
            session['current_content'] = input_text
            session['current_filename'] = filename
            session['current_result'] = result

        else:
            result = {'error': 'No valid content extracted from file or paste. Please try again.'}

    return render_template('index.html', result=result)

@app.route('/humanize', methods=['POST'])
def humanize():
    """Humanize the submitted content"""
    data = request.get_json()
    original_text = data.get('text', '')
    
    if not original_text:
        return jsonify({'error': 'No text provided'})
    
    humanized_text = simple_humanize(original_text)
    improvement = estimate_humanization_improvement(original_text, humanized_text)
    
    return jsonify({
        'original': original_text,
        'humanized': humanized_text,
        'improvement': improvement
    })

@app.route('/save', methods=['POST'])
def save():
    """Save the content to database"""
    content = session.get('current_content')
    filename = session.get('current_filename', 'Submission')
    
    if content:
        conn = sqlite3.connect('plagiarism.db')
        c = conn.cursor()
        c.execute("""INSERT INTO submissions (filename, content, timestamp) 
                     VALUES (?, ?, ?)""",
                  (filename, content, datetime.now()))
        conn.commit()
        conn.close()
        
        # Clear session data
        session.pop('current_content', None)
        session.pop('current_filename', None)
        session.pop('current_result', None)
        
        return render_template('index.html', message='✅ Content saved successfully to database!')
    
    return redirect(url_for('index'))

@app.route('/download', methods=['POST'])
def download_humanized():
    """Download humanized content"""
    data = request.get_json()
    humanized_text = data.get('text', '')
    
    # Store for download
    session['download_text'] = humanized_text
    
    return jsonify({'status': 'ready'})

if __name__ == '__main__':
    app.run()
