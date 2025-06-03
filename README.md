# SIS AI Assistant

An intelligent surgical information chatbot built to streamline surgical case management, patient scheduling, and appointment handling.

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

### Environment

- **Node.js** ≥ 18.x  
- **npm** ≥ 8.x  

---

## Running the Backend

```bash
cd backend
source venv/bin/activate
uvicorn app:app --reload
```

Visit: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## Running the Frontend

```bash
cd chatbot-frontend
npm install
npm run dev
```

Visit: [http://localhost:5173](http://localhost:5173)

---

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

## Example Workflow

1. Open the app at [http://localhost:5173](http://localhost:5173)  
2. Choose a preloaded question (e.g., “How do I add a patient?”)  
3. View the AI-generated response  
4. Ask follow-up questions directly  

---

## Further Customization

- Expand `preload.py` (backend) and update UI for new question sets  
- Add streaming responses to reduce perceived latency  
- Connect to a database for persistent state (e.g., PostgreSQL, MongoDB)  
- Deploy backend via Uvicorn/Gunicorn and proxy (e.g., NGINX)  
- Deploy frontend via Vercel, Netlify, or GitHub Pages  

---

## License

MIT License

