import datetime
import http.client
import json
import pathlib
import shutil

import bs4

import raiz.remoteok as ro


def fetch_to_file(*, server_name, request_method, url, expected_status, filename, query_string):
    file_path = pathlib.Path(filename)
    if file_path.is_file():
        ## Already exists
        return None
    conn = http.client.HTTPSConnection(server_name)
    conn.request(request_method, f"{url}?{query_string}")
    response = conn.getresponse()
    if not (expected_status == response.status):
        raise Exception("Unexpected status code")
    with open(filename, 'wb') as file:
        shutil.copyfileobj(response, file)


def fetch_all(vs):
    for v in vs:
        base_dir = v["base_dir"]
        filename = pathlib.Path(base_dir, "index.html")
        base_dir.mkdir(parents=True, exist_ok=True)
        fetch_to_file(
            ## TODO: Paginacao
            **v["next_request"](dict(server_name=v["server_name"],
                                     request_method="GET",
                                     url="/",
                                     query_string="tags=software&action=get_jobs&premium=0&pagination=1&offset=",
                                     expected_status=200,
                                     filename=filename),
                                0)
        )
        if v["target_file"].is_file():
            return

        with (open(filename, 'r') as raw_htm,
              open(v["target_file"], "w") as target):
            for x in v["extract"](bs4.BeautifulSoup(raw_htm, 'html.parser')):
                target.write(json.dumps(x))
                target.write("\n")


def date_como_nome_de_pasta(now):
    return f"{now}".replace(" ", "T").replace(":", "-")[:16]


def main():
    current_id = date_como_nome_de_pasta(datetime.datetime.now())
    target_dir = pathlib.Path("data", current_id)
    fetches = [
        dict(
            server_name="remoteok.com",
            extract=ro.ro_extract,
            base_dir=pathlib.Path(target_dir, "remoteok"),
            next_request=ro.next_request,
            target_file=pathlib.Path(target_dir, "remoteok", "target.jsonl"),
        ),
        ## TODO: Proxima implementacao
        # dict(
        #     server_name="es.indeed.com",
        #     extract=indeed.extract,
        #     base_dir=pathlib.Path(target_dir, "indeed"),
        #     next_request=indeed.next_request,
        #     target_file=pathlib.Path(target_dir, "indeed", "target.jsonl"),
        # ),
    ]
    fetch_all(fetches)

    print(current_id)


if __name__ == "__main__":
    main()
