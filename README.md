# English learning app

# Requirements

- uv (https://docs.astral.sh/uv/getting-started/installation/)

# Setup venv

    uv venv
    uv pip install -r requirements.txt
    source .venv/bin/activate

# Tests
    
    uv pip install tox
    tox

# Run fastapi view

    uvicorn fastapi_view:app --reload

# Run cli version

    python main.py