import unittest
from src.ids import IDS
from src.config import load_config

class TestIDS(unittest.TestCase):
    def setUp(self):
        self.config = {
            "patterns": [
                {"name": "TestPattern", "regex": "attack from ([\\d.]+)", "severity": "high"}
            ],
            "log_file": "test.log"
        }
        self.ids = IDS(self.config)

    def test_analyze_line(self):
        line = "attack from 1.2.3.4 detected"
        alerts = self.ids.analyze_line(line, 1)
        self.assertEqual(len(alerts), 1)
        self.assertEqual(alerts[0]['ip'], "1.2.3.4")
        self.assertEqual(alerts[0]['pattern'], "TestPattern")

if __name__ == "__main__":
    unittest.main()
