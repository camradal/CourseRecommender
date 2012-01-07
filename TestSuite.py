#!/usr/bin/env python

import copy
import random
import unittest

import Storage

from Common import *
from GenericTest import GenericTest

class TestStudentIndex(GenericTest):
    def testHortingExcludeOne(self):
        """
        Take out one class out and test the effectiveness of prediction using
        horting only.

        Choose a random student, take out one class and calculate horting based
        on the rest of classes. After the horts are discovered, use prediction
        using horting only to find if the course that was taken out is in the
        top predicted courses for the student.

        At least half of the courses must be predicted for the test to pass.
        """
        logging.info("Horting Exclude One")
        count, pos, num = 0.0, 0.0, 0.0
        for i in range(NUM_TESTS):
            c, p, n = self.horting_exclude_num(1)
            logging.debug("Round %i: accuracy: %2.2f, position: %2.2f", i, float(c) / n, float(p) / n)
            count += c
            pos += p
            num += n
        logging.info(">>> Test Result: %2.2f accuracy, %2.2f avg position", count / num, pos / count)
        logging.info(LINE)
        self.assert_(count > MIN_CORRECT * NUM_TESTS)

    def testHortingExcludeTen(self):
        """
        Take out ten of the classes and test the effectiveness of prediction
        using horting only.

        At least half of the courses excluded should be predicted, otherwise
        test will fail.
        """
        logging.info("Horting Exclude Ten")
        index = self.storage.student_index.student_index
        count, pos, num = 0.0, 0.0, 0.0
        for i in range(NUM_TESTS):
            course_ids = set()
            while len(course_ids) < 10 + MIN_CLASSES:
                student_id = random.choice(index.keys())
                course_ids = index[student_id].courses
            c, p, n = self.horting_exclude_num(num=10, student_id=student_id)
            logging.debug("Round %i: accuracy: %2.2f, position: %2.2f", i, float(c) / n, float(p) / n)
            count += c
            pos += p
            num += n
        logging.info(">>> Test Result: %2.2f accuracy, %2.2f avg position", count / num, pos / count)
        logging.info(LINE)
        self.assert_(count / num > MIN_CORRECT)

if __name__ == "__main__":
    random.seed()
    setup_logging("test_one_ten")
    unittest.main()
