from flask import Flask, request, render_template, send_file, jsonify
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)

# Enable CORS for all routes
CORS(app)

#function to generate filenames based on timestamp
def generate_filename():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"uploaded_image_{timestamp}.png"

@app.route('/')
def hello():
    return '<h1>Pls No Hack</h1>'

@app.route('/api/upload', methods=['POST'])
def upload_image():
    #key value pair missing in form-data of content body
    if 'image' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    image = request.files['image']

    if image.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    # Add additional checks if needed (e.g., file extension, file size)

    # Save the image to a temporary file (optional)
    image_path = f"/uploads/{generate_filename()}"
    image.save(image_path)

    #INSERT MACHINE LEARNING HERE

    # Include the image path in the response
    response_data = {'message': 'Image uploaded successfully', 'image_path': image_path}

    return jsonify(response_data)