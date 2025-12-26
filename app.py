import os
import subprocess
import re
from fastapi import FastAPI, Request, Response

app = FastAPI()

PORT = int(os.environ.get("PORT", 8000))
PIPER_BINARY = "/app/piper/piper"

# Updated Model Paths
MODELS = {
    "en": "/app/model_en.onnx",      # English
    "hi": "/app/model_rohan.onnx"    # Hindi (Rohan Updated)
}

def is_hindi(text):
    """Hindi characters detect karne ke liye"""
    return bool(re.search(r'[\u0900-\u097F]', text))

@app.post("/tts")
async def generate_speech(request: Request):
    try:
        data = await request.json()
        
        # Text fetch karein
        text = data.get("text") or data.get("input") or data.get("message") or data.get("content")
        
        if not text:
            print("LOG: No text found")
            return {"error": "No text provided"}

        # --- Smart Language Selection ---
        if is_hindi(text):
            print(f"LOG: Hindi (Rohan) Detected -> {text[:15]}...")
            model_path = MODELS["hi"]  # Ab Rohan model use hoga
        else:
            print(f"LOG: English Detected -> {text[:15]}...")
            model_path = MODELS["en"]

        command = [
            PIPER_BINARY,
            "--model", model_path,
            "--output_file", "-"
        ]

        process = subprocess.Popen(
            command,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        wav_audio, error = process.communicate(input=text.encode('utf-8'))

        if process.returncode != 0:
            return {"error": f"Piper Error: {error.decode('utf-8')}"}

        return Response(content=wav_audio, media_type="audio/wav")
    
    except Exception as e:
        return {"error": f"Server Error: {str(e)}"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=PORT)