#!/usr/bin/env python

import logging
import operator
import random
import re
import unittest
import xlrd

import Storage

from Constants import DEFAULT_DEPTH, MIN_STAT_STUDENTS
from Common import setup_logging, load_major_names

class TestMajors(unittest.TestCase):
    def setUp(self):
        """Setup the storage, that has student index and course index."""
        self.storage = Storage.Storage()
        self.storage.update_from_excel("tablea.xls")
        self.storage.update_from_excel("tableb.xls")

    def testMajorCounts(self):
        """Testing the number of students and accuracy of horting in majors."""
        logging.info("Test: Number students and accuracy of horting in majors.")
        m_count = {}
        m_accuracy = []
        m_acc_gur = {}
        m_names = load_major_names()

        for student in self.storage.student_index.student_index.itervalues():
            major_id = student.major_id
            m_count[major_id] = m_count.get(major_id, 0) + 1

        r = re.compile(".+Major\s(\w+):\s(\S+)\s.*")
        for major_id, major_result in r.findall(open("./Logs/test_majors_prediction_gur_40_100.txt").read()):
            m_acc_gur[major_id] = major_result
        for major_id, major_result in r.findall(open("./Logs/test_majors_prediction_40_100.txt").read()):
            m_accuracy.append((major_id, major_result))
        m_accuracy.sort(key=operator.itemgetter(1), reverse=True)

        logging.info("Total students: %i", len(self.storage.student_index.student_index))
        logging.info("Total majors: %i", len(m_count))
        logging.info("Major id, name followed by number of students and accuracy")
        for major_id, major_acc in m_accuracy:
            try:
                #only consider majors of 5 students or more
                if m_count[major_id] >= MIN_STAT_STUDENTS:
                    logging.info("%s&%s&%s&%s&%i\\\\\hline", major_id, major_acc, m_acc_gur[major_id], m_names[major_id], m_count[major_id])
                    #logging.info("%s; %s; %s; %s; %i", major_id, major_acc, m_acc_gur[major_id], m_names[major_id], m_count[major_id])
            except KeyError:
                #non-standard entries from database
                continue


    def _testHighHorting(self):
        """
        Check horting between students and check which ones have horting that is
        very high.

        The high is considered if horting value is greater than 0.75 for more
        than 0.5 horts of student.
        """
        logging.info("Test: High horting values between students by major.")
        self.storage.student_index.update_horting()
        majors, t_majors = {}, {}
        m_names = load_major_names()

        for student in self.storage.student_index.student_index.itervalues():
            major_id = student.major_id
            t_majors[major_id] = t_majors.get(major_id, 0) + 1
            high_horts = sum((1 for hort_val in student.horts.itervalues() if hort_val > 0.75))
            if (float(high_horts) / len(student.horts)) > 0.50:
                majors[major_id] = majors.get(major_id, 0) + 1

        m_list = [(m_id, m_val) for m_id, m_val in majors.iteritems() if m_val > 0]
        m_list.sort(key=operator.itemgetter(1), reverse=True)
        logging.debug("Highest values are...")
        for m_id, m_val in m_list:
            logging.info("%s: %2.2f (%2.2f): %s", m_id, m_val, float(m_val) / t_majors[m_id], m_names[m_id])
            #logging.info("%s&%2.2f&%2.2f&%s\\\\\hline", m_id, m_val, float(m_val) / t_majors[m_id], m_names[m_id])

    def _testHortsOutsideMajor(self):
        """Test how many horts are outside the major for each student."""
        logging.info("Test: The number of students outside the major.")
        index = self.storage.student_index
        index.update_horting()
        majors, t_majors, t_students = {}, {}, {}
        m_names = load_major_names()
        total_students, total_horts, total_outside = 0, 0, 0

        for student in index.student_index.itervalues():
            total_students += 1
            major_id = student.major_id
            t_students[major_id] = t_students.get(major_id, 0) + 1
            for hort_id in student.horts.iterkeys():
                total_horts += 1
                t_majors[major_id] = t_majors.get(major_id, 0) + 1
                if index.student_index[hort_id].major_id != major_id:
                    total_outside += 1
                    majors[major_id] = majors.get(major_id, 0) + 1
        #the list comprehension will only take majors with more than 5 students
        m_list = [(m_id, m_val, float(m_val) / t_majors[m_id]) for m_id, m_val in majors.iteritems() if t_students[m_id] > 5]
        m_list.sort(key=operator.itemgetter(2), reverse=True)
        logging.info("Total students: %i", total_students)
        logging.info("Total horts: %i", total_horts)
        logging.info("Avg horts outside major: %i (%2.2f)", total_outside, float(total_outside) / total_horts)
        logging.info("Highest values with majors with more than 5 students...")
        for m_id, m_val, m_pc in m_list:
            #logging.info("%s: %2.2f (%2.2f): %s(%i)", m_id, m_val, m_pc, m_names[m_id], t_students[m_id])
            logging.info("%s&%2.2f&%2.2f&%s&%i\\\\\hline", m_id, m_val, m_pc, m_names[m_id], t_students[m_id])

    def tearDown(self):
        pass

if __name__ == "__main__":
    setup_logging("test_majors.txt")
    unittest.main()
