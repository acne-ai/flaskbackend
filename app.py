from flask import Flask, request, render_template, send_file, jsonify
from flask_cors import CORS
from datetime import datetime
from openai import OpenAI
import json

app = Flask(__name__)

# Enable CORS for all routes
CORS(app)

# establish openai client using api key environment variable
client = OpenAI()

#prompt paths
file_path1 = "prompt_preface.txt"
file_path2 = "prompt_body.txt"

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

    image_path = f"uploads/{generate_filename()}"
    #image_path = f"/uploads/{generate_filename()}"
    image.save(image_path)

    #INSERT MACHINE LEARNING HERE
    acne_type = "papulosapustulosa"

    #OPEN AI INTGRATION
    #Read content from the first file
    with open(file_path1, "r") as file1:
        content1 = file1.read()
    # Read content from the second file
    with open(file_path2, "r") as file2:
        content2 = file2.read()
    combined_prompt = f"{content1}{acne_type}\n{content2}"
    # Call the OpenAI GPT-3.5-turbo API for completion
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": combined_prompt}
        ]
    )

    #Extract the model's reply 
    cleaned_data = completion.choices[0].message.content

    # Handle the case where the cleaned_data starts with '{' directly after newline
    if cleaned_data[0] == '{':
        json_data = json.loads(cleaned_data)
    else:
        # If there are additional characters before '{', remove them
        json_start_index = cleaned_data.find('{')
        if json_start_index != -1:
            cleaned_data = cleaned_data[json_start_index:]
        json_data = json.loads(cleaned_data)

    print(json_data)

    return json_data
