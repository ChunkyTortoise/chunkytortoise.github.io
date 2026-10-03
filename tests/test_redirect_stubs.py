"""Retired pages redirect with root-absolute targets that exist in the site."""

import re
from html.parser import HTMLParser
from pathlib import Path
from unittest import TestCase, main

ROOT = Path(__file__).resolve().parents[1]
REFRESH = re.compile(r'http-equiv="refresh"\s+content="\d+;\s*url=([^"]+)"', re.IGNORECASE)


class Hrefs(HTMLParser):
    def __init__(self):
        super().__init__()
        self.hrefs = []

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            href = dict(attrs).get("href")
            if href:
                self.hrefs.append(href)


def site_path(url):
    """Map a root-absolute URL path to a file in the repository."""
    path = url.split("#", 1)[0].split("?", 1)[0]
    target = ROOT / path.lstrip("/")
    return target / "index.html" if path.endswith("/") else target


def stubs():
    for page in sorted(ROOT.rglob("*.html")):
        if "node_modules" in page.parts:
            continue
        match = REFRESH.search(page.read_text())
        if match:
            yield page, match.group(1)


class RedirectStubTests(TestCase):
    def test_stubs_exist(self):
        self.assertGreater(len(list(stubs())), 0)

    def test_refresh_targets_are_root_absolute_and_exist(self):
        for page, url in stubs():
            with self.subTest(page=str(page.relative_to(ROOT))):
                self.assertTrue(url.startswith("/"), f"refresh target {url!r} is not root-absolute")
                self.assertTrue(site_path(url).is_file(), f"refresh target {url!r} does not exist")

    def test_stub_links_resolve(self):
        for page, _ in stubs():
            parser = Hrefs()
            parser.feed(page.read_text())
            for href in parser.hrefs:
                if href.startswith(("http://", "https://", "mailto:")):
                    continue
                with self.subTest(page=str(page.relative_to(ROOT)), href=href):
                    self.assertTrue(href.startswith("/"), f"link {href!r} is not root-absolute")
                    self.assertTrue(site_path(href).is_file(), f"link {href!r} does not exist")

    def test_relative_target_would_fail(self):
        """A subfolder stub with url=index.html resolves to a missing file."""
        self.assertFalse((ROOT / "services" / "index.html").is_file())


if __name__ == "__main__":
    main()
