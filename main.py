"""
Root entry point for Cloud Run
Imports backend.main as a proper package
"""
from backend.main import app

# Export app for uvicorn to find
__all__ = ["app"]
