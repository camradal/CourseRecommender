#!/usr/bin/env python
import operator

from Constants import MIN_COMMON_CLASSES, MIN_HORTING_VALUE, MAX_HORTS

class Student:
    """
    Student class represents a memory model of student.

    Major represented as a string. Course history, high rated classes and low
    rated classes are sets. Horts is a hash table organized by student id and
    horting value.
    """
    def __init__(self, student_id):
        self.student_id = student_id
        self.major_id = ""
        self.courses = set()
        self.rated_high = set()
        self.rated_low = set()
        self.horts = {}
        self.mod_horts = {}

    def add_course(self, course_id, rating=0):
        """Add course to student, including rating."""
        self.courses.add(course_id)
        if rating == 1:
            self.rated_high.add(course_id)
        elif rating == -1:
            self.rated_low.add(course_id)

    def update_major(self, major_id):
        self.major_id = major_id

    def get_horting(self, other):
        """Return the horting value for candidate student if it is contained in
        horting set."""
        if isinstance(other, Student):
            return self.horts.get(other.student_id, 0)
        else:
            return self.horts.get(other, 0)

    def update_horting(self, candidates):
        """
        Update horting set for current student using the candidate(s) provided.

        The number of maximum horts is set in constant file and limited by
        default to provide for uniform prediction performance between students.
        """
        hort_list = []
        num_courses = len(self.courses)
        if isinstance(candidates, Student):
            candidates = [candidates]
        for candidate in candidates:
            num_common = len(self.courses & candidate.courses)
            if num_common >= MIN_COMMON_CLASSES:
                hort_value = float(num_common) / num_courses
                if hort_value >= MIN_HORTING_VALUE:
                    hort_list.append((candidate.student_id, hort_value))
        hort_list.sort(key=operator.itemgetter(1), reverse=True)
        self.horts = dict(hort_list[:MAX_HORTS])

    def __str__(self):
        ret_str = "Student ID: %s\n" % self.student_id
        ret_str += "Major ID: %s\n" % self.major_id
        ret_str += "Course Set (%i):\n" % len(self.courses)
        for course in self.courses:
            ret_str += str(course) + " "
        ret_str += "\n"
        ret_str += "Horting Set (%i):\n" % len(self.horts)
        for hort_id, hort_value in self.horts.items():
            ret_str += "%s(%f) " % (hort_id, hort_value)
        return ret_str + "\n"
