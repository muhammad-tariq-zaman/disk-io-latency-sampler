"""Sample disk write/read latency in a directory and summarise it.

Usage: python3 main.py [--dir /tmp] [--chunks 10] [--size-kb 256]
Writes chunks with fsync, reads them back, and reports count, average,
minimum, maximum and 95th percentile latency in milliseconds.
"""
import argparse
import os
import sys
import tempfile
import time


def percentile(samples, pct):
    ordered = sorted(samples)
    index = max(0, min(len(ordered) - 1, int(pct / 100 * len(ordered))))
    return ordered[index]


def summarise(samples):
    return {"count": len(samples), "avg_ms": sum(samples) / len(samples),
            "min_ms": min(samples), "max_ms": max(samples),
            "p95_ms": percentile(samples, 95)}


def sample(directory, chunks=10, size_kb=256):
    payload = os.urandom(size_kb * 1024)
    path = os.path.join(directory, "io-latency-sample.bin")
    write_times, read_times = [], []
    try:
        with open(path, "wb") as f:
            for _ in range(chunks):
                start = time.monotonic()
                f.write(payload)
                f.flush()
                os.fsync(f.fileno())
                write_times.append((time.monotonic() - start) * 1000)
        with open(path, "rb") as f:
            for _ in range(chunks):
                start = time.monotonic()
                f.read(size_kb * 1024)
                read_times.append((time.monotonic() - start) * 1000)
    finally:
        if os.path.exists(path):
            os.unlink(path)
    return write_times, read_times


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dir", default=None, help="Directory to test (default: a temp dir)")
    parser.add_argument("--chunks", type=int, default=10)
    parser.add_argument("--size-kb", type=int, default=256)
    args = parser.parse_args(argv)
    directory = args.dir or tempfile.mkdtemp()
    writes, reads = sample(directory, args.chunks, args.size_kb)
    for label, samples in (("write", writes), ("read", reads)):
        stats = summarise(samples)
        print(f"{label}: {stats['count']} samples, avg {stats['avg_ms']:.2f}ms, "
              f"min {stats['min_ms']:.2f}ms, max {stats['max_ms']:.2f}ms, p95 {stats['p95_ms']:.2f}ms")
    return 0


if __name__ == "__main__":
    sys.exit(main())
