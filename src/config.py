SYMBOL = "btcusdt"
STREAM_TYPE = "depth@100ms"  # will become "depth@100ms" in piece five
WS_URL = f"wss://stream.binance.com:9443/ws/{SYMBOL}@{STREAM_TYPE}"

BATCH_SIZE = 500 #change size back to 500
OUTPUT_DIR = "data"

BACKOFF_START = 1
BACKOFF_MAX = 30