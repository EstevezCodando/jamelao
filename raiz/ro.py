#!/usr/bin/env python

import http.client as hc
import shutil
from pathlib import Path

import bs4


def main():
    has_next = True
    offset = 0
    conn = hc.HTTPSConnection("remoteok.com")
    try:
        while has_next:
            conn.request("GET", f"/?tags=software&action=get_jobs&premium=0&pagination=1&offset={offset}")
            response = conn.getresponse()
            if not (200 == response.status):
                raise RuntimeError("Unexpected status code")
            current_body = Path("data", f"{offset}.html")
            with open(current_body, 'wb') as file:
                shutil.copyfileobj(response, file)
            with open(current_body, 'r') as file:
                soup = bs4.BeautifulSoup(file)
                size = len(soup.select("script[type='application/ld+json']"))
                if size > 0:
                    offset = offset + size
                else:
                    has_next = False

    finally:
        conn.close()


if __name__ == "__main__":
    main()
