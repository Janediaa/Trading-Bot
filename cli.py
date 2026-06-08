"""Command-line interface for Binance Futures Trading Bot."""

import argparse
import sys
from typing import Optional
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from bot.orders import OrderExecutor, OrderExecutionError
from bot.validators import ValidationError
from bot.logging_config import LoggerSetup

logger = LoggerSetup.get_logger(__name__)
console = Console()


def create_parser() -> argparse.ArgumentParser:
    """
    Create and configure argument parser.

    Returns:
        argparse.ArgumentParser: Configured parser.
    """
    parser = argparse.ArgumentParser(
        prog="Binance Futures Trading Bot",
        description="Place orders on Binance Futures Testnet",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001
  python cli.py --symbol BTCUSDT --side SELL --type LIMIT --quantity 0.001 --price 105000
        """,
    )

    parser.add_argument(
        "--symbol",
        required=True,
        help="Trading symbol (e.g., BTCUSDT, ETHUSDT)",
    )

    parser.add_argument(
        "--side",
        required=True,
        choices=["BUY", "SELL"],
        help="Order side: BUY or SELL",
    )

    parser.add_argument(
        "--type",
        required=True,
        choices=["MARKET", "LIMIT"],
        dest="order_type",
        help="Order type: MARKET or LIMIT",
    )

    parser.add_argument(
        "--quantity",
        required=True,
        type=float,
        help="Order quantity",
    )

    parser.add_argument(
        "--price",
        type=float,
        default=None,
        help="Order price (required for LIMIT orders)",
    )

    return parser


def print_order_summary(
    symbol: str,
    side: str,
    order_type: str,
    quantity: float,
    price: Optional[float] = None,
) -> None:
    """
    Print formatted order summary before placement.

    Args:
        symbol: Trading symbol.
        side: Order side.
        order_type: Order type.
        quantity: Order quantity.
        price: Order price (optional).
    """
    table = Table(title="[bold blue]Order Summary[/bold blue]", show_header=False)
    table.add_column("Parameter", style="cyan")
    table.add_column("Value", style="green")

    table.add_row("Symbol", symbol)
    table.add_row("Side", f"[bold]{side}[/bold]")
    table.add_row("Order Type", order_type)
    table.add_row("Quantity", str(quantity))

    if price is not None:
        table.add_row("Price", str(price))

    console.print(table)


def print_order_result(
    success: bool, order_id: Optional[str] = None, message: str = ""
) -> None:
    """
    Print formatted order result.

    Args:
        success: Whether order was successful.
        order_id: Order ID if successful.
        message: Result message.
    """
    if success:
        panel = Panel(
            f"[bold green]✓ SUCCESS[/bold green]\n\n"
            f"Order ID: [bold]{order_id}[/bold]\n"
            f"{message}",
            border_style="green",
            title="[bold green]Order Placed[/bold green]",
        )
    else:
        panel = Panel(
            f"[bold red]✗ FAILURE[/bold red]\n\n{message}",
            border_style="red",
            title="[bold red]Order Failed[/bold red]",
        )

    console.print(panel)


def print_order_details(order_info: dict) -> None:
    """
    Print detailed order information.

    Args:
        order_info: Formatted order information.
    """
    table = Table(
        title="[bold blue]Order Details[/bold blue]", show_header=False
    )
    table.add_column("Field", style="cyan")
    table.add_column("Value", style="yellow")

    table.add_row("Order ID", order_info.get("order_id", "N/A"))
    table.add_row("Status", order_info.get("status", "N/A"))
    table.add_row("Symbol", order_info.get("symbol", "N/A"))
    table.add_row("Side", order_info.get("side", "N/A"))
    table.add_row("Type", order_info.get("order_type", "N/A"))
    table.add_row("Quantity", order_info.get("quantity", "N/A"))
    table.add_row("Executed Quantity", order_info.get("executed_quantity", "N/A"))

    if order_info.get("price") != "N/A":
        table.add_row("Price", order_info.get("price", "N/A"))

    if order_info.get("average_price") != "N/A":
        table.add_row("Average Price", order_info.get("average_price", "N/A"))

    console.print(table)


def main() -> int:
    """
    Main entry point for the CLI.

    Returns:
        int: Exit code (0 for success, 1 for failure).
    """
    parser = create_parser()
    args = parser.parse_args()

    try:
        # Print order summary
        print_order_summary(
            symbol=args.symbol,
            side=args.side,
            order_type=args.order_type,
            quantity=args.quantity,
            price=args.price,
        )

        console.print("\n[bold cyan]Placing order...[/bold cyan]\n")

        # Initialize executor
        executor = OrderExecutor()

        # Execute order
        if args.order_type == "MARKET":
            response = executor.place_market_order(
                symbol=args.symbol,
                side=args.side,
                quantity=args.quantity,
            )
        else:  # LIMIT
            if args.price is None:
                error_msg = "Price is required for LIMIT orders"
                logger.error(error_msg)
                print_order_result(
                    success=False,
                    message=error_msg,
                )
                return 1

            response = executor.place_limit_order(
                symbol=args.symbol,
                side=args.side,
                quantity=args.quantity,
                price=args.price,
            )

        # Format and display result
        order_info = OrderExecutor.format_order_response(response)

        print_order_result(
            success=True,
            order_id=order_info["order_id"],
            message="Order has been placed on Binance Futures Testnet",
        )

        console.print()
        print_order_details(order_info)

        logger.info("Order placement completed successfully")
        return 0

    except ValidationError as e:
        error_msg = f"Validation Error: {str(e)}"
        logger.error(error_msg)
        print_order_result(success=False, message=error_msg)
        return 1

    except OrderExecutionError as e:
        error_msg = f"Order Execution Error: {str(e)}"
        logger.error(error_msg)
        print_order_result(success=False, message=error_msg)
        return 1

    except Exception as e:
        error_msg = f"Unexpected Error: {str(e)}"
        logger.error(error_msg, exc_info=True)
        print_order_result(success=False, message=error_msg)
        return 1


if __name__ == "__main__":
    sys.exit(main())
