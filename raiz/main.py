from bs4 import BeautifulSoup


def find_title(html):
    soup = BeautifulSoup(html, 'html.parser')
    return "Hello World"

## uv run -m unittest

if __name__ == "__main__":
    print("ok!")
