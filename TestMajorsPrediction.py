#!/usr/bin/env python

import copy
import random
import unittest

import Storage

from Common import *
from GenericTest import GenericTest

class TestMajorsPrediction(GenericTest):
    def testHortingMajors(self):
        """Test how horting works for different majors."""
        logging.info("Horting Accuracy for Majors")
        m_count, m_pos, m_num = {}, {}, {}
        index = self.storage.student_index.student_index
        for i in range(10000):
            student_id = random.choice(index.keys())
            major_id = index[student_id].major_id
            c, p, n = self.horting_exclude_num(num=1, student_id=student_id)
            m_count[major_id] = m_count.get(major_id, 0) + c
            m_pos[major_id] = m_pos.get(major_id, 0) + p
            m_num[major_id] = m_num.get(major_id, 0) + n
            logging.debug("Round %i: major: %s, accuracy: %2.2f, position: %2.2f", i, major_id, float(c) / n, float(p) / n)
        logging.info(">>> Horting Accuracy for Majors Test Results...")
        for major_id in m_count.iterkeys():
            #print major_id, m_count[major_id], m_num[major_id], m_pos[major_id]
            #logging.info("Major %s: %2.2f accuracy, %2.2f avg position",
                         #major_id, m_count[major_id] / m_num[major_id], m_pos[major_id] / m_num[major_id])
            logging.info("Major %s: %2.2f accuracy", major_id, float(m_count[major_id]) / m_num[major_id])
        logging.info(LINE)

    def testHortingMajorsGur(self):
        """Test how horting works for different majors for GURs."""
        logging.info("Horting Accuracy for Majors GURs")
        m_count, m_pos, m_num = {}, {}, {}
        gur_ids = load_courses("Test/gur_all.dat")
        index = self.storage.student_index.student_index
        for i in range(10000):
            course_ids = set()
            while len(course_ids) == 0:
                student_id = random.choice(index.keys())
                major_id = index[student_id].major_id
                course_ids = index[student_id].courses.intersection(gur_ids)
            c, p, n = self.horting_exclude_num(num=1, student_id=student_id, hort_courses=gur_ids)
            m_count[major_id] = m_count.get(major_id, 0) + c
            m_pos[major_id] = m_pos.get(major_id, 0) + p
            m_num[major_id] = m_num.get(major_id, 0) + n
            logging.debug("Round %i: major: %s, accuracy: %2.2f, position: %2.2f", i, major_id, float(c) / n, float(p) / n)
        logging.info(">>> Horting Accuracy for Majors GURs Test Results...")
        for major_id in m_count.iterkeys():
            #print major_id, m_count[major_id], m_num[major_id], m_pos[major_id]
            #logging.info("Major %s: %2.2f accuracy, %2.2f avg position",
                         #major_id, m_count[major_id] / m_num[major_id], m_pos[major_id] / m_num[major_id])
            logging.info("Major %s: %2.2f GUR accuracy", major_id, float(m_count[major_id]) / m_num[major_id])
        logging.info(LINE)

if __name__ == "__main__":
    random.seed()
    setup_logging("test_majors_prediction")
    unittest.main()
