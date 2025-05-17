# 3D Model Error Detector

A web application that uses machine learning to detect errors in 3D models and 3D-printed objects. Upload an image of your 3D model or print, and the application will analyze it for potential defects.

## Features

- Fast and accurate error detection using a trained Keras model
- Modern, responsive web interface
- Drag-and-drop image upload
- Real-time image preview
- Clear error detection results with confidence scores
- Mobile-friendly design

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Virtual environment (recommended)

## Setup

1. Clone this repository or download the files to your local machine.

2. Place your trained model file `model.h5` in the root directory of the project.

3. Create and activate a virtual environment (recommended):
   ```bash
   python -m venv venv
   # On Windows:
   .\venv\Scripts\activate
   # On Unix or MacOS:
   source venv/bin/activate
   ```

4. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

1. Make sure your virtual environment is activated.

2. Start the FastAPI server:
   ```bash
   uvicorn main:app --reload
   ```

3. Open your web browser and navigate to:
   ```
   http://localhost:8000
   ```

## Usage

1. Click the upload area or drag and drop an image of your 3D model/print.
2. Wait for the analysis to complete.
3. View the results, which will show either:
   - ✅ No error (with confidence score)
   - ❌ Error detected (with confidence score)

## Project Structure

```
3d_error_detector/
├── main.py              # FastAPI application
├── model.h5             # Your trained Keras model
├── requirements.txt     # Python dependencies
├── templates/
│   └── index.html      # Web interface
└── uploads/            # Temporary folder for uploads
```

## Notes

- The application automatically deletes uploaded images after processing
- The model expects images to be resized to 224x224 pixels
- Supported image formats: JPG, PNG, GIF
- For best results, ensure good lighting and clear visibility of the 3D model in the image

## Error Messages

If you encounter any issues:

- Check that `model.h5` is present in the root directory
- Ensure all dependencies are installed correctly
- Verify that the uploaded file is a valid image format
- Check the console for any Python errors 