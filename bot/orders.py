"""Order execution business logic."""

from typing import Dict, Any, Optional
from bot.client import BinanceFuturesClient, BinanceClientError
from bot.validators import OrderValidator, ValidationError
from bot.logging_config import LoggerSetup

logger = LoggerSetup.get_logger(__name__)


class OrderExecutionError(Exception):
    """Custom exception for order execution errors."""

    pass


class OrderExecutor:
    """Execute trading orders with validation and error handling."""

    def __init__(self) -> None:
        """Initialize order executor with Binance client."""
        try:
            self.client = BinanceFuturesClient()
        except BinanceClientError as e:
            error_msg = f"Failed to initialize order executor: {str(e)}"
            logger.error(error_msg)
            raise OrderExecutionError(error_msg)

    def place_market_order(
        self, symbol: str, side: str, quantity: float
    ) -> Dict[str, Any]:
        """
        Execute a market order with validation.

        Args:
            symbol: Trading symbol.
            side: Order side (BUY or SELL).
            quantity: Order quantity.

        Returns:
            Dict containing order response.

        Raises:
            ValidationError: If validation fails.
            OrderExecutionError: If order execution fails.
        """
        logger.info(
            f"Executing market order: {side} {quantity} {symbol}"
        )

        try:
            # Validate inputs
            symbol, side, _, quantity, _ = OrderValidator.validate_all(
                symbol=symbol,
                side=side,
                order_type="MARKET",
                quantity=quantity,
                price=None,
            )

            # Place order via client
            response = self.client.place_market_order(
                symbol=symbol, side=side, quantity=quantity
            )

            logger.info(
                f"Market order executed successfully: "
                f"OrderID={response.get('orderId')}"
            )

            return response

        except ValidationError as e:
            error_msg = f"Market order validation failed: {str(e)}"
            logger.error(error_msg)
            raise OrderExecutionError(error_msg)
        except BinanceClientError as e:
            error_msg = f"Market order execution failed: {str(e)}"
            logger.error(error_msg)
            raise OrderExecutionError(error_msg)
        except Exception as e:
            error_msg = f"Unexpected error in market order: {str(e)}"
            logger.error(error_msg)
            raise OrderExecutionError(error_msg)

    def place_limit_order(
        self, symbol: str, side: str, quantity: float, price: float
    ) -> Dict[str, Any]:
        """
        Execute a limit order with validation.

        Args:
            symbol: Trading symbol.
            side: Order side (BUY or SELL).
            quantity: Order quantity.
            price: Order price.

        Returns:
            Dict containing order response.

        Raises:
            ValidationError: If validation fails.
            OrderExecutionError: If order execution fails.
        """
        logger.info(
            f"Executing limit order: {side} {quantity} {symbol} @ {price}"
        )

        try:
            # Validate inputs
            symbol, side, _, quantity, price = OrderValidator.validate_all(
                symbol=symbol,
                side=side,
                order_type="LIMIT",
                quantity=quantity,
                price=price,
            )

            # Place order via client
            response = self.client.place_limit_order(
                symbol=symbol, side=side, quantity=quantity, price=price
            )

            logger.info(
                f"Limit order executed successfully: "
                f"OrderID={response.get('orderId')}"
            )

            return response

        except ValidationError as e:
            error_msg = f"Limit order validation failed: {str(e)}"
            logger.error(error_msg)
            raise OrderExecutionError(error_msg)
        except BinanceClientError as e:
            error_msg = f"Limit order execution failed: {str(e)}"
            logger.error(error_msg)
            raise OrderExecutionError(error_msg)
        except Exception as e:
            error_msg = f"Unexpected error in limit order: {str(e)}"
            logger.error(error_msg)
            raise OrderExecutionError(error_msg)

    @staticmethod
    def format_order_response(response: Dict[str, Any]) -> Dict[str, str]:
        """
        Format order response for display.

        Args:
            response: Raw order response from API.

        Returns:
            Dict with formatted order information.
        """
        return {
            "order_id": str(response.get("orderId", "N/A")),
            "status": response.get("status", "N/A"),
            "executed_quantity": str(response.get("executedQty", "0")),
            "average_price": str(response.get("avgPrice", "N/A")),
            "symbol": response.get("symbol", "N/A"),
            "side": response.get("side", "N/A"),
            "order_type": response.get("type", "N/A"),
            "quantity": str(response.get("origQty", "0")),
            "price": str(response.get("price", "N/A")),
        }
