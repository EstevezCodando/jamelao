import json

def first_request(_):
    return dict(
        request_method="GET",
        expected_status=200,
        server_name="es.indeed.com",
        url="/jobs",
        query_string="q=software&l=Madrid%2C%20Madrid%20provincia&radius=25&from=searchOnDesktopSerp",
        headers={
            "User-Agent": "https://es.indeed.com/jobs?q=software&l=Madrid%2C%20Madrid%20provincia&radius=25&from=searchOnDesktopSerp",
            "Referer": "https://es.indeed.com/jobs?q=software&l=Madrid%2C+Madrid+provincia&radius=25&from=searchOnDesktopSerp&vjk=0992e01f161cc4ec",
            "Alt-Used": "es.indeed.com",

        },
    )

def extract(soup):
    return []


def next_request(request, offset):
    query_string = f"tags=software&action=get_jobs&premium=0&pagination=1&offset={offset}"
    return dict(**request, query_string=query_string)
