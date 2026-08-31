import asyncio
from src.ingestion import run_ingestion

if __name__ == "__main__":
    asyncio.run(run_ingestion())