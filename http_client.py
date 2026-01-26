import time

import requests
from flask import current_app


def timed_get(url, **kwargs):
    start = time.perf_counter()

    # kwargs.setdefault("timeout", 2.5)
    resp = requests.get(url, **kwargs)

    duration = (time.perf_counter() - start) * 1000
    current_app.logger.info(f"upstream_time_ms={duration:.1f} url={url}")

    return resp
