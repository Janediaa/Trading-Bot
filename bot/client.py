"""Binance Futures client wrapper."""

from typing import Dict, Any, Optional
from binance.um_futures import UMFutures
from binance.error import ClientError as BinanceClientError
from bot.config import Config
from bot.logging_config import LoggerSetup

logger = LoggerSetup.get_logger(__name__)


class BinanceClientError(Exception):
    """Custom exception for Binance client errors."""

    pass


class BinanceFuturesClient:
    """Wrapper for Binance Futures Testnet client."""

    def __init__(self) -> None:
        """
        Initialize Binance Futures Testnet client.

        Raises:
            BinanceClientError: If API credentials are not configured.
        """
        self.config = Config()

        if not self.config.is_valid():
            error_msg = (
                "API credentials not configured. "
                "Please set BINANCE_API_KEY and BINANCE_API_SECRET in .env"
            )
            logger.error(error_msg)
            raise BinanceClientError(error_msg)

        try:
            self.client = UMFutures(
                key=self.config.get_api_key(),
                secret=self.config.get_api_secret(),
                base_url=self.config.get_testnet_url(),
            )
            logger.info("Binance Futures Testnet client initialized successfully")
        except Exception as e:
            error_msg = f"Failed to initialize Binance client: {str(e)}"
            logger.error(error_msg)
            raise BinanceClientError(error_msg)

    def place_market_order(
        self, symbol: str, side: str, quantity: float
    ) -> Dict[str, Any]:
        """
        Place a market order.

        Args:
            symbol: Trading symbol (e.g., BTCUSDT).
            side: Order side (BUY or SELL).
            quantity: Order quantity.

        Returns:
            Dict containing order response from Binance API.

        Raises:
            BinanceClientError: If order placement fails.
        """
        try:
            logger.debug(
                f"Placing market order: {side} {quantity} {symbol}"
            )

            params = {
                "symbol": symbol,
                "side": side,
                "type": "MARKET",
                "quantity": quantity,
            }

            logger.debug(f"Order request parameters: {params}")

            response = self.client.new_order(**params)

            logger.info(
                f"Market order placed successfully: "
                f"Symbol={symbol}, Side={side}, Quantity={quantity}, "
                f"OrderID={response.get('orderId')}"
            )

            return response

        except BinanceClientError as e:
            error_msg = f"Binance API error: {str(e)}"
            logger.error(error_msg)
            raise BinanceClientError(error_msg)
        except Exception as e:
            error_msg = f"Unexpected error placing market order: {str(e)}"
            logger.error(error_msg)
            raise BinanceClientError(error_msg)

    def place_limit_order(
        self, symbol: str, side: str, quantity: float, price: float
    ) -> Dict[str, Any]:
        """
        Place a limit order.

        Args:
            symbol: Trading symbol (e.g., BTCUSDT).
            side: Order side (BUY or SELL).
            quantity: Order quantity.
            price: Order price.

        Returns:
            Dict containing order response from Binance API.

        Raises:
            BinanceClientError: If order placement fails.
        """
        try:
            logger.debug(
                f"Placing limit order: {side} {quantity} {symbol} @ {price}"
            )

            params = {
                "symbol": symbol,
                "side": side,
                "type": "LIMIT",
                "quantity": quantity,
                "price": price,
                "timeInForce": "GTC",  # Good Till Cancel
            }

            logger.debug(f"Order request parameters: {params}")

            response = self.client.new_order(**params)

            logger.info(
                f"Limit order placed successfully: "
                f"Symbol={symbol}, Side={side}, Quantity={quantity}, "
                f"Price={price}, OrderID={response.get('orderId')}"
            )

            return response

        except BinanceClientError as e:
            error_msg = f"Binance API error: {str(e)}"
            logger.error(error_msg)
            raise BinanceClientError(error_msg)
        except Exception as e:
            error_msg = f"Unexpected error placing limit order: {str(e)}"
            logger.error(error_msg)
            raise BinanceClientError(error_msg)

    def get_order_status(self, symbol: str, order_id: int) -> Dict[str, Any]:
        """
        Get order status.

        Args:
            symbol: Trading symbol.
            order_id: Order ID.

        Returns:
            Dict containing order details.

        Raises:
            BinanceClientError: If request fails.
        """
        try:
            logger.debug(f"Fetching order status: {symbol} OrderID={order_id}")

            response = self.client.query_order(symbol=symbol, orderId=order_id)

            logger.info(
                f"Order status fetched: {symbol} OrderID={order_id} "
                f"Status={response.get('status')}"
            )

            return response

        except BinanceClientError as e:
            error_msg = f"Binance API error: {str(e)}"
            logger.error(error_msg)
            raise BinanceClientError(error_msg)
        except Exception as e:
            error_msg = f"Unexpected error fetching order status: {str(e)}"
            logger.error(error_msg)
            raise BinanceClientError(error_msg)
