#!/usr/bin/env python
"""Performance profiling."""

import cProfile
import logging
import os
import pickle
import time

import Storage

from Constants import DEBUG_REBUILD, STORAGE_CACHE
from Common import setup_logging

#setup logging to file and console
setup_logging(log_file="profiler_log.txt", console_output=True)

# setup storage, use pickling for caching
try:
    if DEBUG_REBUILD:
        try:
            os.remove(STORAGE_CACHE)
        except OSError:
            logging.info("No cache to delete")
    cache_in = open(STORAGE_CACHE, "rb")
    storage = pickle.load(cache_in)
except:
    storage = Storage.Storage()
    storage.update_from_excel("tablea.xls")
    storage.update_from_excel("tableb.xls")
    storage.student_index.update_horting()
    cache_out = open(STORAGE_CACHE, "wb")
    pickle.dump(storage, cache_out)

def test_fun():
    t_start = time.time()
    student_id = "W00491416"
    index = storage.student_index
    hort_courses = index.get_hort_courses(student_id)
    logging.debug("Horting search time: %2.2f, number: %i",
                  time.time() - t_start, len(hort_courses))
    predicted_courses = index.get_predicted_courses_fast(student_id, hort_courses)
    logging.debug("Prediction search time: %2.2f", time.time() - t_start)

if __name__ == "__main__":
    cProfile.run("test_fun()")
