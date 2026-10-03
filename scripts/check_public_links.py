"""Check public portfolio-page destinations as an anonymous visitor, using only stdlib."""

from concurrent.futures import ThreadPoolExecutor
from html.parser import HTMLParser
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import unquote, urlsplit
from urllib.request import Request, urlopen
import argparse

ROOT = Path(__file__).resolve().parents[1]
PAGES = (
    "index.html",
    "about.html",
    "projects.html",
    "blog.html",
    "case-studies/docextract.html",
    "case-studies/agent-security.html",
    "case-studies/acuity.html",
)


class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.hrefs = []
        self.srcs = []

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            href = dict(attrs).get("href")
            if href:
                self.hrefs.append(href)
        elif tag == "img":
            src = dict(attrs).get("src")
            if src:
                self.srcs.append(src)


def collect_links(root, pages):
    external, errors = set(), []
    for page in pages:
        parser = Links()
        parser.feed((root / page).read_text())
        local_srcs = [src for src in parser.srcs if not urlsplit(src).scheme]
        for href in parser.hrefs + local_srcs:
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


def check_url(url, opener=urlopen):
    try:
        request = Request(url, headers={"User-Agent": "portfolio-link-check/1.0"})
        with opener(request, timeout=20) as response:
            status = response.status
            final = urlsplit(response.geturl())
            if status != 200:
                return f"{url}: HTTP {status}"
            if "/auth/" in final.path or "/login" in final.path:
                return f"{url}: redirects to login ({response.geturl()})"
    except HTTPError as error:
        message = f"{url}: {error}"
        error.close()
        return message
    except (URLError, TimeoutError, OSError) as error:
        return f"{url}: {error}"
    return None


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
        f"{len(PAGES)} public pages, {len(urls)} external destinations, {len(errors)} failures"
    )
    return bool(errors)


if __name__ == "__main__":
    raise SystemExit(main())
