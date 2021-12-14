@echo off
uvicorn clinicapi.main:app --reload  --reload-exclude *.pdf --host 0.0.0.0
pause