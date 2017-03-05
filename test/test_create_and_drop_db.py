# coding=utf-8

import os
import sys
import unittest


from zhihu_database.operations import drop_db


class TestCreateAndDropDB(unittest.TestCase):


    def test_drop(self):
        drop_db()
        self.assertEqual(1, 1)

if __name__ == '__main__':
    unittest.main()