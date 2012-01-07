#!/usr/bin/env python
import operator

class CourseIndex:
    """
    Inverted index of students associated with courses.

    The index is implemented using a dictionary as follows: Key is course id.
    Value is a set of all students who have taken the class. Therefore, if
    student has attempted the class numerous time, only one attempt will be
    shown.
    """

    def __init__(self):
        self.inv_index = {}

    def add_student(self, student_id, course_id):
        """Add a student to a course in inverted index."""
        if course_id not in self.inv_index:
            self.inv_index[course_id] = set()
        self.inv_index[course_id].add(student_id)

    def get_course(self, course_id):
        """Return information about a course."""
        return self.inv_index[course_id]

    def get_courses(self):
        """Return information about all courses."""
        return self.inv_index

    def get_popular(self):
        """Return most popular courses arranged by number of students."""
        pop_list = []
        pop_dict = {}
        for course_id, students in self.inv_index.iteritems():
            pop_list.append((course_id, len(students)))
        pop_list.sort(key=operator.itemgetter(1), reverse=True)
        for i, course in enumerate(pop_list):
            pop_dict[course[0]] = i
        return pop_dict

    def __str__(self):
        ret_str = ""
        for course_id, students in self.inv_index.items():
            ret_str += "Course ID: %s\n" % course_id
            ret_str += "Student list (%i):\n" % len(students)
            for student_id in students:
                ret_str += str(student_id) + " "
            ret_str += "\n"
        return ret_str

    #properties
    popular = property(fget=get_popular, doc="Most popular courses arranged by number of students.")
