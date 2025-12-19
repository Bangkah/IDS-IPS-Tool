import unittest

from src.ips import IPS

class TestIPS(unittest.TestCase):
    def setUp(self):
        self.config = {
            "patterns": [
                {"name": "TestPattern", "regex": "attack from ([\\d.]+)", "severity": "high"}
            ],
            "log_file": "test.log"
        }
        self.ips = IPS(self.config)

    def test_analyze_and_block(self):
        # Simulasi log file
        import tempfile
        with tempfile.NamedTemporaryFile(mode='w+', delete=False) as f:
            f.write("attack from 1.2.3.4 detected\n")
            f.flush()
            self.ips.analyze_and_block(f.name)
        # Cek apakah IP sudah masuk blocked_ips
        self.assertIn("1.2.3.4", self.ips.blocked_ips)

if __name__ == "__main__":
    unittest.main()
