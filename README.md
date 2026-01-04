# Ourion Backend API

## Project Overview
The OpenCV Ourion project aims to leverage computer vision and machine learning techniques to enhance recycling efficiency and accuracy. This repository contains the **Python/Flask backend** that processes images using OpenCV.

## Running Locally

### 1. Setup Virtual Environment
Open a terminal in the repository root:

**Windows (PowerShell):**
```
powershell
python -m venv venv
.\venv\Scripts\activate
```

**Windows (PowerShell):**
```
python3 -m venv venv
source venv/bin/activate
```

### 2. Install Dependencies
```
# Install backend dependencies (server-optimized)
pip install flask opencv-python-headless flask-cors gunicorn

# OR if you have a requirements file:
# pip install -r requirements.txt
```

### 3. Start the Server
```
python app.py
```

## Development Environment & Set Up (WSL + Docker)

This guide describes how to set up the development environment using Windows Subsystem for Linux (WSL) and Docker for containerization.

1. Install WSL (Ubuntu)

- Open PowerShell as Administrator.

- Run the command: wsl --install

- Restart your machine if prompted.

- When prompted, create a Linux user account.

2. Install Docker in WSL

- Install Docker Desktop for Windows.

- In Docker Desktop > Settings > General, ensure Use WSL 2 based engine is enabled.

- In Ubuntu (WSL), run:

```
# Add Docker's official GPG key:
sudo apt-get update
sudo apt-get install ca-certificates curl gnupg
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL [https://download.docker.com/linux/ubuntu/gpg](https://download.docker.com/linux/ubuntu/gpg) | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg

# Add the repository to Apt sources:
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] [https://download.docker.com/linux/ubuntu](https://download.docker.com/linux/ubuntu) \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update

# Install Docker
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```

3. Clone the Repository

```
git clone [https://github.com/YOUR_USERNAME/ourion-api.git](https://github.com/mmurata22/ourion-api.git)

```
