"""Baseline for ProfileCollector.detect_tech.

Fingerprints are separate case-insensitive regex scans over the full homepage.
Prints the median milliseconds of 5 calls.
"""
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from sellbird.collectors.profile import ProfileCollector


def homepage() -> str:
    """A small-business homepage with two real fingerprints buried in a large body."""
    scripts = []
    for i in range(60):
        scripts.append("<script>var x='" + ("n" * 1800) + "';</script>")
    body = []
    for i in range(900):
        body.append(
            f"<section><h2>Service {i}</h2><p>Acme Roofing repairs storm damage "
            "and replaces shingles across the metro area.</p></section>"
        )
    fingerprints = (
        '<script src="https://cdn.shopify.com/s/files/theme.js"></script>'
        '<link rel="stylesheet" href="/wp-content/themes/acme/style.css">'
    )
    return (
        "<!doctype html><html><head><title>Acme Roofing</title>"
        + "".join(scripts)
        + fingerprints
        + "</head><body>"
        + "".join(body)
        + "</body></html>"
    )


def main() -> None:
    html = homepage()
    collector = ProfileCollector(None)
    collector.detect_tech(html)
    samples = []
    for _ in range(5):
        started = time.perf_counter()
        collector.detect_tech(html)
        samples.append((time.perf_counter() - started) * 1000.0)
    samples.sort()
    print(f"{samples[2]:.4f}")


if __name__ == "__main__":
    main()
