@echo off
cd /d D:\AgriAI\backend
call venv\Scripts\activate
uvicorn app.main:app --reload
pause
