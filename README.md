# Binance Futures Testnet Trading Bot

A production-quality Python CLI application for placing orders on Binance Futures Testnet (USDT-M Futures). This project implements comprehensive validation, logging, and error handling for reliable trading operations.

## Table of Contents

- [Features](#features)
- [Architecture](#architecture)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Setup Guide](#setup-guide)
  - [Step 1: Install Python](#step-1-install-python)
  - [Step 2: Clone/Setup Project](#step-2-clonesset-up-project)
  - [Step 3: Create Virtual Environment](#step-3-create-virtual-environment)
  - [Step 4: Install Dependencies](#step-4-install-dependencies)
  - [Step 5: Create Binance Testnet API Keys](#step-5-create-binance-testnet-api-keys)
  - [Step 6: Configure Environment](#step-6-configure-environment)
  - [Step 7: Verify Setup](#step-7-verify-setup)
- [How to Run](#how-to-run)
- [Command Examples](#command-examples)
- [Output Examples](#output-examples)
- [Logging](#logging)
- [Validation Rules](#validation-rules)
- [Error Handling](#error-handling)
- [API Documentation](#api-documentation)
- [Troubleshooting](#troubleshooting)
- [Assumptions](#assumptions)

---

## Features

✅ **MARKET Orders** - Execute immediate orders at current market price
✅ **LIMIT Orders** - Place orders at specified price levels
✅ **BUY/SELL Support** - Full position opening and closing
✅ **Binance Futures Testnet** - Safe testing environment (no real funds)
✅ **Comprehensive Logging** - Rotating file logs with detailed information
✅ **Input Validation** - Complete parameter validation with clear error messages
✅ **Error Handling** - Graceful failure handling with user-friendly error messages
✅ **Rich CLI Output** - Colored console output with formatted tables
✅ **Type Hints** - Full Python type annotations for code clarity
✅ **Production Quality** - PEP8 formatting, docstrings, and modular design

---

## Architecture

### Design Principles

- **Separation of Concerns**: Each module has a single responsibility
- **Modular Structure**: Easy to test, extend, and maintain
- **Error Isolation**: All errors caught and logged before user display
- **Configuration Management**: Centralized environment handling
- **Validation Layer**: All inputs validated before API calls

### Module Responsibilities

| Module | Responsibility |
|--------|-----------------|
| `config.py` | Load and validate environment variables |
| `logging_config.py` | Setup centralized logging with rotation |
| `validators.py` | Validate all CLI inputs |
| `client.py` | Binance API wrapper and HTTP communication |
| `orders.py` | Business logic for order execution |
| `cli.py` | CLI interface and user output |

---

## Project Structure

```
trading_bot/
├── bot/
│   ├── __init__.py              # Package initialization
│   ├── client.py                # Binance Futures client wrapper
│   ├── orders.py                # Order execution logic
│   ├── validators.py            # Input validation
│   ├── config.py                # Configuration management
│   └── logging_config.py         # Centralized logging setup
├── logs/                         # Log files (created at runtime)
│   └── trading_bot.log          # Main application log
├── cli.py                        # CLI entry point
├── requirements.txt              # Python dependencies
├── .env.example                  # Environment variables template
├── .env                          # Environment variables (DO NOT COMMIT)
├── .gitignore                    # Git ignore rules
└── README.md                     # This file
```

---

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Internet connection (for package downloads and API calls)
- Binance Futures Testnet account (free)

### Step 1: Install Python

**Windows:**
```bash
# Download from https://www.python.org/downloads/
# Run installer and ensure "Add Python to PATH" is checked
python --version  # Verify installation
```

**macOS:**
```bash
brew install python3
python3 --version  # Verify installation
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get update
sudo apt-get install python3 python3-pip
python3 --version  # Verify installation
```

### Step 2: Clone/Setup Project

```bash
# Navigate to your projects directory
cd /path/to/projects

# If from GitHub (replace with your repo)
git clone https://github.com/yourusername/binance-futures-bot.git
cd binance-futures-bot

# Or if local, just navigate to the project directory
cd trading_bot
```

### Step 3: Create Virtual Environment

**Windows:**
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate

# You should see (venv) prefix in terminal
```

**macOS/Linux:**
```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# You should see (venv) prefix in terminal
```

### Step 4: Install Dependencies

```bash
# With virtual environment activated
pip install -r requirements.txt

# Verify installation
pip list
```

Expected packages:
- python-binance (>=1.0.19)
- python-dotenv (>=1.0.0)
- rich (>=13.7.0)
- requests (>=2.31.0)

### Step 5: Create Binance Testnet API Keys

1. **Go to Binance Testnet Website:**
   - Visit: https://testnet.binancefuture.com/

2. **Create or Login to Account:**
   - Sign up for a new testnet account (free)
   - Or login with existing Binance account

3. **Generate API Keys:**
   - Click on account icon (top-right)
   - Select "API Management" or "API Key"
   - Create new key for "Futures Trading"
   - Label: "Trading Bot" (optional)
   - Restrictions: Enable "Futures Trading"
   - Save API Key and Secret securely

4. **Copy Your Credentials:**
   ```
   API Key:    Your_API_Key_Here_123abc...
   Secret:     Your_API_Secret_Here_xyz789...
   ```

### Step 6: Configure Environment

1. **Create .env file:**
   ```bash
   # Copy the example file
   # Windows:
   copy .env.example .env
   
   # macOS/Linux:
   cp .env.example .env
   ```

2. **Edit .env file:**
   ```bash
   # Open in your text editor
   # Windows: notepad .env
   # macOS/Linux: nano .env
   
   # Add your credentials:
   BINANCE_API_KEY=your_actual_api_key_here
   BINANCE_API_SECRET=your_actual_api_secret_here
   ```

3. **Save the file** (do NOT commit to git)

### Step 7: Verify Setup

```bash
# Test import without errors
python -c "from bot.config import Config; print('✓ Setup verified')"

# Should print: ✓ Setup verified
```

---

## How to Run

### Basic Command Format

```bash
python cli.py --symbol SYMBOL --side SIDE --type TYPE --quantity QUANTITY [--price PRICE]
```

### Parameters

| Parameter | Required | Values | Example |
|-----------|----------|--------|---------|
| `--symbol` | Yes | Any Binance symbol | BTCUSDT, ETHUSDT |
| `--side` | Yes | BUY, SELL | BUY |
| `--type` | Yes | MARKET, LIMIT | MARKET |
| `--quantity` | Yes | Positive number | 0.001, 1.5 |
| `--price` | Conditional | Positive number | 100000, 2500.50 |

**Note:** `--price` is mandatory for LIMIT orders, optional for MARKET orders.

---

## Command Examples

### Example 1: Market Buy Order

```bash
python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001
```

**What happens:**
- Buys 0.001 BTC at current market price
- Order executes immediately at market rate
- Fastest execution, price may vary

### Example 2: Market Sell Order

```bash
python cli.py --symbol ETHUSDT --side SELL --type MARKET --quantity 1.0
```

**What happens:**
- Sells 1 ETH at current market price
- Closes or reduces position
- Immediate execution

### Example 3: Limit Buy Order

```bash
python cli.py --symbol BTCUSDT --side BUY --type LIMIT --quantity 0.001 --price 40000
```

**What happens:**
- Places order to buy 0.001 BTC at exactly 40000 USDT
- Waits for price to reach limit
- May not execute if price never hits target

### Example 4: Limit Sell Order

```bash
python cli.py --symbol BNBUSDT --side SELL --type LIMIT --quantity 10 --price 500
```

**What happens:**
- Places order to sell 10 BNB at exactly 500 USDT each
- Sits in order book until filled
- Partial fills possible

### Example 5: With Additional Symbols

```bash
# SOL trading
python cli.py --symbol SOLUSDT --side BUY --type MARKET --quantity 10

# XRP trading  
python cli.py --symbol XRPUSDT --side SELL --type LIMIT --quantity 100 --price 2.5
```

---

## Output Examples

### Successful Market Order

```
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃                    Order Summary                           ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ Parameter           │ Value                                 │
├─────────────────────┼───────────────────────────────────────┤
│ Symbol              │ BTCUSDT                               │
│ Side                │ BUY                                   │
│ Order Type          │ MARKET                                │
│ Quantity            │ 0.001                                 │
└─────────────────────┴───────────────────────────────────────┘

Placing order...

┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃                  ✓ Order Placed                            ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│                                                             │
│ ✓ SUCCESS                                                  │
│                                                             │
│ Order ID: 123456789                                        │
│ Order has been placed on Binance Futures Testnet          │
│                                                             │
└─────────────────────────────────────────────────────────────┘

┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃                   Order Details                            ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ Field               │ Value                                 │
├─────────────────────┼───────────────────────────────────────┤
│ Order ID            │ 123456789                             │
│ Status              │ FILLED                                │
│ Symbol              │ BTCUSDT                               │
│ Side                │ BUY                                   │
│ Type                │ MARKET                                │
│ Quantity            │ 0.001                                 │
│ Executed Quantity   │ 0.001                                 │
│ Average Price       │ 43250.50                              │
└─────────────────────┴───────────────────────────────────────┘
```

### Validation Error

```
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃                  ✗ Order Failed                            ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│                                                             │
│ ✗ FAILURE                                                  │
│                                                             │
│ Validation Error: Price is mandatory for LIMIT orders     │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## Logging

### Log File Location

All logs are written to: `logs/trading_bot.log`

### Log Rotation

- **Max File Size:** 10 MB
- **Backup Count:** 5 files
- **Naming:** `trading_bot.log.1`, `trading_bot.log.2`, etc.

When main log reaches 10MB, it's renamed and a new one starts.

### Log Format

```
YYYY-MM-DD HH:MM:SS - LEVEL - MODULE - MESSAGE
```

### Log Levels

- **DEBUG** - Detailed diagnostic information
- **INFO** - General informational messages
- **WARNING** - Warning messages
- **ERROR** - Error messages with stack traces

### Example Log Entries

```
2026-01-15 14:30:22 - INFO - client - Binance Futures Testnet client initialized successfully
2026-01-15 14:30:23 - DEBUG - validators - Symbol validation passed: BTCUSDT
2026-01-15 14:30:23 - INFO - orders - Executing market order: BUY 0.001 BTCUSDT
2026-01-15 14:30:24 - DEBUG - client - Order request parameters: {'symbol': 'BTCUSDT', 'side': 'BUY', 'type': 'MARKET', 'quantity': 0.001}
2026-01-15 14:30:25 - INFO - client - Market order placed successfully: Symbol=BTCUSDT, Side=BUY, Quantity=0.001, OrderID=123456789
```

### Viewing Logs

```bash
# View last 50 lines (Windows PowerShell or Linux)
tail -50 logs/trading_bot.log

# View specific module logs (Windows - use | more or other tools)
grep "client" logs/trading_bot.log

# View error logs only
grep "ERROR" logs/trading_bot.log

# Count total log entries
wc -l logs/trading_bot.log
```

---

## Validation Rules

### Symbol Validation
- ✓ Cannot be empty
- ✓ Must be a string
- ✓ Minimum 2 characters
- ✓ Converted to uppercase

### Side Validation
- ✓ Must be exactly: `BUY` or `SELL`
- ✓ Case-insensitive (BUY, buy, Buy all work)
- ✓ Cannot be empty

### Order Type Validation
- ✓ Must be exactly: `MARKET` or `LIMIT`
- ✓ Case-insensitive
- ✓ Cannot be empty

### Quantity Validation
- ✓ Must be a positive number
- ✓ Minimum: 0.001
- ✓ Cannot be zero or negative
- ✓ Must be numeric

### Price Validation
- ✓ Required for LIMIT orders only
- ✓ Must be a positive number
- ✓ Minimum: 0.01
- ✓ Cannot be zero or negative
- ✓ Must be numeric

---

## Error Handling

### Input Validation Errors

```bash
# Missing required argument
$ python cli.py --symbol BTCUSDT
error: the following arguments are required: --side, --type, --quantity

# Invalid side
$ python cli.py --symbol BTCUSDT --side INVALID --type MARKET --quantity 0.001
Validation Error: Side must be BUY or SELL, got: INVALID

# Missing price for LIMIT order
$ python cli.py --symbol BTCUSDT --side BUY --type LIMIT --quantity 0.001
Price is mandatory for LIMIT orders
```

### API Errors

```bash
# Invalid symbol on Binance
Validation Error: Binance API error: Invalid symbol INVALIDUSDT

# Authentication failure
Binance API error: Invalid API key
```

### Network Errors

```bash
# Connection timeout
Unexpected error: Connection timeout - Check your internet connection

# Unable to reach server
Unexpected error: Failed to connect to testnet.binancefuture.com
```

### User-Friendly Messages

All errors show:
1. ✗ FAILURE indicator
2. Clear error message
3. Logged details for debugging
4. Exit code 1 for script integration

---

## API Documentation

### Binance Futures Testnet

**Base URL:** https://testnet.binancefuture.com

**Order Types:**
- MARKET - Immediate execution at market price
- LIMIT - Execution at specific price (GTC - Good Till Cancel)

**Order Sides:**
- BUY - Open long position or close short
- SELL - Open short position or close long

**Response Fields:**

```json
{
  "orderId": 123456789,
  "symbol": "BTCUSDT",
  "status": "FILLED",
  "side": "BUY",
  "type": "MARKET",
  "origQty": "0.001",
  "executedQty": "0.001",
  "price": "43250.50",
  "avgPrice": "43250.50"
}
```

### python-binance Library

The application uses `python-binance` for API interaction.

**Documentation:** https://python-binance.readthedocs.io/

**Key Methods Used:**
- `UMFutures.new_order()` - Place new order
- `UMFutures.query_order()` - Query order status

---

## Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'binance'"

**Solution:**
```bash
# Ensure virtual environment is activated
# Then reinstall dependencies
pip install -r requirements.txt

# Verify installation
python -c "import binance; print(binance.__version__)"
```

### Issue: "No module named 'bot'"

**Solution:**
```bash
# Ensure you're in the correct directory
pwd  # Check current directory

# Should be in trading_bot/ root directory
# Should see cli.py, bot/, requirements.txt

# Run from project root:
python cli.py --help
```

### Issue: "BINANCE_API_KEY not found in environment"

**Solution:**
```bash
# Check .env file exists
ls -la .env  # macOS/Linux or dir .env (Windows)

# Verify contents (don't share this!)
cat .env  # macOS/Linux or type .env (Windows)

# Should show:
# BINANCE_API_KEY=your_key
# BINANCE_API_SECRET=your_secret

# Ensure no quotes around values:
# INCORRECT: BINANCE_API_KEY="your_key"
# CORRECT:   BINANCE_API_KEY=your_key
```

### Issue: "Invalid API key"

**Solution:**
```bash
1. Check API key is correct (copy from Binance again)
2. Verify key is for Testnet, not Mainnet
3. Check API key has "Futures Trading" permission
4. Restart terminal to reload .env
5. Check logs for exact error: cat logs/trading_bot.log
```

### Issue: "Invalid symbol BTCUSDT"

**Solution:**
```bash
# Symbol format is correct. This usually means:
1. API key doesn't have permission for this symbol
2. Symbol not trading on testnet
3. Typo in symbol

# Try with common testnet symbols:
python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001
python cli.py --symbol ETHUSDT --side BUY --type MARKET --quantity 0.01
python cli.py --symbol BNBUSDT --side BUY --type MARKET --quantity 0.1
```

### Issue: "Quantity must be at least 0.001"

**Solution:**
```bash
# Quantity too small. Increase quantity:
# INCORRECT: --quantity 0.0001
# CORRECT:   --quantity 0.001

python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001
```

### Issue: Order placement hangs/takes too long

**Solution:**
```bash
# Check internet connection
ping google.com

# Check if testnet is accessible
curl https://testnet.binancefuture.com

# If still hanging, Ctrl+C to cancel and try again
# Check logs: tail logs/trading_bot.log
```

### Issue: No logs being created

**Solution:**
```bash
# Check logs directory exists
ls -d logs/  # macOS/Linux or dir logs (Windows)

# If not, create it:
mkdir logs  # macOS/Linux or md logs (Windows)

# Run command again to generate logs
python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001

# Check log file
cat logs/trading_bot.log
```

---

## Assumptions

### Technical Assumptions

1. **Binance Futures Testnet is online**
   - Application requires live connection to testnet.binancefuture.com
   - If testnet is down, orders will fail with connection errors

2. **Python 3.8+ is installed**
   - Features used are compatible with Python 3.8+
   - Tested on Python 3.9, 3.10, 3.11

3. **Virtual environment best practice**
   - Project assumes use of virtual environment
   - Ensures dependency isolation and reproducibility

4. **Fresh API keys for security**
   - Each user should generate their own testnet API keys
   - Keys are never shared or hardcoded

### Functional Assumptions

1. **Testnet has sufficient balance**
   - Testnet accounts start with test USDT
   - User responsible for maintaining testnet balance

2. **Symbols are valid Binance Futures pairs**
   - Bot validates symbol format but depends on Binance's symbol list
   - Popular pairs: BTCUSDT, ETHUSDT, BNBUSDT, ADAUSDT, etc.

3. **Network connectivity is stable**
   - Bot makes live API calls
   - Temporary network issues may cause timeouts

4. **No concurrent order placement**
   - Application processes one order at a time
   - Not designed for high-frequency trading
   - No rate limiting implemented (assumed under Binance limits)

### Behavioral Assumptions

1. **Order details are final**
   - No order modification or cancellation implemented
   - Once placed, order follows Binance rules

2. **Market orders execute immediately (testnet)**
   - Testnet provides instant fills on market orders
   - Mainnet may have slippage/delays

3. **LIMIT orders may not fill**
   - Limit orders placed at order book
   - May remain pending if price never reached

4. **User accepts testnet risks**
   - Testnet data may be reset
   - Testnet orders don't involve real funds
   - For learning/testing purposes only

---

## Security Notes

⚠️ **IMPORTANT SECURITY CONSIDERATIONS**

1. **Never commit .env file to git**
   - `.gitignore` prevents this by default
   - Your API keys would be exposed

2. **API Keys are sensitive**
   - Treat like passwords
   - Rotate if accidentally exposed
   - Use testnet keys for testing (lower risk)

3. **Use Testnet for Development**
   - Testnet uses practice funds only
   - No real money at risk
   - Safe environment for testing

4. **Limit API Key Permissions**
   - Enable only "Futures Trading"
   - Disable withdrawal permissions
   - IP whitelist if available (testnet: N/A)

5. **Monitor Logs**
   - Check `logs/trading_bot.log` regularly
   - Look for unauthorized access attempts
   - Report suspicious activity to Binance

---

## Support & Maintenance

### Updating Dependencies

```bash
# Update to latest compatible versions
pip install --upgrade -r requirements.txt

# Check for outdated packages
pip list --outdated
```

### Running Tests (if implemented)

```bash
pytest tests/
pytest --cov=bot tests/
```

### Code Quality

```bash
# Format code (install black first)
pip install black
black bot/ cli.py

# Check linting (install flake8)
pip install flake8
flake8 bot/ cli.py
```

### Version Info

```bash
python cli.py --version
```

---

## Contact & Contribution

For issues or improvements:
- Check logs in `logs/trading_bot.log`
- Review README troubleshooting section
- Verify API credentials are correct
- Ensure testnet is accessible

---

**Last Updated:** January 2026
**Version:** 1.0.0
**Status:** Production Ready
