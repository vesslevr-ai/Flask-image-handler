import os
from flask import Flask, request, send_from_directory, render_template_string
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB

# Ensure uploads folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Allowed file check
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    uploaded_filename = None
    if request.method == 'POST':
        if 'file' not in request.files:
            return 'No file part'
        file = request.files['file']
        if file.filename == '':
            return 'No selected file'
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            uploaded_filename = filename

    return render_template_string('''
    <!doctype html>
    <html>
    <head>
        <title>Upload new File</title>
        <style>
            body, html {
                margin: 0;
                padding: 0;
                height: 100%;
                font-family: Arial, sans-serif;
                color: white;
                text-align: center;
            }

            /* Background video */
            .bg-video {
                position: fixed;
                right: 0;
                bottom: 0;
                min-width: 100%;
                min-height: 100%;
                z-index: -1;
                object-fit: cover;
            }

            /* Content overlay */
            .content {
                position: relative;
                z-index: 1;
                top: 50%;
                transform: translateY(-50%);
                background-color: rgba(0,0,0,0.5);
                padding: 30px;
                border-radius: 10px;
                display: inline-block;
            }

            form input[type=file] {
                margin: 10px 0;
            }

            form input[type=submit] {
                padding: 5px 15px;
                border: none;
                border-radius: 5px;
                background-color: #4CAF50;
                color: white;
                cursor: pointer;
            }

            .uploaded-img {
                margin-top: 20px;
                max-width: 80%;
                border: 5px solid #fff;
                border-radius: 10px;
            }
        </style>
    </head>
    <body>
        <!-- Background video -->
        <video autoplay muted loop class="bg-video">
            <source src="{{ url_for('static', filename='background.mp4') }}" type="video/mp4">
            Your browser does not support HTML5 video.
        </video>

        <div class="content">
            <h1>Upload a File</h1>
            <form method="post" enctype="multipart/form-data">
              <input type="file" name="file">
              <input type="submit" value="Upload">
            </form>

            {% if uploaded_filename %}
                <div>
                    <h2>Uploaded Image:</h2>
                    <img class="uploaded-img" src="{{ url_for('uploaded_file', filename=uploaded_filename) }}">
                </div>
            {% endif %}
        </div>
    </body>
    </html>
    ''', uploaded_filename=uploaded_filename)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)