# backend/src/tests/test_data_loader.py

import unittest
from src.utils.data_loader import DataLoader

class TestDataLoader(unittest.TestCase):
    def test_load_data_from_csv(self):
        data_loader = DataLoader()
        data = data_loader.load_data_from_csv("test.csv")
        self.assertIsNotNone(data)
