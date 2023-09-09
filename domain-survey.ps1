if (-not (Test-Path .\.venv -PathType Container)) {
    virtualenv .venv
}

.\.venv\Scripts\Activate.ps1

pip install -r .\requirements.txt
python domain-survey.py
