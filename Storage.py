#!/usr/bin/env python

import logging
import md5
import pg
import pgdb
import xlrd

import CourseIndex
import StudentIndex

class Storage:
    """Storage reads information from disk or database and saves the state"""
    def __init__(self):
        """Open or create storage"""
        self.course_index = CourseIndex.CourseIndex()
        self.student_index = StudentIndex.StudentIndex()

    def update_from_db(self):
        """
        Update storage from database.

        Be sure to fill in right arguments within the code.
        """
        try:
            logging.info("Reading database...")
            conn = pgdb.connect(dsn="localhost:postgres",
                                user="postgres",
                                password="secret",
                                database="postgres")
            cursor = conn.cursor()
            cursor.execute("SELECT email, major, status, course_id, rating FROM survey")
            rows = cursor.fetchall()
            for row in rows:
                #there's no student id, will use email instead
                student_id = md5.new(row[0]).hexdigest()
                self.course_index.add_student(student_id, row[3])
                self.student_index.update_student(student_id, row[3], row[1], row[4])
        except pg.Error:
            logging.error("Database update failed")
        finally:
            conn.close()

    def update_from_excel(self, filename):
        """Read Excel file and update information in indexes"""
        logging.info("Reading file %s...", filename)
        try:
            book = xlrd.open_workbook(filename)
        except IOError:
            logging.error("Can't read file %s", filename)
        else:
            worksheet = book.sheet_by_index(0)
            for i in range(1, worksheet.nrows):
                #student_id = md5.new(worksheet.cell_value(i, 0)).hexdigest()
                student_id = worksheet.cell_value(i, 0)
                #date = worksheet.cell_value(i, 1)
                #status = worksheet.cell_value(i, 2)
                try:
                    major_id = str(int(worksheet.cell_value(i, 3)))
                except ValueError:
                    major_id = worksheet.cell_value(i, 3)
                try:
                    course_num = int(worksheet.cell_value(i, 5))
                except ValueError:
                    course_num = worksheet.cell_value(i, 5)
                finally:
                    course_id = "%s%s" % (worksheet.cell_value(i, 4), course_num)
                self.course_index.add_student(student_id, course_id)
                self.student_index.update_student(student_id, course_id, major_id)
