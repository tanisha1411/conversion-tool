from flask import Flask, render_template, request
import os
from werkzeug.utils import secure_filename
from doc_analyzer import analyze_document

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf', 'docx', 'txt', 'jpg', 'jpeg', 'png'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    filename = None
    structured_data = None
    answer = None

    if request.method == 'POST':
        # If file is uploaded
        if 'file' in request.files:
            file = request.files['file']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                # Analyze immediately after upload (no query yet)
                structured_data, answer, tables = analyze_document(filepath, None)
                structured_data = structured_data.to_string(index=False)
                tables_html = ""
                if tables:
                    for idx, table in enumerate(tables):
                        if hasattr(table, 'to_html'):
                            tables_html += f"<h4>Table {idx+1}</h4>{table.to_html(index=False)}"
                        else:
                            tables_html += f"<h4>Table {idx+1}</h4><pre>{table}</pre>"
                return render_template('index2.html', filename=filename, structured_data=structured_data, tables_html=tables_html, answer=None)
        # If query is submitted
        elif 'filename' in request.form and 'query' in request.form:
            filename = request.form['filename']
            user_query = request.form['query']
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            structured_data, answer, tables = analyze_document(filepath, user_query)
            # Convert DataFrame to string for display
            structured_data = structured_data.to_string(index=False)
            return render_template('index2.html', filename=filename, structured_data=structured_data, answer=answer)

    return render_template('index2.html')

if __name__ == '__main__':
    app.run(debug=True)