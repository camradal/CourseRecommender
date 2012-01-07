#!/usr/bin/env python

import copy
import random
import unittest

import Storage

from Common import *
from GenericTest import GenericTest

class TestModifier(GenericTest):
    def _testModifierLow(self):
        """
        Test horting using modifier, try to predict low rated courses.

        Ideally, those courses should come up lower than without modifier.
        """
        logging.info("Horting Modifier Low Exclude One")
        index = self.storage.student_index.student_index
        count, pos, num = 0.0, 0.0, 0.0
        count_mod, pos_mod, num_mod = 0.0, 0.0, 0.0
        #Hack to remove the student with only 3 classes:
        self.mod_ids.remove("456ea9d2d1f27a6a9019db2c1ff99678")
        #test excluding low courses
        for i in range(NUM_TESTS):
            course_ids = set()
            while len(course_ids) == 0:
                student_id = random.choice(self.mod_ids)
                try:
                    course_ids = set(random.sample(index[student_id].rated_low, 1))
                except ValueError:
                    course_ids = set()
            c, p, n = self.horting_exclude_num(num=1, student_id=student_id, sample_ids=course_ids, modifier=False)
            count += c
            pos += p
            num += n
            logging.debug("Round %i w/o mod: accuracy: %2.2f, position: %2.2f", i, float(c) / n, float(p) / n)
            c, p, n = self.horting_exclude_num(num=1, student_id=student_id, sample_ids=course_ids, modifier=True)
            count_mod += c
            pos_mod += p
            num_mod += n
            logging.debug("Round %i with mod: accuracy: %2.2f, position: %2.2f", i, float(c) / n, float(p) / n)
        logging.info("Horting without modifier")
        logging.info(">>> Test Result: %2.2f accuracy, %2.2f avg position", count / num, pos / count)
        logging.info("Horting with modifier")
        logging.info(">>> Test Result: %2.2f accuracy, %2.2f avg position", count_mod / num_mod, pos_mod / count_mod)
        logging.info(LINE)

    def _testModifierHigh(self):
        """
        Test horting using modifier, try to predict high rated courses.

        Ideally, those courses should come up higher than without modifier.
        """
        logging.info("Horting Modifier High Exclude One")
        index = self.storage.student_index.student_index
        count, pos, num = 0.0, 0.0, 0.0
        count_mod, pos_mod, num_mod = 0.0, 0.0, 0.0
        #Hack to remove the student with only 3 classes:
        self.mod_ids.remove("456ea9d2d1f27a6a9019db2c1ff99678")
        #test excluding low courses
        for i in range(NUM_TESTS):
            course_ids = set()
            while len(course_ids) == 0:
                student_id = random.choice(self.mod_ids)
                try:
                    course_ids = set(random.sample(index[student_id].rated_low, 1))
                except ValueError:
                    course_ids = set()
            c, p, n = self.horting_exclude_num(num=1, student_id=student_id, sample_ids=course_ids, modifier=False)
            count += c
            pos += p
            num += n
            logging.debug("Round %i w/o mod: accuracy: %2.2f, position: %2.2f", i, float(c) / n, float(p) / n)
            c, p, n = self.horting_exclude_num(num=1, student_id=student_id, sample_ids=course_ids, modifier=True)
            count_mod += c
            pos_mod += p
            num_mod += n
            logging.debug("Round %i with mod: accuracy: %2.2f, position: %2.2f", i, float(c) / n, float(p) / n)
        logging.info("Horting without modifier")
        logging.info(">>> Test Result: %2.2f accuracy, %2.2f avg position", count / num, pos / count)
        logging.info("Horting with modifier")
        logging.info(">>> Test Result: %2.2f accuracy, %2.2f avg position", count_mod / num_mod, pos_mod / count_mod)
        logging.info(LINE)

    def testModifier(self):
        """
        Test modifier, that assigns preference to high and low rated courses.

        First, predict without modifier, than compare how it is better with
        modifier.

        Try predicting classes that are only highly rated. We don't want to
        predict classes that are low rated. Those classes would show really low
        in the ratings.
        """
        logging.info("Horting Modifier Exclude One")
        index = self.storage.student_index.student_index
        count, pos, num = 0.0, 0.0, 0.0
        count_mod, pos_mod, num_mod = 0.0, 0.0, 0.0
        #Hack to remove the student with only 3 classes:
        self.mod_ids.remove("456ea9d2d1f27a6a9019db2c1ff99678")
        for i in range(NUM_TESTS):
            student_id = random.choice(self.mod_ids)
            course_ids = set(random.sample(index[student_id].courses - index[student_id].rated_low, 1))
            c, p, n = self.horting_exclude_num(num=1, student_id=student_id, sample_ids=course_ids, modifier=False)
            count += c
            pos += p
            num += n
            logging.debug("Round %i w/o mod: accuracy: %2.2f, position: %2.2f", i, float(c) / n, float(p) / n)
            c, p, n = self.horting_exclude_num(num=1, student_id=student_id, sample_ids=course_ids, modifier=True)
            count_mod += c
            pos_mod += p
            num_mod += n
            logging.debug("Round %i with mod: accuracy: %2.2f, position: %2.2f", i, float(c) / n, float(p) / n)
        logging.info("Horting without modifier")
        logging.info(">>> Test Result: %2.2f accuracy, %2.2f avg position", count / num, pos / count)
        logging.info("Horting with modifier")
        logging.info(">>> Test Result: %2.2f accuracy, %2.2f avg position", count_mod / num_mod, pos_mod / count_mod)
        logging.info(LINE)

if __name__ == "__main__":
    random.seed()
    setup_logging("test_modifier")
    unittest.main()
