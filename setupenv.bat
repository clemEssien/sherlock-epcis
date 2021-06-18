@echo off

echo Setting up Python environment for Windows...

python -m venv ./env
call env/Scripts/activate.bat
pip install -r requirements.txt

echo Setup Complete.