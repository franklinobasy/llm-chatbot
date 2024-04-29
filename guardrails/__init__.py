"""
Module: guardrails/__init__.py

The `__init__.py` module serves as an initialization script for the `guardrails` package.

Variables:
    - guardrail_app: Instance of LLMRails representing the guardrails application with loaded configuration settings.

Usage:
    from guardrails import guardrail_app

    # Access the guardrails application instance
    app_instance = guardrail_app
"""
from guardrails.configs.config import guardrail_app
