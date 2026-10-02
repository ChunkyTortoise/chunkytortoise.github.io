"""Check hiring-page destinations as an anonymous visitor, using only stdlib."""

from concurrent.futures import ThreadPoolExecutor
from html.parser import HTMLParser
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import unquote, urlsplit
from urllib.request import Request, urlopen
import argparse
import time

ROOT = Path(__file__).resolve().parents[1]
PAGES = ("index.html", "about.html", "projects.html", "blog.html")


class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.hrefs = []

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            href = dict(attrs).get("href")
            if href:
                self.hrefs.append(href)


def collect_links(root, pages):
    external, errors = set(), []
    for page in pages:
        parser = Links()
        parser.feed((root / page).read_text())
        for href in parser.hrefs:
            url = urlsplit(href)
            if url.scheme in ("http", "https"):
                external.add(href)
            elif not url.scheme and not url.netloc:
                destination = (
                    root / unquote(url.path.lstrip("/"))
                    if url.path.startswith("/")
                    else (root / page).parent / unquote(url.path)
                )
                if url.path and not destination.exists():
                    errors.append(f"{page}: missing {href}")
    return sorted(external), errors


def fetch_once(url, opener):
    """Return (error or None, retryable)."""
    try:
        request = Request(url, headers={"User-Agent": "portfolio-link-check/1.0"})
        with opener(request, timeout=20) as response:
            status = response.status
            final = urlsplit(response.geturl())
            if status != 200:
                return f"{url}: HTTP {status}", status >= 500
            if "/auth/" in final.path or "/login" in final.path:
                return f"{url}: redirects to login ({response.geturl()})", False
    except HTTPError as error:
        message = f"{url}: {error}"
        retryable = error.code >= 500 or error.code == 429
        error.close()
        return message, retryable
    except (URLError, TimeoutError, OSError) as error:
        return f"{url}: {error}", True
    return None, False


def check_url(url, opener=urlopen, attempts=3, sleep=time.sleep):
    """Retry server errors and timeouts so a brief GitHub outage is not a broken link."""
    for attempt in range(attempts):
        error, retryable = fetch_once(url, opener)
        if error is None or not retryable:
            return error
        if attempt + 1 < attempts:
            sleep(2 ** (attempt + 1))
    return error


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--offline", action="store_true", help="Check local files only")
    args = parser.parse_args()
    urls, errors = collect_links(ROOT, PAGES)
    if not args.offline:
        with ThreadPoolExecutor(max_workers=4) as pool:
            errors.extend(result for result in pool.map(check_url, urls) if result)
    for error in errors:
        print(error)
    print(
        f"{len(PAGES)} hiring pages, {len(urls)} external destinations, {len(errors)} failures"
    )
    return bool(errors)


if __name__ == "__main__":
    raise SystemExit(main())
