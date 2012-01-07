#!/usr/bin/env python

class Prediction():
    """Contains information about a prediction for a course for student."""
    def __init__(self, student_id, course_id, path):
        self.student_id = student_id
        self.course_id = course_id
        self.path = path
        self.horting_path = []
        self.horting_sum = 1.0

    def __cmp__(self, other):
        """Compare predictions using horting sum."""
        return cmp(self.horting_sum, other.horting_sum)

    def __str__(self):
        str = "Predict %s for %s\n" % (self.course_id, self.student_id)
        str += "Path: " 
        for p in self.path:
            str += "%s -> " % p
        str += "\nHorting path: "
        for p in self.horting_path:
            str += "%2.2f -> " % p
        str += "\nHorting value %2.2f\n" % self.horting_sum
        return str
