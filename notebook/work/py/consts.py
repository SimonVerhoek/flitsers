import calendar
import pathlib

"""
Date and time related
"""
DAYS_OF_WEEK = list(calendar.day_name)

MONTHS_OF_YEAR = list(calendar.month_name)[1:]


"""
File and directory related
"""
ROOT_DIR = pathlib.Path().resolve()
DATA_DIR = ROOT_DIR / "data"
WORK_DIR = ROOT_DIR / "work"
