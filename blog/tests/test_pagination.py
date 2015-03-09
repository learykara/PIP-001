import os
import unittest

os.environ['CONFIG_PATH'] = 'blog.config.TestingConfig'

import blog
from blog.views import paginate


class TestPagination(unittest.TestCase):

    def test_pagination(self):
        [start, end, total_pages] = paginate(0, 10)
        self.assertEqual(start, 0)
        self.assertEqual(end, 10)


if __name__ == '__main__':
    unittest.main()
