import os, sys, tempfile
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import unittest
from main import summarise, sample, percentile


class TestIoSampler(unittest.TestCase):
    def test_summarise(self):
        stats = summarise([10.0, 20.0, 30.0, 40.0])
        self.assertEqual(stats["count"], 4)
        self.assertAlmostEqual(stats["avg_ms"], 25.0)
        self.assertEqual(stats["min_ms"], 10.0)
        self.assertEqual(stats["max_ms"], 40.0)

    def test_percentile_top(self):
        self.assertEqual(percentile([1.0, 2.0, 3.0, 4.0], 95), 4.0)

    def test_sample_returns_chunks(self):
        with tempfile.TemporaryDirectory() as tmp:
            writes, reads = sample(tmp, chunks=3, size_kb=16)
            self.assertEqual((len(writes), len(reads)), (3, 3))
            self.assertTrue(all(w >= 0 for w in writes + reads))
