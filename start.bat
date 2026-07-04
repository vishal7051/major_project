@echo off
echo Starting AI Career Platform...

start cmd /k "cd backend && call venv\Scripts\activate.bat && uvicorn main:app --host 0.0.0.0 --port 8000"

start cmd /k "cd frontend && npm run dev"

start cmd /k "npx -y n8n@1"

echo All servers started!
echo Backend:  http://localhost:8000/docs
echo Frontend: http://localhost:3000
echo n8n:      http://localhost:5678
pause
