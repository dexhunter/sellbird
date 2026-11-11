"""Baseline for sellbird.collectors.profile.accelerators.

One About-sized page is parsed from scratch for every accelerator program.
Prints the median milliseconds of 5 calls.
"""
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from sellbird.collectors.profile import accelerators


def about_page() -> str:
    """A startup About page: a script block, then a few thousand short paragraphs."""
    script = "<script>window.__DATA__='" + ("a1b2" * 8000) + "';</script>"
    style = "<style>" + (".nav{display:flex;color:#222;}" * 200) + "</style>"
    paragraphs = []
    for i in range(1800):
        paragraphs.append(
            f"<p>Acme builds scheduling software for shop {i}. "
            "The team is in Denver and ships weekly.</p>"
        )
    alt = '<img alt="Acme mark" src="/logo.png">'
    return (
        "<!doctype html><html><head><title>About Acme</title>"
        + style + script
        + "</head><body><h1>About Acme</h1>"
        + alt
        + "".join(paragraphs)
        + "</body></html>"
    )


def main() -> None:
    html = about_page()
    accelerators(html, "acme.example")
    samples = []
    for _ in range(5):
        started = time.perf_counter()
        accelerators(html, "acme.example")
        samples.append((time.perf_counter() - started) * 1000.0)
    samples.sort()
    print(f"{samples[2]:.4f}")


if __name__ == "__main__":
    main()
