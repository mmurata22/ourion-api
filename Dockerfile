# 1. Use a lightweight Python base
FROM python:3.11-slim

# 2. Install the system libraries that OpenCV needs
# (This is why we need Docker. Standard Python environments lack these)
RUN apt-get update && apt-get install -y \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgl1-mesa-glx \
    && rm -rf /var/lib/apt/lists/*

# 3. Set up the app directory
WORKDIR /app

# 4. Install Python libraries
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy your code (app.py)
COPY . .

# 6. Expose the port
ENV PORT=10000
EXPOSE 10000

# 7. Run the app
# We use 'app:app' because your file is named 'app.py' and the Flask instance is likely named 'app' inside it.
CMD ["gunicorn", "--bind", "0.0.0.0:10000", "app:app"]