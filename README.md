# SIS AI Assistant

A lightweight AI‐powered chat interface for Surgical Information Systems (SIS).  
The project consists of:

1. **Backend** (FastAPI)  
   - Hosts a `/chat` endpoint that uses a HuggingFace model (e.g. `tiiuae/falcon-rw-1b`) to generate responses  
   - Implements basic FHIR‐style handlers for patients and appointments  
   - CORS‐enabled for a separate frontend

2. **Frontend** (Vite + React + Tailwind CSS)  
   - A responsive chat UI that sends user questions to the FastAPI `/chat` endpoint  
   - Displays conversation history, loading states, and preloaded SIS‐specific prompts  

---

## Technologies

### Backend

- **FastAPI** - High-performance, asynchronous Python web framework  
- **Uvicorn** - Fast ASGI server implementation  
- **Pydantic** - Data validation and settings management  
- **Transformers (HuggingFace)** - AI language modeling (e.g., `tiiuae/falcon-rw-1b`)  
- **PyTorch** - Deep learning framework for model inference  
- **FHIRClient** - Integration with FHIR resources  
- **HTTPX** - HTTP client for backend interactions  
- **Rich** - Enhanced console output  
- **python-dotenv** - Environment variable management  

### Frontend

- **React** - JavaScript library for UI development  
- **Vite** - Fast build tool with instant hot module replacement (HMR)  
- **Tailwind CSS (v3.4.17)** - Utility-first CSS framework  
- **PostCSS & Autoprefixer** - CSS processing and vendor prefix automation  

## Prerequisites

Make sure you have the following installed:

- **Python 3.12.x** (3.12.3 recommended)  
- **Node.js 18.x or later** (with npm)  
- A CPU or GPU environment (CPU‐only works but is slower for inference)  
  - If you have an NVIDIA GPU, install PyTorch with CUDA support for faster inference  

---


## Backend Setup

### 1. Clone and Create Virtual Environment

```bash
git clone <your‐repo‐url> SIS-AI-Assistant
cd SIS-AI-Assistant/backend

# Create a virtual environment (Python 3.12)
python3 -m venv venv
source venv/bin/activate

# Install Dependencies
pip install --upgrade pip
pip install -r requirements.txt
```
### 2. Start The FastAPI Server
```bash
uvicorn app:app --reload
```
---
## Running the Frontend

Follow these steps to install dependencies and start the Vite + React + Tailwind (v3.4.17) frontend:

1. **Navigate to the `chatbot-frontend/` directory**  
   ```bash
   cd chatbot-frontend

2. **Install all Node.js dependencies**
    npm install

3. **Run the development server**
    npm run dev
    ```
----

## Usage

### Interacting with SIS AI Assistant

- **Preloaded Questions**:  
  Select from suggested questions to immediately get AI assistance.

- **Custom Queries**:  
  Enter your surgical or patient-related questions in the input field and press **Ask** to receive AI-generated responses.

- **FHIR Integration** (test with `curl`):  
```bash
curl http://127.0.0.1:8000/patient/{patient_id}
curl http://127.0.0.1:8000/appointments?date=2025-06-03
```

---
