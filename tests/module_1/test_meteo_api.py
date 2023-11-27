""" This is a dummy example to show how to import code from src/ for testing"""
import unittest
from src.module_1.module_1_meteo_api import (
    main,
    get_data_meteo_api,
    calculate_average,
    calculate_dispersion,
)


class TestModule1(unittest.TestCase):
    def test_calculate_average(self):
        data = [1, 2, 3, 4, 5]
        self.assertEqual(calculate_average(data), 3.0)


if __name__ == "__main__":
    unittest.main()
# def test_main():
# pyenraise NotImplementedError
