import calendar
import pathlib
from datetime import datetime, timedelta


"""
Date and time related
"""
HOURS_OF_DAY = [h for h in range(0, 24)]

DAYS_OF_WEEK = list(calendar.day_name)

MONTHS_OF_YEAR = list(calendar.month_name)[1:]

TOMORROW: datetime = datetime.now() + timedelta(days=1)
TOMORROW_DAY: str = TOMORROW.strftime("%A")
TOMORROW_MONTH: str = TOMORROW.strftime("%B")
TOMORROW_YEAR: str = TOMORROW.strftime("%Y")


"""
File and directory related
"""
ROOT_DIR = pathlib.Path("..")
DATA_DIR = ROOT_DIR / "data"
WORK_DIR = ROOT_DIR / "work"


"""
Data related
"""
SIDES = ["links", "rechts", "beide"]
