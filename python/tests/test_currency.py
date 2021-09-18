# coding: utf-8
import unittest

from common.helpers.Currency import Currency


class TestCurrency(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestCurrency, self).__init__(*args, **kwargs)
        self.account_id = "f24c250e-b71a-4f48-acdb-a02637ab76f6"

    def test_get_symbol_from_code(self):
        code = "GBP"

        result = (Currency()).getSymbolFromCode(code)

        expected = chr(163)  # £

        self.assertEquals(result, expected)
