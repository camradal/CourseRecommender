#!/usr/bin/env python

import copy
import random
import unittest

import Storage

from Constants import TOP_N

class GenericTest(unittest.TestCase):
    def setUp(self):
        """Setup the storage, that has student index and course index."""
        self.storage = Storage.Storage()
        self.storage.update_from_db()
        self.mod_ids = self.storage.student_index.student_index.keys()
        self.storage.update_from_excel("tablea.xls")
        self.storage.update_from_excel("tableb.xls")
        self.storage.student_index.update_horting()

    def horting_exclude_num(self, num, student_id=None, hort_courses=None, sample_ids=None, modifier=False):
        """
        Test horting algorithm for arbitrary number of courses taken out of
        students curriculum.

        Also, the course list to be tested on can be specified. It can be a list
        of GURs.
        """
        #get a random student if it's not specified
        index = self.storage.student_index
        if not student_id:
            student_id = random.choice(index.student_index.keys())
        student = index[student_id]
        student_copy = copy.deepcopy(self.storage.student_index.student_index[student_id])
        #logging.debug("Student %s", student_id)

        #if classes to sample from student already provided, use them
        if sample_ids:
            course_ids = sample_ids
        #otherwise try the list of courses to choose from
        elif hort_courses:
            filtered_ids = student.courses & hort_courses
            #if num is 0, then test all courses in the list
            if num == 0:
                course_ids = filtered_ids
                num = len(course_ids)
            else:
                course_ids = set(random.sample(filtered_ids, num))
        else:
            course_ids = set(random.sample(student.courses, num))
        #logging.debug("Courses(%i): %s", len(student.courses), student.courses)
        #logging.debug("Sampled(%i): %s", len(course_ids), course_ids)

        #remove sampled courses from student
        student.courses -= course_ids
        student.rated_high -= course_ids
        student.rated_low -= course_ids
        index.update_horting(student_id)

        if modifier:
            index.update_density(student_id)

        if not hort_courses:
            hort_courses = index.get_hort_courses(student_id)
        predictions = index.get_predicted_courses_fast(student_id, hort_courses)
        #logging.debug("Hort courses(%i): %s", len(hort_courses), hort_courses)
        #logging.debug("Total predictions(%i): %s", len(predictions), predictions)
        pos, total_pos = 0, 0
        found = set()
        for pred_id, val in predictions[:TOP_N]:
            if pred_id in course_ids:
                found.add(pred_id)
                #logging.debug("Excluded course %s found at position %i with value: %f", pred_id, pos, val)
                total_pos += pos
            pos += 1
        #not_found = course_ids - found
        #if not_found:
        #logging.debug("Not found: %s %s", student_id, not_found)
        #restore student
        self.storage.student_index.student_index[student_id] = copy.deepcopy(student_copy)
        return (len(found), total_pos, num)
