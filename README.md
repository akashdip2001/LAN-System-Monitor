# LAN System Monitor

![IMG20250817035818](https://github.com/user-attachments/assets/af2a9bba-0371-4707-a97a-7ed1442054c2)

A lightweight **LAN-based system monitoring tool** built with **FastAPI + WebSockets**.
It allows you to monitor CPU, RAM, Disk, Processes, and Network usage of your system **from any device on your local network** via a browser.

---

## 🚀 Features

* 📊 Real-time system metrics (CPU, RAM, Disk, Processes, Network)
* 🌍 Access from any device on the same LAN (PC, phone, tablet)
* 🔒 Token-based authentication
* ⚡ Fast, asynchronous backend using **FastAPI + Uvicorn**
* 🖥️ Web dashboard auto-refreshes metrics every second

---

## 📂 Project Structure

```
LAN-System-Monitor/
│── main.py        # Main application script
│── requirements.txt
│── README.md
│── dist/          # (generated after building exe with PyInstaller)
│── venv/          # (optional, local virtual environment)
```

---

## 🔧 Installation & Setup

### 1️⃣ Clone Repository

```bash
git clone https://github.com/yourusername/LAN-System-Monitor.git
cd LAN-System-Monitor
```

### 2️⃣ Create Virtual Environment (Recommended)

```bash
python -m venv venv
source venv/bin/activate   # on Linux / Mac
venv\Scripts\activate      # on Windows
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

If you don’t have `requirements.txt` yet, create it with:

```txt
fastapi
uvicorn
psutil
```

---

## ▶️ Running the Agent

### Run with Python

```bash
python main.py
```

You’ll see output like:

```
Agent URL:   http://192.168.1.42:8765
Auth token:  'change-me'
```

<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/6133dbae-dd1f-4f38-802f-6ab18b2e33b2" />

Open that URL in your browser **(PC or mobile)**, enter the token, and start monitoring.

---

## 🔒 Configuration

The agent uses **environment variables** for customization:

* `AGENT_PORT` → Server port (default: `8765`)
* `AGENT_TOKEN` → Auth token (default: `change-me`)

Example (Linux/macOS):

```bash
export AGENT_PORT=9000
export AGENT_TOKEN=super-secret
python main.py
```

Example (Windows PowerShell):

```powershell
$env:AGENT_PORT="9000"
$env:AGENT_TOKEN="super-secret"
python main.py
```

---

## 📦 Building Standalone EXE (Windows)

Use **PyInstaller** to create a single-file executable:

```bash
pip install pyinstaller
pyinstaller --onefile main.py
```

The EXE will be generated in the `dist/` folder.
Run it directly:

```powershell
dist\main.exe
```

---

## 🛠 Tech Stack

* [FastAPI](https://fastapi.tiangolo.com/) – High-performance API framework
* [Uvicorn](https://www.uvicorn.org/) – ASGI server
* [psutil](https://pypi.org/project/psutil/) – System resource monitoring

---

<p align="center">
  <img src="https://github.com/user-attachments/assets/c99cf8a3-1382-44dd-9068-ab4ecd31b6ca" width="72%" /> 
  <img src="https://github.com/user-attachments/assets/f8adb944-c479-40fa-bdf5-d156c1fcdd94" width="23%" /> 
</p>
