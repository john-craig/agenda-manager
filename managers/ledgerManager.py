import handlers.dateHandler as dateHandler
import handlers.ledgerHandler as ledgerHandler
import os, shutil

TEMPLATE_PATH = '/home/iranon/sync/ledger/references/templates'
LEDGER_PATH = '/home/iranon/sync/ledger'

only_directories = lambda item: item.is_dir()
only_files = lambda item: not item.is_dir()

def expandMonthLedger(path, numWeeks=None):
    if not numWeeks:
        numWeeks = len(dateHandler.getWeekRanges())

    # Create a file for each week named appropriately
    files = filter(only_files, os.scandir(path))

    for file in files:
        baseName = file.name

        """
            To Do:
                with five-week months, determine if the extra
                week should be a week 0 or a week 5
        """
        for i in range(0, numWeeks):
            dotPos = baseName.find('.')
            curName = baseName[:dotPos] + str(i + 1) + baseName[dotPos:]

            shutil.copy(path + '/' + baseName, path + '/' + curName)

        os.remove(path + '/' + baseName)


    # Call expandMonth on subdirectories
    directories = filter(only_directories, os.scandir(path))

    for directory in directories:
        expandMonthLedger(path + "/" + directory.name, numWeeks)

def handleMonthLedger():
    year = str(dateHandler.getYear())
    month = dateHandler.getMonth()

    nextMonthName = dateHandler.getMonthName(month + 1) if month < 12 else dateHandler.getMonthName(1)
    nextMonthName = nextMonthName.lower()

    yearPath = LEDGER_PATH + "/" + year
    monthPath = yearPath + "/" + nextMonthName

    # Make sure target directory is empty
    #os.rmdir(monthPath)

    # Copy from the template
    shutil.copytree(TEMPLATE_PATH + "/monthLedger", monthPath, dirs_exist_ok=True)

    expandMonthLedger(monthPath + '/logs')
    expandMonthLedger(monthPath + '/records')
    expandMonthLedger(monthPath + '/budgets')


def run():
    handleMonthLedger()

def fetch(option):
    date = dateHandler.getToday()

    if option == 'log':
        path = ledgerHandler.getWeekLogByDate(date)
    elif option == 'record':
        path = ledgerHandler.getWeekRecordByDate(date)
    elif option == 'regimen':
        path = ledgerHandler.getWeekRegimenByDate(date)
    elif option == 'nutrition':
        path = ledgerHandler.getWeekNutritionByDate(date)
    elif option == 'budget':
        path = ledgerHandler.getWeekBudgetByDate(date)

    return path
