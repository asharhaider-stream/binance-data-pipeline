# Binance Depth Data Pipeline

A low-latency ingestion pipeline for Binance's live order book data. Connects to the public depth websocket stream, timestamps each update on arrival, and persists it to disk as Parquet in efficient batches.

## What it does

- Streams real-time order book depth updates and reconnects automatically with backoff if the connection drops
- Corrects for local clock drift using NTP before computing latency, so the numbers reflect actual network delay rather than an unsynced system clock
- Flags any row where clock correction wasn't available, instead of silently reporting bad timing data as if it were trustworthy
- Batches writes to Parquet rather than hitting disk per message, keeping storage efficient without blocking the read loop

## Structure

src/
config.py # symbol, stream type, batch size
clock.py # NTP offset correction
ingestion.py # websocket connection + reconnect loop
storage.py # Parquet writer
main.py # entry point


## Running it

```bash
pip install -r requirements.txt
python main.py
```

## Part of a series

This is the first piece of a self-directed trading systems build — a matching engine, backtester, and statistical arbitrage strategy follow, each building on what this one produces. Links added here as they're completed.
