#!/usr/bin/env python

"""
The file contains constants for controlling the program.
"""

#Rebuild cache every time the program is run
DEBUG_REBUILD = True

#Temporary storage file name, used for caching
STORAGE_CACHE = "storage_cache.tmp"

#Number of classes in common needed to be considered a hort
MIN_COMMON_CLASSES = 2

#Minimum number of classes to base prediction on
MIN_CLASSES = 2

#Minimum horting value to be considered a hort
MIN_HORTING_VALUE = 0.10

#Minimum value for class to be shown in predicted list
MIN_PREDICT_HORTING = 5.0

#Maximum value for class to be shown in predicted list
MAX_PREDICT_HORTING = 50000.0

#Maximum number of horts per student
MAX_HORTS = 100

#Default depth of search for horts. Due to very dense data, more than 2 results
#in atrocious performance.
DEFAULT_DEPTH = 2

#Top number of results where to do default search
TOP_N = 40

#Number of iterations of each test
NUM_TESTS = 100

#The minimum percentage of correctness for test to pass
MIN_CORRECT = 0.3

#Which algorithm to use for prediction: dijkstra or full. Dijkstra algorithm is
#much faster, but the results are not as accurate, since not all edges are
#exploited. Full algorithm is slower and cannot go as deep as dijkstra.
ALG_DIJKSTRA = 0
ALG_FULL = 1
ALGORITHM = ALG_FULL

#minimum students in major to generate stats for
MIN_STAT_STUDENTS = 5

#Translation table from course department abbr. to major abbr.
TRANSLATION_TABLE = {"ACCT": "DD",
                     "AMST": "XK",
                     "ANTH": "UC",
                     "ARAB": "G",
                     "ART": "2A",
                     "A/HI": "2B",
                     "ASTR": "R",
                     "BIOL": "BB",
                     "C/AM": "XJ",
                     "CHEM": "CA",
                     "CHIN": "G",
                     "CLST": "G",
                     "COMM": "CM",
                     "CSD": "VC", #Communication Sci & Disorders
                     "CSCI": "NC",
                     "CCE": "E",
                     "DNC": "2F",
                     "DSCI": "D",
                     "DSGN": "2G", #Design
                     "EAST": "XQ",
                     "ECON": "D",
                     "EDUC": "E", #Education
                     "EDAD": "E", #Educational Administration
                     "ELED": "E", #Elementary Education
                     "ETEC": "WB",
                     "ENG": "FB",
                     "ESCI": "8A", #Environmental Studies and Sciences
                     "ESTU": "8A",
                     "EXT": "E", #Extended Education
                     "FAIR": "7A", #Fairhaven, Interdisciplinary
                     "FIN": "D",
                     "FREN": "G",
                     "EGEO": "IB",
                     "GEOL": "J",
                     "GERM": "G",
                     "GREK": "G",
                     "HLED": "Q", #Health Education
                     "HIST": "KA",
                     "HNRS": None,
                     "HSP": "6B", #Human Services
                     "I T ": None, #Instructional Technology
                     "INTL": None,
                     "ITAL": "G",
                     "JAPN": "G",
                     "JOUR": "FC",
                     "LAT": "G",
                     "LBRL": "HA", #Liberal Studies, General
                     "LIBR": "None",
                     "LING": "FD",
                     "MGMT": "D",
                     "MIS": "D",
                     "MKTG": "D",
                     "MBA": "D",
                     "MATH": "NB",
                     "M/CS": "ND",
                     "LANG": "G",
                     "MUS": "2C",
                     "OPS": None,
                     "PHIL": "PA",
                     "PE": "Q",
                     "PHYS": "R",
                     "PLSC": "SA",
                     "PSY": "TB",
                     "RECR": "Q",
                     "RC": "E",
                     "RUSS": "G",
                     "SCED": ("XA", "XB", "XC", "XD"),
                     "SEC": "PB",
                     "SOC": "UB",
                     "SPAN": "G",
                     "SPED": "PB",
                     "SAA": None, #Student Affairs Administration
                     "TESL": "XE", #Teaching Eng/Second Language
                     "THTR": "2D",
                     "UNIV": None,
                     "WMNS": "XI"}

LINE = "----------------------------------------------------------------------"
