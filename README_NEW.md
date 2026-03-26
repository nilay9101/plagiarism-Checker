# Content Analyzer - Plagiarism & AI Detection Tool

A comprehensive application for detecting plagiarism and AI-generated content in any text or document. This smart system helps users identify plagiarism, detect AI-generated content, and humanize text with a user-friendly interface.

## Features

✨ **AI Detection** - Analyzes linguistic patterns to detect AI-generated content with percentage accuracy
🔍 **Plagiarism Detection** - Compares submitted content against a database of previous submissions
🤖 **Content Humanization** - Transforms AI-detected text into more human-like content
📄 **Multi-Format Support** - Accepts .txt, .pdf, and .docx files, plus direct text input
💾 **Database Storage** - Automatically stores submissions for future comparison
📊 **Detailed Analytics** - Shows AI percentage, plagiarism percentage, and matching sources

## How It Works

1. **Submit Content** - Upload a file or paste text directly into the interface
2. **Analysis** - The system analyzes your content for:
   - AI-generated content percentage (using linguistic markers)
   - Plagiarism percentage (by comparing against database submissions)
   - Similar matches from previous submissions
3. **Humanization** - If AI content is detected, you can humanize the text to make it more natural
4. **Save or Download** - Save content to database or download humanized versions

## Technical Details

### Technology Stack
- **Backend**: Python + Flask
- **Database**: SQLite
- **Analysis**: SequenceMatcher for plagiarism, TextStat for AI detection
- **Frontend**: Bootstrap 5 + Vanilla JavaScript

### AI Detection Method
The system uses multiple linguistic markers to detect AI-generated content:
- Flesch-Kincaid Grade Level (formal/academic writing)
- Average sentence length (AI tends to use longer sentences)
- Passive voice frequency (AI uses more passive constructions)
- Vocabulary diversity (AI has higher word uniqueness)

### Humanization Process
The humanization module:
- Replaces formal conjunctions with casual alternatives
- Breaks up overly long sentences
- Adds more natural language patterns
- Reduces passive voice usage

## Project Structure

```
Content-Analyzer/
├── app.py                    # Main Flask application
├── plagiarism_checker.py    # Plagiarism & AI detection logic
├── humanize_text.py         # Text humanization module
├── database.py              # Database initialization
├── requirements.txt         # Python dependencies
│
├── uploads/                 # Temporary uploaded files
├── assignments/             # Sample/baseline texts
│
├── templates/
│   └── index.html          # Main UI interface
├── static/
│   └── styles.css          # Custom styling
└── plagiarism.db           # SQLite database
```

## Installation

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Initialize the database:
   ```bash
   python database.py
   ```
4. Run the application:
   ```bash
   python app.py
   ```
5. Open your browser to `http://localhost:5000`

## Usage Examples

### Detecting AI Content
Submit any text and get an AI percentage score. If over 30%, you'll see the option to humanize.

### Comparing Against Database
Your content is automatically compared against all stored submissions to detect plagiarism.

### Humanizing Content
Click "Humanize Content" to convert AI-detected text into more human-like writing while preserving meaning.

## Future Enhancements

- Integration with advanced NLP models (GPT-based detection)
- API key support for premium AI detection services
- PDF report generation
- User authentication and submission history
- Advanced plagiarism detection (crossref, external sources)
- Multi-language support

## License

Open source - feel free to use and modify for your needs.
