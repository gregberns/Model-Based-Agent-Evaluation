# packages/framework/utils/api_key.py

import os
from pathlib import Path
from typing import Optional
import logging

logger = logging.getLogger(__name__)

def get_gemini_api_key(command_line_key: Optional[str] = None) -> str:
    """
    Get the Gemini API key from multiple sources with priority order.

    Priority order:
    1. Command line argument (highest priority)
    2. .env file in project root
    3. GEMINI_API_KEY environment variable
    4. .env file in home directory

    Args:
        command_line_key: API key provided via command line argument

    Returns:
        str: The Gemini API key

    Raises:
        ValueError: If no API key is found in any source
    """

    # 1. Check command line argument first (highest priority)
    if command_line_key:
        logger.info("Using API key from command line argument")
        return command_line_key

    # 2. Check for .env file in project root
    project_root = Path(__file__).parent.parent.parent.parent
    env_file = project_root / ".env"

    if env_file.exists():
        try:
            with open(env_file, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and '=' in line and not line.startswith('#'):
                        key, value = line.split('=', 1)
                        if key.strip() == 'GEMINI_API_KEY':
                            logger.info("Using API key from project .env file")
                            return value.strip()
        except Exception as e:
            logger.warning(f"Could not read .env file: {e}")

    # 3. Check environment variable
    env_key = os.getenv('GEMINI_API_KEY')
    if env_key:
        logger.info("Using API key from environment variable")
        return env_key

    # 4. Check for .env file in home directory
    home_env_file = Path.home() / ".env"
    if home_env_file.exists():
        try:
            with open(home_env_file, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and '=' in line and not line.startswith('#'):
                        key, value = line.split('=', 1)
                        if key.strip() == 'GEMINI_API_KEY':
                            logger.info("Using API key from home .env file")
                            return value.strip()
        except Exception as e:
            logger.warning(f"Could not read home .env file: {e}")

    # If no API key found, raise an error
    raise ValueError(
        "No Gemini API key found. Please provide one of the following:\n"
        "1. Command line argument: --api-key YOUR_KEY\n"
        "2. Project .env file: Add GEMINI_API_KEY=your_key to .env\n"
        "3. Environment variable: export GEMINI_API_KEY=your_key\n"
        "4. Home .env file: Add GEMINI_API_KEY=your_key to ~/.env"
    )

def validate_api_key(api_key: str) -> bool:
    """
    Basic validation of the API key format.

    Args:
        api_key: The API key to validate

    Returns:
        bool: True if the key appears valid, False otherwise
    """
    if not api_key:
        return False

    # Basic format checks - Gemini API keys are typically long strings
    if len(api_key) < 20:
        return False

    # Should not contain common whitespace characters
    if any(char.isspace() for char in api_key):
        return False

    return True
