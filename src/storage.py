import os
import time
import pandas as pd


def flush_to_parquet(buffer, out_dir="data"):
    """
    Writes a list of dict records to a timestamped Parquet file.
    Called once the in-memory buffer hits its batch size threshold.
    """
    os.makedirs(out_dir, exist_ok=True)
    df = pd.DataFrame(buffer)
    filename = f"{out_dir}/depth_{int(time.time())}.parquet"
    df.to_parquet(filename, engine="pyarrow")
    print(f"Flushed {len(buffer)} rows -> {filename}")