# src/clock.py
import logging
import time
import ntplib

NTP_SERVERS = ["pool.ntp.org", "time.google.com", "time.windows.com"]


def get_clock_offset(retries=2, delay=2):
    """
    Returns the offset (in seconds) between real time and this machine's clock,
    tried against several NTP servers in case one is unreachable.
    Returns None if all servers fail — callers must handle this explicitly
    rather than assume a correction was applied.
    """
    client = ntplib.NTPClient()

    for server in NTP_SERVERS:
        for attempt in range(1, retries + 1):
            try:
                response = client.request(server, version=3)
                print(f"Clock offset from {server}: {response.offset*1000:.1f}ms")
                return response.offset
            except Exception as e:
                print(f"NTP request to {server} failed (attempt {attempt}/{retries}): {e}")
                if attempt < retries:
                    time.sleep(delay)

    logging.warning("All NTP servers unreachable. Clock correction unavailable this run.")
    return None