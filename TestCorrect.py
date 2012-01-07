#!/usr/bin/env python

import logging
import random
import unittest

import Storage

from Constants import DEFAULT_DEPTH
from Common import setup_logging

class TestStudentIndex(unittest.TestCase):
    def setUp(self):
        """Setup the storage, that has student index and course index."""
        self.storage = Storage.Storage()
        self.storage.update_from_excel("tablea.xls")
        self.storage.update_from_excel("tableb.xls")

    def testGetHorts(self):
        """
        Test getting horts down to default depths using Dijkstra and recursive method.

        It is important to run test on same data multiple times, because the
        recursive method tends to cache the data.
        """
        self.storage.student_index.update_horting()
        for i in range(10):
            student_id = random.choice(self.storage.student_index.student_index.keys())
            horts_recursive_set = self.storage.student_index.get_horts(student_id)
            horts_dijkstra = self.storage.student_index.test_build_all_paths_dijkstra(student_id)
            horts_dijkstra_set = set(horts_dijkstra)
            self.assertEqual(len(horts_dijkstra), len(horts_dijkstra_set))
            self.assertEqual(horts_recursive_set, horts_dijkstra_set)

    def tearDown(self):
        pass

if __name__ == "__main__":
    setup_logging()
    unittest.main()
