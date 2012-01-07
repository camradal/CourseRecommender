#!/usr/bin/env python

import copy
import random
import unittest

import Storage

from Common import *
from GenericTest import GenericTest

class TestStudentIndex(GenericTest):
    def check_major_classes(self, major_id, major_file):
        req_ids = load_courses(major_file)
        sample_ids = {}
        index = self.storage.student_index.student_index
        for student_id, student in index.iteritems():
            if student.major_id.startswith(major_id):
                #exclude all major courses
                major_ids = set((course_id for course_id in student.courses for req_id in req_ids if course_id.startswith(req_id)))
                non_major_ids = student.courses - major_ids
                if len(non_major_ids) > 0:
                    hort_courses = self.storage.student_index.get_hort_courses(student_id) | self.storage.student_index[student_id].courses
                    major_hort_courses = set((course_id for course_id in hort_courses for req_id in req_ids if course_id.startswith(req_id)))
                    sample_ids[student_id] = (non_major_ids, hort_courses - major_hort_courses)
        return sample_ids

    def testHortingExcludeNonMajor(self):
        """
        Test horting prediction capabilities when excluding all the major
        classes and trying to predict only electives and GURs.

        The prediction is based solely on major courses, electives and GURs have
        to predicted.

        The prediction set should not include any major courses either.

        The departments that are tested are:
        1) Accounting (DD*)
        2) Archeology (UC05)
        3) Computer Science (NC*)
        4) Human Services (6B*)
        5) Theatre (2D*)
        They represent five different colleges from Western.
        """
        logging.info("Horting Exclude All Non-Major Courses")
        non_major_ids = {} #a dict with id key and non-major classes value
        non_major_ids.update(self.check_major_classes(major_id="DD", major_file="Majors/accounting.dat"))
        non_major_ids.update(self.check_major_classes(major_id="NC", major_file="Majors/compsci.dat"))
        non_major_ids.update(self.check_major_classes(major_id="6B", major_file="Majors/humanserv.dat"))
        non_major_ids.update(self.check_major_classes(major_id="UC05", major_file="Majors/archeology.dat"))
        non_major_ids.update(self.check_major_classes(major_id="2D", major_file="Majors/theatre.dat"))
        count, pos, num = 0.0, 0.0, 0.0
        for i in range(NUM_TESTS):
            student_id, sample_val = random.choice(non_major_ids.items())
            #sample_ids = set(random.sample(sample_ids, 1))
            c, p, n = self.horting_exclude_num(num=len(sample_val[0]), student_id=student_id, sample_ids=sample_val[0], hort_courses=sample_val[1])
            logging.debug("Round %i: accuracy: %2.2f, position: %2.2f", i, float(c) / n, float(p) / n)
            count += c
            pos += p
            num += n
        logging.info(">>> Test Result: %2.2f accuracy, %2.2f avg position", count / num, pos / count)
        logging.info(LINE)
        self.assert_(count / num > MIN_CORRECT)


    def testHortingExcludeOneNonMajor(self):
        """
        Test horting prediction capabilities when excluding all the major
        classes and trying to predict only electives and GURs.

        The prediction is based solely on major courses, electives and GURs have
        to predicted.

        The prediction set should not include any major courses either.

        The departments that are tested are:
        1) Accounting (DD*)
        2) Archeology (UC05)
        3) Computer Science (NC*)
        4) Human Services (6B*)
        5) Theatre (2D*)
        They represent five different colleges from Western.
        """
        logging.info("Horting Exclude One Non-Major Courses")
        non_major_ids = {} #a dict with id key and non-major classes value
        non_major_ids.update(self.check_major_classes(major_id="DD", major_file="Majors/accounting.dat"))
        non_major_ids.update(self.check_major_classes(major_id="NC", major_file="Majors/compsci.dat"))
        non_major_ids.update(self.check_major_classes(major_id="6B", major_file="Majors/humanserv.dat"))
        non_major_ids.update(self.check_major_classes(major_id="UC05", major_file="Majors/archeology.dat"))
        non_major_ids.update(self.check_major_classes(major_id="2D", major_file="Majors/theatre.dat"))
        count, pos, num = 0.0, 0.0, 0.0
        for i in range(NUM_TESTS):
            student_id, sample_val = random.choice(non_major_ids.items())
            sample_id = set(random.sample(sample_val[0], 1))
            c, p, n = self.horting_exclude_num(num=1, student_id=student_id, sample_ids=sample_id, hort_courses=sample_val[1])
            logging.debug("Round %i: accuracy: %2.2f, position: %2.2f", i, float(c) / n, float(p) / n)
            count += c
            pos += p
            num += n
        logging.info(">>> Test Result: %2.2f accuracy, %2.2f avg position", count / num, pos / count)
        logging.info(LINE)
        self.assert_(count / num > MIN_CORRECT)

if __name__ == "__main__":
    random.seed()
    setup_logging("test_non_major")
    unittest.main()
