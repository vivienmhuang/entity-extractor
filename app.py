# /***********************************************************************************************************************************************
# Load in libraries and environment variables
# ***********************************************************************************************************************************************/
from flask import Flask, request, jsonify, send_file
import os
import json

# Read in scripts
from pipeline.python.logging import Logger
from pipeline.python.preprocessing import *

# Initialise logger
logger = Logger(__name__)

# Start app
app = Flask(__name__)

# /***********************************************************************************************************************************************
# Add upload folder
# ***********************************************************************************************************************************************/
UPLOAD_FOLDER = 'pipeline/uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# /***********************************************************************************************************************************************
# Run app
# ***********************************************************************************************************************************************/
@app.route('/api/v1/extract', methods=['POST'])
def extract():
    # Check if file is present in request
    if 'file' not in request.files:
        return jsonify({"error": "Bad request, file not included or empty filename."}), 400
    
    file = request.files['file']
    
    # Check if filename is empty
    if file.filename == '':
        return jsonify({"error": "Bad request, file not included or empty filename."}), 400
    
    # Check file extension
    if not file.filename.lower().endswith('.pdf'):
        return jsonify({"error": "Unsupported file type."}), 415
    
    try:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)
        
        # Process pdf
        text = extract_text_from_pdf(filepath, logger)
        entities = extract_entities(text, logger)
        
        # Remove file from folder
        os.remove(filepath)
        
        return jsonify(entities), 200
    
    except Exception as e:
        logger.error(f"Error processing request: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

@app.route('/openapi.yaml')
def serve_openapi_spec():
    return send_file('openapi.yaml', mimetype='text/yaml')

if __name__ == '__main__':
    app.run(debug=True, port=5000)