import os, shutil
import handlers.dateHandler as dateHandler
BASE_PATH= "/home/iranon/ledger/"

# Return a path to the week log corresponding to a specific date object
def getWeekLogByDate(date):
    path = getMonthLedgerByDate(date) + "/logs/"

    weekNum = dateHandler.getWeekNumber(date) + 1
    path = path + "weekLog" + str(weekNum) + ".docx"

    return path


# Return a path to a week log corresponding to a specific date object
def getWeekRecordByDate(date):
    path = getMonthLedgerByDate(date) + "/records/"

    weekNum = dateHandler.getWeekNumber(date) + 1
    path = path + "weekRecord" + str(weekNum) + ".xlsx"

    return path

def getWeekRegimenByDate(date):
    path = getMonthLedgerByDate(date) + "/records/regimens/"

    weekNum = dateHandler.getWeekNumber(date) + 1
    path = path + "weekRegimen" + str(weekNum) + ".xlsx"

    return path

def getWeekNutritionByDate(date):
    path = getMonthLedgerByDate(date) + "/records/nutrition/"

    weekNum = dateHandler.getWeekNumber(date) + 1
    path = path + "weekNutrition" + str(weekNum) + ".xlsx"

    return path


def getWeekBudgetByDate(date):
    path = getMonthLedgerByDate(date) + "/budgets/"

    weekNum = dateHandler.getWeekNumber(date) + 1
    path = path + "weekBudget" + str(weekNum) + ".xlsx"

    return path

def getMonthLedgerByDate(date):
    path = BASE_PATH + str(date.year)

    path = path + "/" + dateHandler.getMonthName(
        dateHandler.getMonth(date, technical=True)
    ).lower()

    # print(path)

    return path
