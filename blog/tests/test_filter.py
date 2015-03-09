import os
import unittest
import datetime

os.environ['CONFIG_PATH'] = 'blog.config.TestingConfig'

from blog.filters import dateformat


class FilterTests(unittest.TestCase):

    def test_date_format(self):
        date = datetime.date(1999, 12, 31)
        formatted = dateformat(date, '%y/%m/%d')
        self.assertEqual(formatted, '99/12/31')

    def test_date_format_none(self):
        formatted = dateformat(None, '%y/%m/%d')
        self.assertEqual(formatted, None)


if __name__ == '__main__':
    unittest.main()
