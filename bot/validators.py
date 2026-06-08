"""Input validation module."""

from typing import Tuple, Optional
from bot.logging_config import LoggerSetup

logger = LoggerSetup.get_logger(__name__)


class ValidationError(Exception):
    """Custom exception for validation errors."""

    pass


class OrderValidator:
    """Validator for order parameters."""

    VALID_SIDES = {"BUY", "SELL"}
    VALID_TYPES = {"MARKET", "LIMIT"}
    MIN_QUANTITY = 0.001
    MIN_PRICE = 0.01

    @staticmethod
    def validate_symbol(symbol: str) -> None:
        """
        Validate trading symbol.

        Args:
            symbol: Trading symbol (e.g., BTCUSDT).

        Raises:
            ValidationError: If symbol is invalid.
        """
        if not symbol:
            error_msg = "Symbol cannot be empty"
            logger.warning(f"Validation failed: {error_msg}")
            raise ValidationError(error_msg)

        if not isinstance(symbol, str):
            error_msg = "Symbol must be a string"
            logger.warning(f"Validation failed: {error_msg}")
            raise ValidationError(error_msg)

        symbol = symbol.strip().upper()
        if len(symbol) < 2:
            error_msg = "Symbol must be at least 2 characters"
            logger.warning(f"Validation failed: {error_msg}")
            raise ValidationError(error_msg)

        logger.debug(f"Symbol validation passed: {symbol}")

    @staticmethod
    def validate_side(side: str) -> None:
        """
        Validate order side.

        Args:
            side: Order side (BUY or SELL).

        Raises:
            ValidationError: If side is invalid.
        """
        if not side:
            error_msg = "Side cannot be empty"
            logger.warning(f"Validation failed: {error_msg}")
            raise ValidationError(error_msg)

        side_upper = side.strip().upper()
        if side_upper not in OrderValidator.VALID_SIDES:
            error_msg = f"Side must be BUY or SELL, got: {side}"
            logger.warning(f"Validation failed: {error_msg}")
            raise ValidationError(error_msg)

        logger.debug(f"Side validation passed: {side_upper}")

    @staticmethod
    def validate_order_type(order_type: str) -> None:
        """
        Validate order type.

        Args:
            order_type: Order type (MARKET or LIMIT).

        Raises:
            ValidationError: If order type is invalid.
        """
        if not order_type:
            error_msg = "Order type cannot be empty"
            logger.warning(f"Validation failed: {error_msg}")
            raise ValidationError(error_msg)

        order_type_upper = order_type.strip().upper()
        if order_type_upper not in OrderValidator.VALID_TYPES:
            error_msg = f"Order type must be MARKET or LIMIT, got: {order_type}"
            logger.warning(f"Validation failed: {error_msg}")
            raise ValidationError(error_msg)

        logger.debug(f"Order type validation passed: {order_type_upper}")

    @staticmethod
    def validate_quantity(quantity: float) -> None:
        """
        Validate order quantity.

        Args:
            quantity: Order quantity.

        Raises:
            ValidationError: If quantity is invalid.
        """
        try:
            qty = float(quantity)
        except (ValueError, TypeError):
            error_msg = f"Quantity must be a positive number, got: {quantity}"
            logger.warning(f"Validation failed: {error_msg}")
            raise ValidationError(error_msg)

        if qty <= 0:
            error_msg = f"Quantity must be positive, got: {qty}"
            logger.warning(f"Validation failed: {error_msg}")
            raise ValidationError(error_msg)

        if qty < OrderValidator.MIN_QUANTITY:
            error_msg = (
                f"Quantity must be at least {OrderValidator.MIN_QUANTITY}, "
                f"got: {qty}"
            )
            logger.warning(f"Validation failed: {error_msg}")
            raise ValidationError(error_msg)

        logger.debug(f"Quantity validation passed: {qty}")

    @staticmethod
    def validate_price(price: Optional[float], order_type: str) -> None:
        """
        Validate order price.

        Args:
            price: Order price.
            order_type: Order type (MARKET or LIMIT).

        Raises:
            ValidationError: If price is invalid.
        """
        order_type_upper = order_type.strip().upper()

        if order_type_upper == "LIMIT":
            if price is None:
                error_msg = "Price is mandatory for LIMIT orders"
                logger.warning(f"Validation failed: {error_msg}")
                raise ValidationError(error_msg)

            try:
                price_val = float(price)
            except (ValueError, TypeError):
                error_msg = f"Price must be a positive number, got: {price}"
                logger.warning(f"Validation failed: {error_msg}")
                raise ValidationError(error_msg)

            if price_val <= 0:
                error_msg = f"Price must be positive, got: {price_val}"
                logger.warning(f"Validation failed: {error_msg}")
                raise ValidationError(error_msg)

            if price_val < OrderValidator.MIN_PRICE:
                error_msg = (
                    f"Price must be at least {OrderValidator.MIN_PRICE}, "
                    f"got: {price_val}"
                )
                logger.warning(f"Validation failed: {error_msg}")
                raise ValidationError(error_msg)

            logger.debug(f"Price validation passed: {price_val}")

    @staticmethod
    def validate_all(
        symbol: str,
        side: str,
        order_type: str,
        quantity: float,
        price: Optional[float] = None,
    ) -> Tuple[str, str, str, float, Optional[float]]:
        """
        Validate all order parameters.

        Args:
            symbol: Trading symbol.
            side: Order side (BUY or SELL).
            order_type: Order type (MARKET or LIMIT).
            quantity: Order quantity.
            price: Order price (optional for MARKET orders).

        Returns:
            Tuple of normalized parameters (symbol, side, order_type, quantity, price).

        Raises:
            ValidationError: If any parameter is invalid.
        """
        OrderValidator.validate_symbol(symbol)
        OrderValidator.validate_side(side)
        OrderValidator.validate_order_type(order_type)
        OrderValidator.validate_quantity(quantity)
        OrderValidator.validate_price(price, order_type)

        # Normalize values
        symbol_norm = symbol.strip().upper()
        side_norm = side.strip().upper()
        order_type_norm = order_type.strip().upper()
        quantity_norm = float(quantity)
        price_norm = float(price) if price is not None else None

        logger.info(
            f"All validations passed: {symbol_norm} {side_norm} "
            f"{order_type_norm} {quantity_norm} {price_norm}"
        )

        return symbol_norm, side_norm, order_type_norm, quantity_norm, price_norm
