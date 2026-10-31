# disk-io-latency-sampler

Measure real disk write (fsync) and read latency in a directory and summarise average, min, max and p95 — a quick check when an app complains the disk is slow.

## How to run

```sh
python3 main.py --chunks 10 --size-kb 256
```

## Example output

```
write: 10 samples, avg 1.23ms, min 0.80ms, max 2.10ms, p95 2.10ms
read: 10 samples, avg 0.45ms, min 0.30ms, max 0.70ms, p95 0.70ms
```

Standard library only. Run the tests with `python3 -m unittest discover`.
