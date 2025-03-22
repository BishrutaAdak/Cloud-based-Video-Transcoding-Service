from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import ffmpeg
import boto3
from werkzeug.utils import secure_filename

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# AWS S3 Configuration
AWS_ACCESS_KEY = ' '  # Replace with your AWS access key
AWS_SECRET_KEY = ' '  # Replace with your AWS secret key
S3_BUCKET_NAME = ' '  # Replace with your S3 bucket name

# Initialize S3 client
s3 = boto3.client(
    's3',
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY
)

# Folder to store uploaded and transcoded videos
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Allowed video file extensions
ALLOWED_EXTENSIONS = {'mp4', 'avi', 'mov', 'mkv'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['POST'])
def upload_video():
    if 'video' not in request.files:
        return jsonify({'error': 'No video file provided'}), 400

    file = request.files['video']

    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file and allowed_file(file.filename):
        # Save the uploaded file
        filename = secure_filename(file.filename)
        input_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(input_path)

        # Transcode the video
        output_filename = f"transcoded_{filename}"
        output_path = os.path.join(app.config['UPLOAD_FOLDER'], output_filename)

        try:
            (
                ffmpeg
                .input(input_path)
                .output(output_path, vcodec='libx264', acodec='aac')
                .run()
            )
        except ffmpeg.Error as e:
            return jsonify({'error': f'Transcoding failed: {e.stderr}'}), 500

        # Upload the transcoded video to S3
        try:
            s3.upload_file(
                output_path,
                S3_BUCKET_NAME,
                f"videos/{output_filename}"
            )
        except Exception as e:
            return jsonify({'error': f'S3 upload failed: {str(e)}'}), 500

        # Clean up local files
        os.remove(input_path)
        os.remove(output_path)

        return jsonify({'message': 'Video uploaded and transcoded successfully!'}), 200

    return jsonify({'error': 'Invalid file type'}), 400

if __name__ == '__main__':
    app.run(debug=True)