"""Configuration module for loading environment variables."""

import os
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv


class Config:
    """Configuration class for API credentials and settings."""

    def __init__(self) -> None:
        """Initialize configuration by loading environment variables."""
        # Load .env file from project root
        env_path = Path(__file__).parent.parent / ".env"
        load_dotenv(dotenv_path=env_path)

        self.api_key: Optional[str] = os.getenv("BINANCE_API_KEY")
        self.api_secret: Optional[str] = os.getenv("BINANCE_API_SECRET")
        self.testnet_url: str = "https://testnet.binancefuture.com"

    def is_valid(self) -> bool:
        """
        Validate that required credentials are set.

        Returns:
            bool: True if both API key and secret are set, False otherwise.
        """
        return bool(self.api_key and self.api_secret)

    def get_api_key(self) -> str:
        """
        Get API key.

        Returns:
            str: API key.

        Raises:
            ValueError: If API key is not configured.
        """
        if not self.api_key:
            raise ValueError(
                "BINANCE_API_KEY not found in environment. "
                "Please set it in .env file."
            )
        return self.api_key

    def get_api_secret(self) -> str:
        """
        Get API secret.

        Returns:
            str: API secret.

        Raises:
            ValueError: If API secret is not configured.
        """
        if not self.api_secret:
            raise ValueError(
                "BINANCE_API_SECRET not found in environment. "
                "Please set it in .env file."
            )
        return self.api_secret

    def get_testnet_url(self) -> str:
        """
        Get testnet URL.

        Returns:
            str: Testnet URL.
        """
        return self.testnet_url
