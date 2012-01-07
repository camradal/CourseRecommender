#!/usr/bin/env python
"""Controller objects for MVC."""

import os
import pickle
import time
import web

from Cheetah.Template import Template

import Prediction
import Storage

from Common import *
from Constants import *

# benchmark
t_start = time.time()

# setup logging to file and sys.stderr
setup_logging()

# setup url patterns
urls = ("/", "IndexView",
        "/Students/?", "StudentsView",
        "/Student/(\w+)/?", "StudentView",
        "/Student/(\w+)/(\w+)/?", "PredictView",
        "/Courses/?", "CoursesView",
        "/Course/(\w+)/?", "CourseView")

# setup storage, use pickling for caching
try:
    if DEBUG_REBUILD:
        try:
            os.remove(STORAGE_CACHE)
        except OSError:
            logging.info("No cache to delete")
    cache_in = open(STORAGE_CACHE, "rb")
    storage = pickle.load(cache_in)
except IOError:
    storage = Storage.Storage()
    storage.update_from_excel("tablea.xls")
    storage.update_from_excel("tableb.xls")
    storage.student_index.update_horting()
    cache_out = open(STORAGE_CACHE, "wb")
    pickle.dump(storage, cache_out)

# end benchmark
logging.info("Time to start up: %2.2f", time.time() - t_start)

class IndexView:
    def GET(self):
        t = Template(file="./Templates/IndexView.html")
        print t

class StudentView:
    """Display individual student."""
    def GET(self, student_id):
        t = Template(file="./Templates/StudentView.html")
        t_start = time.time()
        student = storage.student_index.get_student(student_id)
        hort_courses = storage.student_index.get_hort_courses(student_id)
        logging.debug("Horting search time: %2.2f, number: %i", time.time() - t_start, len(hort_courses))
        t.predicted_courses = storage.student_index.get_predicted_courses_fast(student_id, hort_courses)
        t.student = student
        logging.debug("Prediction search time: %2.2f", time.time() - t_start)
        print t

class PredictView:
    """Display individual student."""
    def GET(self, student_id, course_id):
        t = Template(file="./Templates/PredictView.html")
        predictions = storage.student_index.predict_course(student_id, course_id, DEFAULT_DEPTH)
        predictions.sort(reverse=True)
        horting_sum = storage.student_index.sum_predictions(predictions)
        t.student_id = student_id
        t.course_id = course_id
        t.predictions = predictions
        t.horting_sum = horting_sum
        # if the sum is sufficient but not too popular
        if MIN_PREDICT_HORTING < horting_sum < MAX_PREDICT_HORTING:
            t.horting_comment = "<span style=\"color: #00FF00\">Recommended</span>"
        elif horting_sum > MAX_PREDICT_HORTING:
            t.horting_comment = "<span style=\"color: #FF9900\">Recommended, but too popular</span>"
        else:
            t.horting_comment = "<span style=\"color: #FF0000\">Not recommended</span>"
        print t

class StudentsView:
    """Display all students."""
    def GET(self):
        t = Template(file="./Templates/StudentsView.html")
        students = storage.student_index.get_students()
        num_courses = [len(student.courses) for student in students]
        num_horts = [len(student.horts) for student in students]
        t.avg_courses = self.sum_list(num_courses)/len(students)
        t.avg_horts = self.sum_list(num_horts)/len(students)
        t.student_ids = [student.student_id for student in students]
        print t

    def sum_list(self, l):
        """Sums all the elements in the list."""
        return reduce(lambda x,y:x+y, l)

class CourseView:
    """Display individual course."""
    def GET(self, course_id):
        t = Template(file="./Templates/CourseView.html")
        t.course_id = course_id
        t.student_ids = storage.course_index.get_course(course_id)
        print t

class CoursesView:
    """Display all courses."""
    def GET(self):
        t = Template(file="./Templates/CoursesView.html")
        courses = storage.course_index.get_courses()
        t.course_ids = courses.keys()
        print t

web.webapi.internalerror = web.debugerror
if __name__ == "__main__":
    web.run(urls, globals())
