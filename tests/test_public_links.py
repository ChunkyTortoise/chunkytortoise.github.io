"""Exercise anonymous link collection and HTTP failure handling."""

import importlib.util
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest import TestCase, main
from urllib.error import HTTPError

spec = importlib.util.spec_from_file_location(
    "links", Path(__file__).resolve().parents[1] / "scripts/check_public_links.py"
)
links = importlib.util.module_from_spec(spec)
spec.loader.exec_module(links)


class Response:
    status = 200

    def __init__(self, url):
        self.url = url

    def geturl(self):
        return self.url

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return False


class PublicLinksTests(TestCase):
    def test_collects_deduplicated_external_and_existing_local(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "resume.pdf").write_bytes(b"pdf")
            (root / "index.html").write_text(
                '<a href="resume.pdf">Resume</a><a href="https://example.com">One</a><a href="https://example.com">Two</a>'
            )
            self.assertEqual(
                links.collect_links(root, ["index.html"]), (["https://example.com"], [])
            )

    def test_missing_local_file(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "index.html").write_text('<a href="missing.pdf">Resume</a>')
            self.assertEqual(
                links.collect_links(root, ["index.html"])[1],
                ["index.html: missing missing.pdf"],
            )

    def test_anonymous_success(self):
        def opener(request, timeout):
            self.assertNotIn("Authorization", request.headers)
            return Response(request.full_url)

        self.assertIsNone(links.check_url("https://example.com", opener))

    def test_login_redirect_fails(self):
        self.assertIn(
            "redirects to login",
            links.check_url(
                "https://example.com",
                lambda *a, **k: Response("https://example.com/auth/app"),
            ),
        )

    def test_404_fails(self):
        def opener(request, timeout):
            raise HTTPError(request.full_url, 404, "Not Found", {}, None)

        self.assertIn("404", links.check_url("https://example.com", opener))

    def test_404_is_not_retried(self):
        calls = []

        def opener(request, timeout):
            calls.append(1)
            raise HTTPError(request.full_url, 404, "Not Found", {}, None)

        links.check_url("https://example.com", opener, sleep=lambda s: None)
        self.assertEqual(len(calls), 1)

    def test_server_error_retried_then_passes(self):
        calls = []

        def opener(request, timeout):
            calls.append(1)
            if len(calls) < 3:
                raise HTTPError(request.full_url, 504, "Gateway Time-out", {}, None)
            return Response(request.full_url)

        self.assertIsNone(links.check_url("https://example.com", opener, sleep=lambda s: None))
        self.assertEqual(len(calls), 3)

    def test_persistent_server_error_fails(self):
        def opener(request, timeout):
            raise HTTPError(request.full_url, 503, "Service Unavailable", {}, None)

        self.assertIn(
            "503", links.check_url("https://example.com", opener, sleep=lambda s: None)
        )


if __name__ == "__main__":
    main()
