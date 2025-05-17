import os
from fastapi import FastAPI, File, UploadFile, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import tensorflow as tf
import numpy as np
from PIL import Image
import io
import aiofiles
import uuid

app = FastAPI()

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Load the model
try:
    model = tf.keras.models.load_model("model.keras")
except Exception as e:
    print("Error loading model.h5:", e)
    model = None

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

def process_image(image_path):
    """Process image for model prediction"""
    img = Image.open(image_path)
    # Resize image to match model's expected input size
    # Note: Adjust size based on your model's requirements
    img = img.resize((128, 128))
    img_array = tf.keras.preprocessing.image.img_to_array(img)
    img_array = tf.expand_dims(img_array, 0)
    img_array = img_array / 255.0  # Normalize pixel values
    return img_array

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    if not model:
        return JSONResponse(
            content={"error": "Model not loaded. Please ensure model.h5 is present."},
            status_code=500
        )
    
    # Generate unique filename
    file_ext = os.path.splitext(file.filename)[1]
    unique_filename = f"{uuid.uuid4()}{file_ext}"
    file_path = os.path.join(UPLOAD_DIR, unique_filename)
    
    try:
        # Save uploaded file
        async with aiofiles.open(file_path, 'wb') as out_file:
            content = await file.read()
            await out_file.write(content)
        
        # Process image and make prediction
        img_array = process_image(file_path)
        prediction = model.predict(img_array)
        
        # Get prediction result
        # Assuming binary classification where 1 = error, 0 = no error
        has_error = bool(prediction[0][0] > 0.5)
        confidence = float(abs(prediction[0][0] - 0.5) * 2 * 100)
        
        # Clean up uploaded file
        os.remove(file_path)
        
        return {
            "has_error": has_error,
            "confidence": confidence,
            "message": "❌ Error detected" if has_error else "✅ No error"
        }
        
    except Exception as e:
        if os.path.exists(file_path):
            os.remove(file_path)
        return JSONResponse(
            content={"error": str(e)},
            status_code=500
        )

@app.get("/info", response_class=HTMLResponse)
async def info(request: Request):
    return templates.TemplateResponse("info.html", {"request": request})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 