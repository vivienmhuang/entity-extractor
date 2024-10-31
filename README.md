# Medical Entity Extraction API

A Flask-based API for extracting and contextualising entities from medical and research papers. 

## Overview

This API provides endpoints for:
- Extracting text from PDF documents
- Identifying and contextualizing entities in scientific text
- Returning structured JSON responses with entity information

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd <project-directory>
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install required packages:
```bash
pip install -r requirements.txt
```

4. Install the required spaCy model from https://allenai.github.io/scispacy/:
```bash
pip install scispacy
pip install https://s3-us-west-2.amazonaws.com/ai2-s2-scispacy/releases/v0.5.4/en_core_sci_lg-0.5.4.tar.gz
```

## Project Structure
```
.
├── app.py                  # Main Flask application
├── pipeline/
│   ├── uploads/           # Temporary PDF storage
│   └── python/
│       ├── logging.py     # Logging configuration
│       └── preprocessing.py# Text extraction and processing
├── requirements.txt       # Project dependencies
└── openapi.yaml          # API specification
```

## Testing with Postman

### Setup in Postman

1. **Create a New Collection**
   - Open Postman
   - Click "New" -> "Collection"
   - Name it "PDF Entity Extraction API"

2. **Import OpenAPI Specification** (Optional)
   ```
   http://localhost:5000/openapi.yaml
   ```

### Testing Endpoints

#### Entity Extraction Endpoint

1. **Create New Request**
   - Method: `POST`
   - URL: `http://localhost:5000/api/v1/extract`

2. **Configure Request**
   - Go to "Body" tab
   - Select "form-data"
   - Add key: `file`
   - Change type to "File"
   - Select your PDF file

Example request setup:
```
POST http://localhost:5000/api/v1/extract
Body: form-data
Key: file
Type: File
Value: [Select PDF file]
```

### Expected Responses

1. **Successful Response (200 OK)**
```json
[
    {
        "text": "CCR5",
        "start": 100,
        "end": 104,
        "context": "... uses on the relief of symptoms rather than on a biological ‘cure’. have identified rare mutations in CCR5 that confer resilience against ..."
    }
]
```

2. **Error Responses**
   - No file uploaded (400):
     ```json
     {
         "error": "Bad request, file not included or empty filename."
     }
     ```
   - Wrong file type (415):
     ```json
     {
         "error": "Unsupported file type."
     }
     ```
   - Server error (500):
     ```json
     {
         "error": "Internal server error"
     }
     ```