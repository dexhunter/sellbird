"""Baseline for sellbird.gate.do_not_contact_domain_match.

Discovery calls this once per business with the same suppression list.
Prints the median milliseconds of 5 passes over that batch.
"""
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from sellbird.gate import do_not_contact_domain_match


def suppression_list() -> tuple[str, ...]:
    """Already-normalised domains, the shape ComplianceConfig stores, plus a few pastes."""
    entries = [f"blocked-{i}.example" for i in range(180)]
    entries.extend([
        "https://www.blocked-3.example/about",
        "mailto:jane@other.example",
        "*.blocked-9.example",
        "acme.example",
    ])
    return tuple(entries)


def discovered_domains() -> list[str]:
    hosts = [f"shop-{i}.example" for i in range(500)]
    hosts[40] = "mail.blocked-3.example"       # subdomain of a listed domain
    hosts[41] = "notblocked-3.example"         # lookalike, not listed
    hosts[42] = "acme.example"
    return hosts


def main() -> None:
    entries = suppression_list()
    hosts = discovered_domains()

    def once() -> None:
        for host in hosts:
            do_not_contact_domain_match(host, entries)

    once()
    samples = []
    for _ in range(5):
        started = time.perf_counter()
        once()
        samples.append((time.perf_counter() - started) * 1000.0)
    samples.sort()
    print(f"{samples[2]:.4f}")


if __name__ == "__main__":
    main()
