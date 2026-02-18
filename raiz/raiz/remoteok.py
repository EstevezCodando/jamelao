import json

import bs4


def find_title(html):
    soup = bs4.BeautifulSoup(html, 'html.parser')
    vs = soup.select("[itemprop=\"hiringOrganization\"] [itemprop=\"name\"]")
    return list(map(lambda el: el.text.strip(), vs))

def ro_extract(soup):
    return map(lambda el: {
        "title": el["title"],
        "company": el["hiringOrganization"]["name"],
        "link": el["hiringOrganization"]["sameAs"],
        "description": el["description"],
    }, map(
        lambda el: json.loads(el.text),
        soup.select("script[type='application/ld+json']")
    )
               )
