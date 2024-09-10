import click
from flask import Flask, request, render_template, jsonify
import requests
import base64

app = Flask(__name__)

# Global configuration variables
IMAGE_GENERATOR_URL = None
PROMPT = None

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def index(path):
    return render_template('index.html')

@app.route('/generate-image', methods=['POST'])
def generate_image():
    try:
        # Get the width and height from the client
        data = request.json
        width = data.get('width')
        height = data.get('height')

        if not width or not height:
            return jsonify({"error": "Width and height must be provided"}), 400

        # Call the image generator API (server-to-server communication)
        response = requests.post(IMAGE_GENERATOR_URL, json={
            "prompt": PROMPT, 
            "width": width, 
            "height": height,
            "steps": 50
        })

        # Check if the response was successful
        if response.status_code == 200:
            # Extract base64 image data
            data = response.json()
            image_base64 = data.get('image', '')

            return jsonify({"image": image_base64}), 200
        else:
            return jsonify({"error": "Failed to generate image"}), 500

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@click.command()
@click.option('--generator-host', default='localhost', help='Hostname of the image generator.')
@click.option('--generator-port', default=8888, help='Port of the image generator.')
@click.option('--prompt', default='A futuristic cityscape', help='The prompt to send to the image generator.')
@click.option('--host', default='127.0.0.1', help='Host for this Flask server.')
@click.option('--port', default=5000, help='Port for this Flask server.')
def main(generator_host, generator_port, prompt, host, port):
    global IMAGE_GENERATOR_URL
    global PROMPT

    # Set the generator URL and prompt
    IMAGE_GENERATOR_URL = f"http://{generator_host}:{generator_port}/generate"
    PROMPT = prompt

    # Run the Flask app
    app.run(host=host, port=port)

if __name__ == "__main__":
    main()

