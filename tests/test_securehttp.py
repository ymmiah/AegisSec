import email.message
import ssl
import unittest
import urllib.request

from aegissec_vuln import securehttp
from aegissec_vuln.http import HttpError, JsonHttpClient


class EndpointTests(unittest.TestCase):
    def test_https_allowed_anywhere(self):
        securehttp.validate_endpoint("https://api.openai.com/v1")
        securehttp.validate_endpoint("https://integrate.api.nvidia.com/v1")

    def test_http_allowed_only_local(self):
        for ok in ("http://localhost:8000/v1", "http://127.0.0.1/v1", "http://192.168.1.10:8000", "http://nim.local/v1", "http://[::1]:8000"):
            securehttp.validate_endpoint(ok)

    def test_http_remote_refused(self):
        for bad in ("http://api.openai.com/v1", "http://8.8.8.8/v1", "http://evil.example/v1"):
            with self.assertRaises(ValueError):
                securehttp.validate_endpoint(bad)

    def test_non_http_scheme_refused(self):
        for bad in ("ftp://host/x", "file:///etc/passwd", "gopher://x"):
            with self.assertRaises(ValueError):
                securehttp.validate_endpoint(bad)


class TlsTests(unittest.TestCase):
    def test_context_verifies(self):
        ctx = securehttp.ssl_context()
        self.assertTrue(ctx.check_hostname)
        self.assertEqual(ctx.verify_mode, ssl.CERT_REQUIRED)


class RedirectTests(unittest.TestCase):
    def _redirect(self, from_url, to_url):
        handler = securehttp._StripAuthOnRedirect()
        req = urllib.request.Request(from_url, headers={"Authorization": "Bearer secrettoken", "Accept": "application/json"})
        return handler.redirect_request(req, None, 302, "Found", email.message.Message(), to_url)

    def test_auth_stripped_on_cross_host_redirect(self):
        new = self._redirect("https://api.vendor.com/v1/x", "https://evil.example/collect")
        self.assertNotIn("Authorization", new.headers)
        self.assertIn("Accept", new.headers)

    def test_auth_kept_on_same_host_redirect(self):
        new = self._redirect("https://api.vendor.com/v1/x", "https://api.vendor.com/v2/x")
        self.assertIn("Authorization", new.headers)


class RedactTests(unittest.TestCase):
    def test_redacts_known_value_and_key_shapes(self):
        text = "error: key sk-ABC123DEF456 and nvapi-ZZZ999888 and Bearer ghp_abcdef123456; mine=supersecretvalue"
        out = securehttp.redact(text, ["supersecretvalue"])
        for leak in ("sk-ABC123DEF456", "nvapi-ZZZ999888", "ghp_abcdef123456", "supersecretvalue"):
            self.assertNotIn(leak, out)
        self.assertIn("***", out)

    def test_short_values_not_overmatched(self):
        self.assertEqual(securehttp.redact("abc", ["ab"]), "abc")  # too short to redact blindly


class ClientEnforcementTests(unittest.TestCase):
    def test_vuln_client_refuses_plain_http_remote(self):
        with self.assertRaises(HttpError):
            JsonHttpClient().request_json("GET", "http://services.nvd.nist.gov/rest")


if __name__ == "__main__":
    unittest.main()
