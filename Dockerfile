# 1. Base Image
FROM python:3.9-slim

# 2. Working Directory
WORKDIR /app

# 3. System Tools
RUN apt-get update && apt-get install -y \
    wget \
    tar \
    && rm -rf /var/lib/apt/lists/*

# 4. Piper Binary Download
RUN wget -O piper.tar.gz https://github.com/rhasspy/piper/releases/download/2023.11.14-2/piper_linux_x86_64.tar.gz \
    && tar -xvf piper.tar.gz \
    && rm piper.tar.gz

# 5. Voice Models Download

# --- English (US Medium) ---
RUN wget -O model_en.onnx https://huggingface.co/rhasspy/piper-voices/resolve/main/en/en_US/lessac/medium/en_US-lessac-medium.onnx
RUN wget -O model_en.onnx.json https://huggingface.co/rhasspy/piper-voices/resolve/main/en/en_US/lessac/medium/en_US-lessac-medium.onnx.json

# --- Hindi (Rohan Medium - NEW) ---
# Yahan humne Alma ki jagah Rohan model ka link dala hai
RUN wget -O model_rohan.onnx https://huggingface.co/rhasspy/piper-voices/resolve/main/hi/hi_IN/rohan/medium/hi_IN-rohan-medium.onnx
RUN wget -O model_rohan.onnx.json https://huggingface.co/rhasspy/piper-voices/resolve/main/hi/hi_IN/rohan/medium/hi_IN-rohan-medium.onnx.json

# 6. Python Deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 7. App Code
COPY app.py .

# 8. Start Command
CMD ["python", "app.py"]