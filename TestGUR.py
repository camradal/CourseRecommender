#!/usr/bin/env python

import copy
import random
import unittest

import Storage

from Common import *
from GenericTest import GenericTest

class TestStudentIndex(GenericTest):
    def testGUROne(self):
        """
        Take one GUR course out student history and try to predict it.
        """
        logging.info("Horting Exclude One GUR")
        gur_ids = load_courses("Test/gur_all.dat")
        index = self.storage.student_index.student_index
        count, pos, num = 0.0, 0.0, 0.0
        for i in range(NUM_TESTS):
            course_ids = set()
            #there's a chance that there are no GURs taken, then take another sample
            while len(course_ids) == 0:
                student_id = random.choice(index.keys())
                course_ids = index[student_id].courses.intersection(gur_ids)
            c, p, n = self.horting_exclude_num(num=1, student_id=student_id, hort_courses=gur_ids)
            logging.debug("Round %i: accuracy: %2.2f, position: %2.2f", i, float(c) / n, float(p) / n)
            count += c
            pos += p
            num += n
        logging.info(">>> Test Result: %2.2f accuracy, %2.2f avg position", count / num, pos / count)
        logging.info(LINE)
        self.assert_(count / num > MIN_CORRECT)

    def testGURAll(self):
        """
        Take all GUR courses out student history and try to predict them.

        Load all GUR courses, remove all GURs from student course history and
        then try to predict.At least half of student's GURs have to be predicted
        for test to pass.
        """
        logging.info("Horting Exclude All GURs")
        gur_ids = load_courses("Test/gur_all.dat")
        index = self.storage.student_index.student_index
        count, pos, num = 0.0, 0.0, 0.0
        for i in range(NUM_TESTS):
            #there's a chance there are no GURs taken or sample is too small
            course_ids = set()
            while len(course_ids) < MIN_CLASSES:
                student_id = random.choice(index.keys())
                course_ids = index[student_id].courses.intersection(gur_ids)
            c, p, n = self.horting_exclude_num(num=0, student_id=student_id, hort_courses=gur_ids)
            logging.debug("Round %i: accuracy: %2.2f, position: %2.2f", i, float(c) / n, float(p) / n)
            count += c
            pos += p
            num += n
        logging.info(">>> Test Result: %2.2f accuracy, %2.2f avg position", count / num, pos / count)
        logging.info(LINE)
        self.assert_(count / num > MIN_CORRECT)

if __name__ == "__main__":
    random.seed()
    setup_logging("test_gur")
    unittest.main()
