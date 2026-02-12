from bs4 import BeautifulSoup


def find_title(html):
    soup = BeautifulSoup(html, 'html.parser')
    print(soup)
    return "Hello World"
