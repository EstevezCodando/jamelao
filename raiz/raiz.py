import http.client
import shutil
import json
from pathlib import Path

from bs4 import BeautifulSoup


def find_title(html):
    soup = BeautifulSoup(html, 'html.parser')
    vs = soup.select("[itemprop=\"hiringOrganization\"] [itemprop=\"name\"]")
    return list(map(lambda el: el.text.strip(), vs))

## uv run -m unittest
## uv run -m raiz

def fetch_to_file(*, server_name, request_method, url, expected_status, filename):
    file_path = Path(filename)
    if file_path.is_file():
        ## Already exists
        return None
    conn = http.client.HTTPSConnection(server_name)
    conn.request(request_method, url)
    response = conn.getresponse()
    if not (expected_status == response.status):
        raise Exception("Unexpected status code")
    with open(filename, 'wb') as file:
        shutil.copyfileobj(response, file)


def ro_extract(soup):
    return map(lambda el: el,
               map(
                   lambda el: json.loads(el.text),
                   soup.select("script[type='application/ld+json']")
               )
               )

if __name__ == "__main__":
    fetch_to_file(
        server_name="remoteok.com",
        request_method="GET",
        url="/?tags=software&action=get_jobs&premium=0&pagination=1&offset=",
        expected_status=200,
        filename="remoteok.html"
    )
    with open("remoteok.html", 'r') as file:
        if not Path("remoteok.jsonl").is_file():
            with open("remoteok.jsonl", "w") as output:
                for v in ro_extract(BeautifulSoup(file, 'html.parser')):
                    output.write(json.dumps({
                        "title": v["title"],
                        "company": v["hiringOrganization"]["name"],
                        "link": v["hiringOrganization"]["sameAs"],
                        "description": v["description"],
                    }))
                    output.write("\n")
