#!/usr/bin/env python
import heapq
import logging
import operator
import time

import Prediction
import Student

from Constants import *

class StudentIndex:
    """
    Index of student information by their id and directed graph connecting all
    students.

    The dictionary is organized as follows: key is student id, value is Student
    object. The graphs is organized as follows: the nodes are students ids and
    directed edges are horting.
    """

    def __init__(self):
        self.student_index = {}

    def update_student(self, student_id, course_id, major_id, course_rating=0):
        """Update student information with an added course and changed major and
        optional rating."""
        if student_id not in self.student_index:
            self.student_index[student_id] = Student.Student(student_id)
        self.student_index[student_id].add_course(course_id, course_rating)
        self.student_index[student_id].update_major(major_id)

    def get_student(self, student_id):
        """Return Student object by id."""
        return self.student_index[student_id]

    def get_students(self):
        """Return all Student objects."""
        return self.student_index.values()

    def get_courses(self, student_id):
        """Return courses student taken."""
        return self.student_index[student_id].courses

    def update_horting(self, student_id=None):
        """Update the horting set for each student in hash table or only one, if
        that student is specified."""
        #logging.debug("Updating horting between students...")
        students = self.student_index.values()
        if student_id:
            self.student_index[student_id].update_horting(students)
        else:
            for student in students:
                student.update_horting(students)

    def update_density(self, student_id):
        #logging.debug("Updating density...")
        student = self.student_index[student_id]
        horts = self.get_horts(student_id)
        #logging.debug("Student: %s", student_id)
        #logging.debug("Horts of all lengths: %i", len(horts))
        #logging.debug("Rated high: %s", student.rated_high)
        #logging.debug("Rated low: %s", student.rated_low)
        for hort_id in horts:
            courses = self.student_index[hort_id].courses
            high = len(student.rated_high & courses)
            low = len(student.rated_low & courses)
            mult =  float(high * 0.50 + 1) / (low * 0.50 + 1)
            if mult != 1:
                #logging.debug("%s: high: %2.2f, low: %2.2f, mult: %2.2f", hort_id, high, low, mult)
                student.mod_horts[hort_id] = mult

    def build_all_paths_helper(self, student_id, depth, path=[]):
        """The function that builds a list of all paths from the user to all
        horts up to specified depth."""
        path = path + [student_id]
        if len(path) > depth:
            return [path]
        paths = []
        for hort_id in self.student_index[student_id].horts:
            if hort_id not in path:
                newpaths = self.build_all_paths_helper(hort_id, depth, path)
                paths.extend(newpaths)
        return paths

    def build_all_paths(self, student_id):
        """Build paths of all depths from 1 to DEFAULT_DEPTH and put them into a
        dictionary arranged by depth."""
        paths = {}
        for i in range(1, DEFAULT_DEPTH + 1):
            paths[i] = self.build_all_paths_helper(student_id, i)
        return paths

    def build_all_paths_dijkstra(self, student_id):
        """Find all shortest paths to each hort up to certain depth using
        Dijkstra algorithm."""
        hort_dists = {} # horting distances
        paths = {student_id: [student_id]}
        seen = {student_id: 0.0}
        stack = [(student_id, 1.0)]
        pop, push, index = heapq.heappop, heapq.heappush, self.student_index
        while stack:
            (id, hort_val) = pop(stack)
            if id in hort_dists:
                continue
            hort_dists[id] = seen[id]
            if len(paths[id]) <= DEFAULT_DEPTH:
                for hort_id, horting in index[id].horts.iteritems():
                    hort_val = hort_dists[id] * horting
                    if hort_id not in seen or hort_val > seen[hort_id]:
                        seen[hort_id] = hort_val
                        push(stack, (hort_id, hort_val))
                        paths[hort_id] = paths[id] + [hort_id]
        #get all the paths and organized by length
        final = {}
        for i in range(DEFAULT_DEPTH+1):
            final[i + 1] = []
        for path in paths.itervalues():
            final[len(path)].append(path)
        #return paths.keys() #return all horts up to specified depth
        return final

    def predict_course(self, student_id, course_id, depth):
        """Predict course for the student by calculating all paths and ajdusting
        horting values."""
        predictions = []
        if ALGORITHM == ALG_DIJKSTRA:
            all_paths = self.build_all_paths_dijkstra(student_id)
        else:
            all_paths = self.build_all_paths(student_id)
        for path_len, paths in all_paths.iteritems():
            for path in paths:
                if course_id in self.student_index[path[path_len - 1]].courses:
                    p = Prediction.Prediction(student_id, course_id, path)
                    hort_val = 1.0
                    for i in xrange(path_len - 1):
                        #apply modifier if available
                        modifier = self.student_index[student_id].mod_horts.get(path[i + 1], 1.0)
                        hort_val *= self.student_index[path[i]].horts[path[i + 1]] * modifier
                    p.horting_sum = hort_val
                    predictions.append(p)
        return predictions

    def sum_predictions(self, predictions):
        """Sum all the predictions in the predictions list into one number."""
        horting_sum = 0.0
        for prediction in predictions:
            horting_sum += prediction.horting_sum
        return horting_sum

    def get_predicted_courses_fast(self, student_id, course_ids):
        """Find all predicted courses for the student from the course list,
        return sorted list."""
        predicted_courses = []
        if ALGORITHM == ALG_DIJKSTRA:
            all_paths = self.build_all_paths_dijkstra(student_id)
        else:
            all_paths = self.build_all_paths(student_id)
        #logging.debug("Prediction for %s for %i courses with %i horts", student_id, len(course_ids), len(self.get_horts(student_id)))
        for course_id in course_ids:
            sum = 0.0
            for path_len, paths in all_paths.iteritems():
                for path in paths:
                    if course_id in self.student_index[path[path_len - 1]].courses:
                        hort_val = 1.0
                        for i in xrange(path_len - 1):
                            #apply modifier if available
                            modifier = self.student_index[student_id].mod_horts.get(path[i + 1], 1.0)
                            hort_val *= self.student_index[path[i]].horts[path[i + 1]] * modifier
                        sum += hort_val
            if MIN_PREDICT_HORTING < sum < MAX_PREDICT_HORTING:
                predicted_courses.append((course_id, sum))
        predicted_courses.sort(key=operator.itemgetter(1), reverse=True)
        return predicted_courses

    def get_hort_courses_helper(self, student_id, hort_courses, depth=0):
        """
        Find courses in horting neighborhood of student.

        Only courses in neighborhood will ever be considered when searching for
        prediction for any course. So it is beneficial to exclude the rest of
        the courses from search space.
        """
        for course_id in self.student_index[student_id].courses:
            hort_courses[course_id] = hort_courses.get(course_id, 0) + 1
        if depth < DEFAULT_DEPTH:
            for hort_id in self.student_index[student_id].horts.iterkeys():
                self.get_hort_courses_helper(hort_id, hort_courses, depth+1)
        return hort_courses

    def get_hort_courses(self, student_id, limit=500):
        """Find courses in horting neighborhood of student."""
        hort_courses = self.get_hort_courses_helper(student_id, {})
        hort_list = [(c_id, c_count) for (c_id, c_count) in hort_courses.iteritems() if c_count > 1]
        hort_list.sort(key=operator.itemgetter(1), reverse=True)
        hort_list = hort_list[:limit]
        ret_list = set(c_id for (c_id, c_count) in hort_list)
        return ret_list - self.student_index[student_id].courses

    def get_horts_helper(self, student_id, horts, depth=0):
        """Find horts in neighborhood of student using recursion up to constant
        depth."""
        horts.update(self.student_index[student_id].horts)
        if depth < DEFAULT_DEPTH - 1:
            for hort_id in self.student_index[student_id].horts.keys():
                self.get_horts_helper(hort_id, horts, depth + 1)
        return horts

    def get_horts(self, student_id):
        return self.get_horts_helper(student_id, set())

    def __getitem__(self, student_id):
        """The convenience method that allows to access student index within the
        object by just accessing the object itself."""
        return self.student_index[student_id]

    def __str__(self):
        ret_str = ""
        for student in self.student_index.values():
            ret_str += str(student) + "\n"
        return ret_str
