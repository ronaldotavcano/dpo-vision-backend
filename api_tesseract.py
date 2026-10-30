"""Compatibility entry point: uvicorn api_tesseract:app."""
from dpo_vision.api.app import app, executar_tesseract

__all__ = ["app", "executar_tesseract"]
