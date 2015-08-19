#!/usr/bin/python
# coding=utf-8
###############################################################################

from test import CollectorTestCase
from test import get_collector_config
from test import unittest

from rq import RQCollector


###############################################################################

class TestRQCollector(CollectorTestCase):
    def setUp(self):
        config = get_collector_config('RQCollector', {
        })
        self.collector = RQCollector(config, None)

    def test_import(self):
        self.assertTrue(RQCollector)

###############################################################################
if __name__ == "__main__":
    unittest.main()
