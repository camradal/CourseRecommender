#!/usr/bin/env python
"""
Common fuctions used through the Class Recommender project.
"""

import logging
import operator
import time
import xlrd

from Constants import *

def sum_list(l):
    """Sums all the elements in the list."""
    return reduce(operator.add, l)

def mul_list(l):
    return reduce(operator.mul, l)

def setup_logging(log_file="log.txt", console_output=True, print_header=True):
    """Setup logging destination and format with optional console output and
    header."""
    #use name mangling if name is not provided
    if not log_file.endswith(".txt"):
        if ALGORITHM == ALG_DIJKSTRA:
            log_file = "%s_%s_%s_dijkstra.txt" %(log_file, TOP_N, NUM_TESTS)
        else:
            log_file = "%s_%s_%s_full.txt" %(log_file, TOP_N, NUM_TESTS)

    logging.basicConfig(level=logging.DEBUG,
                        format="%(asctime)s %(levelname)s %(message)s",
                        filename="./Logs/%s" % log_file,
                        filemode="w")
    if console_output:
        console = logging.StreamHandler()
        logging.getLogger().addHandler(console)
    if print_header:
        logging.info(LINE)
        logging.info("Log file: %s", log_file)
        logging.info("Rebuild index: %s", DEBUG_REBUILD)
        logging.info("Minimum number of classes: %i", MIN_COMMON_CLASSES)
        logging.info("Minimum horting value: %2.2f", MIN_HORTING_VALUE)
        logging.info("Minimum value for prediction: %2.2f", MIN_PREDICT_HORTING)
        logging.info("Maximum value for prediction: %2.2f", MAX_PREDICT_HORTING)
        logging.info("Maximum number of horts: %i", MAX_HORTS)
        logging.info("Default depth of search: %i", DEFAULT_DEPTH)
        logging.info("Number of top predictions: %i", TOP_N)
        logging.info("Number of test runs: %i", NUM_TESTS)
        logging.info("Minimum accepted percentage: %2.2f", MIN_CORRECT)
        if ALGORITHM == ALG_DIJKSTRA:
            logging.info("Algorithm: Dijkstra")
        else:
            logging.info("Algorithm: Full")
        logging.info(LINE)


def load_courses(filename):
    """
    Read courses from the text file and return them in a set.

    The function is used to load the list of GURs or other classes to
    recommend. The format of files is one class per line. The # signifies
    the comment. """
    course_ids = set()
    try:
        in_file = open(filename, mode="r")
        for line in in_file:
            if line and not line.startswith("#"):
                course_ids.add(line.strip())
    except IOError:
        logging.error("Can't read file %s", filename)
    finally:
        in_file.close()
    return course_ids

def load_major_names(filename="majors.xls"):
    """Load major names from excel file and return them in dictionary."""
    m_names = {}
    try:
        book = xlrd.open_workbook(filename)
        worksheet = book.sheet_by_index(0)
        for i in range(1, worksheet.nrows):
            try:
                major_id = str(int(worksheet.cell_value(i, 0)))
            except ValueError:
                major_id = worksheet.cell_value(i, 0)
            m_names[major_id] = worksheet.cell_value(i, 1)
    except IOError:
        logging.error("Can't read file %s", filename)
    return m_names

def reverse_dict(d):
    """Reverse dictionary so keys are values and values are keys."""
    new_d = {}
    for key, val in d:
        if val:
            new_d[val] = key
    return new_d
