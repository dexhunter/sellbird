"""Baseline peak memory for sellbird.collectors.people.emails_on_page.

The scan keeps several full-page copies (script strip, unescape, tag strip).
Prints the median tracemalloc peak in bytes across 5 calls.
"""
import sys
import tracemalloc
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from sellbird.collectors.people import emails_on_page


def homepage() -> str:
    """A long homepage that publishes one mailto and one obfuscated address."""
    script = "<script>" + ("var q=1;" * 50000) + "</script>"
    paragraphs = "".join(
        f"<p>Acme Roofing has served block {i} since 1998.</p>" for i in range(6000)
    )
    contacts = (
        "<a class='email-link' data-user='owner' data-domain='acme.example'>Email</a>"
        "<p>office [at] acme [dot] com</p>"
        "<a href='mailto:crew@acme.example'>crew</a>"
    )
    return "<html><head>" + script + "</head><body>" + contacts + paragraphs + "</body></html>"


def peak_bytes(html: str) -> int:
    tracemalloc.start()
    emails_on_page(html)
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return peak


def main() -> None:
    html = homepage()
    peak_bytes(html)
    samples = sorted(peak_bytes(html) for _ in range(5))
    print(str(samples[2]))


if __name__ == "__main__":
    main()
