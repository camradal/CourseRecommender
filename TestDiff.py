#!/usr/bin/env python
"""
Test how different the courses in top N items are.

Test cases for testing if the classes recommended to different students are
actually different. The tests are conducted on GURs, as well as all classes. The
statistics are written into log file.
"""

import operator
import random
import unittest

import Storage

from Common import *

class TestStudentIndex(unittest.TestCase):
    def setUp(self):
        """Setup the storage, that has student index and course index."""
        self.storage = Storage.Storage()
        self.storage.update_from_excel("tablea.xls")
        self.storage.update_from_excel("tableb.xls")
        self.storage.student_index.update_horting()

    def get_different(self, num_students, num_courses, gur_only=False):
        """Helper function for testGetDifferent."""
        #count number of different courses & course_position
        student_ids = random.sample(self.storage.student_index.student_index.keys(), num_students)
        course_count = {}
        course_pos = {}
        pop = self.storage.course_index.popular
        for student_id in student_ids:
            if gur_only:
                #logging.info("Testing GURs...")
                hort_courses = load_courses("./Test/gur_all.dat")
            else:
                #logging.info("Testing all classes...")
                hort_courses = self.storage.student_index.get_hort_courses(student_id)
            predict_ids = self.storage.student_index.get_predicted_courses_fast(student_id, hort_courses)
            for i in xrange(min(len(predict_ids), num_courses)):
                course_id, val = predict_ids[i]
                course_count[course_id] = course_count.get(course_id, 0) + 1
                course_pos[course_id] = course_count.get(course_id, 1) + i

        for k in course_pos.keys():
            course_pos[k] = float(course_pos[k]) / course_count[k]

        #totals report
        logging.info("Test: different courses in top %i of %i students", num_courses, num_students)
        logging.info("Total students: %i", len(student_ids))
        logging.info("Total predicted courses: %i", len(course_count))
        logging.info("Top %i predicted courses sorted by frequency with avg position...", num_courses)
        sorted_ids = course_count.items()
        sorted_ids.sort(key=operator.itemgetter(1), reverse=True)
        for course_id, val in sorted_ids[:num_courses]:
            logging.info("%s %i %2.2f (pop %i)", course_id, val, course_pos[course_id], pop[course_id])
            #logging.info("%s&%i&%2.2f&%i\\\\\hline", course_id, val, course_pos[course_id], pop[course_id])

        #unique recommendations report
        unique_count = 0
        half_count = 0
        ten_count = 0
        for course_id, val in sorted_ids:
            if val == 1:
                unique_count += 1
            if val <= len(student_ids) * 0.1:
                ten_count += 1
            if val <= len(student_ids) * 0.5:
                half_count += 1
        logging.info("Courses recommended to less than half of students: %i (%2.2f of total)",
                     half_count, float(half_count) / len(course_count))
        logging.info("Courses recommended to less than tenth of students: %i (%2.2f of total)",
                     ten_count, float(ten_count) / len(course_count))
        logging.info("Unique courses recommended: %i (%2.2f of total)",
                     unique_count, float(unique_count) / len(course_count))
        logging.info("Unique courses per student: %2.2f",
                     float(unique_count) / len(student_ids))

    def testGetDifferent(self):
        """
        Test how different the courses in top N items are.

        For example, how many different classes there are in top 40 of 100
        different students. Ideally, the value should be pretty high, otherwise,
        only a small group of classes gets recommended.
        """
        logging.info("Testing All Courses...")
        self.get_different(10, 10, False)
        self.get_different(20, 20, False)
        self.get_different(40, 40, False)
        self.get_different(80, 20, False)
        self.get_different(80, 40, False)
        logging.info("Testing GUR Courses...")
        self.get_different(10, 10, True)
        self.get_different(20, 20, True)
        self.get_different(40, 40, True)
        self.get_different(80, 20, True)
        self.get_different(80, 40, True)

    def tearDown(self):
        pass

if __name__ == "__main__":
    random.seed()
    setup_logging(log_file="test_diff")
    unittest.main()
