from flask import Flask, render_template, request
import os
from main import process_video  
from flask_cors import CORS

app = Flask(__name__)

CORS(app)

UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'static'

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)


@app.route('/', methods=['GET', 'POST'])
def index():
    output_video = None
    entry_count = None
    exit_count = None

    if request.method == 'POST':
        video_file = request.files['video']
        orientation = request.form['orientation']
        line_pos = int(request.form['line_pos'])

        # Save uploaded file
        video_path = os.path.join(UPLOAD_FOLDER, video_file.filename)
        video_file.save(video_path)

        # Run YOLO footfall counter
        output_path = os.path.join(OUTPUT_FOLDER, 'output.mp4')
        entry_count, exit_count = process_video(video_path, output_path, line_pos, orientation)

        output_video = 'output.mp4'

    return render_template(
        'index.html',
        output_video=output_video,
        entry_count=entry_count,
        exit_count=exit_count
    )


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
