from flask import Flask, session, redirect, request, render_template, flash, url_for, send_from_directory
from dotenv import load_dotenv
import os
import shutil

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = "9834dh095ohqdlksajdfc9234!5"

# Admin credentials (from .env file)
admin_username = os.getenv('admin_username', 'admin')  # Default to 'admin'
admin_password = os.getenv('admin_password', 'password')  # Default to 'password'

# Upload folder
UPLOAD_FOLDER = os.path.join('static', 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def check_type(filename):
    file_type = filename.split('.')[-1]
    file_extensions = {
        "jpeg": "Image",
        "jpg": "Image",
        "png": "Image",
        "gif": "Image",
        "ico": "Image",
        "bmp": "Image",
        "tiff": "Image",
        "svg": "Image",
        "webp": "Image",
        "pdf": "PDF",
        "mp4": "Video",
        "mp3": "Audio",
        "wav": "Audio",
        "ogg": "Audio",
        "flac": "Audio",
        "aac": "Audio",
        "alac": "Audio",
        "mpeg": "Video",
        "avi": "Video",
        "mov": "Video",
        "flv": "Video",
        "wmv": "Video",
        "docx": "Document",
        "doc": "Document",
        "rtf": "Document",
        "odt": "Document",
        "epub": "Document",
        "pptx": "Presentation",
        "ppt": "Presentation",
        "xls": "Excel file",
        "xlsx": "Excel file",
        "csv": "CSV",
        "txt": "Text file",
        "zip": "Archive",
        "rar": "Archive",
        "7z": "Archive",
        "tar": "Archive",
        "gz": "Archive",
        "bz2": "Archive",
        "xz": "Archive",
        "cpio": "Archive",
        "iso": "Disc image",
        "img": "Disc image",
        "dmg": "Disc image",
        "vhd": "Disc image",
        "vmdk": "Disc image",
        "exe": "Executable",
        "msi": "Windows installer",
        "bat": "Executable",
        "app": "Executable",
        "jar": "Executable",
        "py": "Python file",
        "js": "JS file",
        "cpp": "C++ file",
        "h": "C header file",
        "java": "Java file",
        "rb": "Ruby script",
        "pl": "Perl script",
        "go": "Go lang file",
        "html": "HTML file",
        "css": "CSS file",
        "xml": "XML file",
        "ttf": "Font",
        "otf": "Font",
        "sql": "Database file",
        "db": "Database file",
        "sqlite": "SQLite file",
        "json": "JSON file",
        "yaml": "YAML file",
        "md": "Markdown file",
        "vcs": "Version Control",
        "ini": "Configuration file",
    }
    return file_extensions.get(file_type, None)


@app.route('/')
def index():
    return redirect("/dashboard")


@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if not session.get('logged_in'):
        return redirect("/login")

    search_query = request.args.get('search', '').lower()

    files = os.listdir(app.config['UPLOAD_FOLDER'])
    file_data = []
    for i, file in enumerate(files):
        if search_query in file.lower():
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file)
            file_type = check_type(file)
            file_data.append({
                "id": i + 1,
                "name": file,
                "type": file_type,
                "size": f"{os.path.getsize(file_path) / 1024:.2f} KB"
            })
    total, used, free = shutil.disk_usage("/")
    stats = {"files": len(files), "used": used // (1024 ** 3), "free": free // (1024 ** 3)}
    return render_template("dashboard.html", files=file_data, search_query=search_query, stats=stats)



@app.route('/upload', methods=['POST'])
def upload():
    if not session.get('logged_in'):
        return redirect("/login")

    if 'file' not in request.files:
        flash("No file part")
        return redirect(url_for("dashboard"))

    files = request.files.getlist('file')
    for file in files:
        if file.filename != '':
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))

    flash("Files uploaded successfully!")
    return redirect(url_for("dashboard"))


@app.route('/download/<filename>')
def download_file(filename):
    if not session.get('logged_in'):
        return redirect("/login")
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)


@app.route('/delete/<filename>', methods=['POST'])
def delete_file(filename):
    if not session.get('logged_in'):
        return redirect("/login")
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if os.path.exists(file_path):
        os.remove(file_path)
        flash(f"File '{filename}' deleted successfully!")
    else:
        flash(f"File '{filename}' not found!")
    return redirect(url_for("dashboard"))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == admin_username and password == admin_password:
            session["logged_in"] = True
            return redirect('/dashboard')
        else:
            flash("Invalid credentials. Try again.")
    return render_template("login.html")


@app.route('/logout')
def logout():
    session.pop("logged_in", None)
    return redirect("/login")


if __name__ == '__main__':
    app.run(debug=True)
