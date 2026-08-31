# src/ingestion.py
import asyncio
import json
import time
import websockets

from src.clock import get_clock_offset
from src.storage import flush_to_parquet
from src.config import WS_URL, BATCH_SIZE, OUTPUT_DIR, BACKOFF_START, BACKOFF_MAX


async def run_ingestion():
    backoff = BACKOFF_START
    buffer = []

    offset = get_clock_offset()
    clock_valid = offset is not None
    if offset is None:
        offset = 0

    while True:
        try:
            async with websockets.connect(WS_URL) as ws:
                print("Connected.")
                backoff = BACKOFF_START
                async for raw_message in ws:
                    received_at = time.time() + offset
                    data = json.loads(raw_message)
                    event_time = data["E"] / 1000

                    buffer.append({
                        "received_at": received_at,
                        "event_time": event_time,
                        "latency_ms": (received_at - event_time) * 1000,
                        "clock_corrected": clock_valid,  # downstream analysis must check this
                        "bids": data["b"],
                        "asks": data["a"],
                    })

                    if len(buffer) >= BATCH_SIZE:
                        flush_to_parquet(buffer, out_dir=OUTPUT_DIR)
                        buffer.clear()
        except (websockets.ConnectionClosed, OSError) as e:
            print(f"Disconnected: {e}. Reconnecting in {backoff}s...")
            await asyncio.sleep(backoff)
            backoff = min(backoff * 2, BACKOFF_MAX)