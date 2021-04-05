import handlers.logHandler as logHandler
import handlers.dateHandler as dateHandler
import handlers.ledgerHandler as ledgerHandler
import handlers.joplinHandler as noteHandler

from objects.Log import Log
from objects.Notes import Notes

def addLogTask(date, string):
    pass

def getLogTasks(date):
    pass

def addLogDeed(date, string):
    pass

def getLogDeeds(date):
    pass

def completeLogTask(date, string):
    pass

#===========

## TODO: add exception handling
def manageTask(note):
    log = getLogByNote(note)
    section = getDaySection(note, log)

    tasks = logHandler.getTasks(section)
    deeds = logHandler.getDeeds(section)

    inTasks = matchGraphsNote(tasks, note)
    inDeeds = matchGraphsNote(deeds, note)

    isComplete = bool(note['todo_completed'])

    if isComplete:
        if inTasks:
            #This means note is marked as complete in Joplin
            #but it is not a Deed in the Log yet
            logHandler.completeTask(note['title'], section)
        elif inDeeds:
            #The note is marked as complete in Joplin and
            #as complete in the Log -- the note can
            #safely be deleted
            pass
        else:
            #The note is marked as complete in Joplin but
            #it is listed as neither a Deed or a Task in
            #the Log; thus, add it as a Deed
            logHandler.addDeed(note['title'], section)

        #Technically the note should be deleted in all cases
        #here
    else:
        if inTasks:
            #This means the note is incomplete and
            #it is listed as a Task in the log,
            #thus, nothing needs to happen
            pass
        elif inDeeds:
            #This means the note is marked as incomplete
            #in Joplin but is listed under Deeds in the
            #Log. This suggests I manually added it as
            #a Deed. Thus it should be deleted from
            #Joplin.
            pass
        else:
            #This means it is marked incomplete in Joplin
            #but is not in the Deeds or the Tasks of a
            #Log. Thus, add it as a Task.
            logHandler.addTask(note['title'], section)

    saveLogByNote(log, note)




def matchGraphsNote(graphs, note):
    match = False

    for graph in graphs:
        if graph.text == note['title']:
            match = True

    return match


#===========


def getDaySection(note, log):
    date = dateHandler.stringToDate(note['todo_due'])
    day = dateHandler.getDayName(date.weekday())

    return logHandler.getSectionByDay(day, log)

def getLogByNote(note):
    date = dateHandler.stringToDate(note['todo_due'])
    path = ledgerHandler.getWeekLogByDate(date)

    #print(path)

    return logHandler.getLog(path)

def saveLogByNote(log, note):
    date = dateHandler.stringToDate(note['todo_due'])
    path = ledgerHandler.getWeekLogByDate(date)

    log.save(path)

#===========

def determine_differences(itemListA, itemListB):
    differences = []
    foundListA = []
    foundListB = []

    for itemA in itemListA:
        for itemB in itemListB:
            comparison = compare_items(
                itemA,
                itemB
            )

            if comparison == 1:
                foundListA.append(itemA)
                foundListB.append(itemB)

            if comparison == -1:
                foundListA.append(itemA)
                foundListB.append(itemB)

                differences.append(
                    (itemA, itemB)
                )



    for itemA in itemListA:
        if itemA not in foundListA:
            differences.append((itemA, None))

    for itemB in itemListB:
        if itemB not in foundListB:
            differences.append((None, itemB))

    return differences

"""
    Specifications:
        -completed note items should generally be removed
        -
        -
"""
def resolve_differences(differences, log, notes):
    #Difference resolution
    for difference in differences:
        #This means there is a Note item for which there is no Log Item
        if difference[0] == None:
            log.add_item(difference[1])
        #This means there is a Log item for which is no Note
        elif difference[1] == None:
            #In theory I should add this method into here but...meh
            pass
        #This means there is another difference
        else:
            #There is a discrepancy in the completion status
            if difference[0]['completed'] != difference[1]['completed']:
                #The Note item is marked complete
                if difference[1]['completed']:
                    log.complete_item(difference[0])

                notes.remove_item(difference[1])
            #There is a discrepancy in the date
            elif difference[0]['date'] != difference[1]['date']:
                #Not sure how to resolve this but the case is here
                pass
            #There is a discrepancy in the scope of the items
            elif difference[0]['scope'] != difference[1]['scope']:
                #Not sure how to resolve this but the case is here
                pass

# Returns 1 if exactly identical
# Returns 0 if different title
# Returns -1 same title but other differences
def compare_items(itemA, itemB):
    comparison = 0

    if itemA['title'] == itemB['title']:
        comparison = 1

        if itemA['completed'] != itemB['completed']:
            comparison = -1

    # if itemA['date'] != itemB['date']:
    #     comparison *= -1

    return comparison


#===========

#Update the Agenda of the Log
def run():
    log = Log()
    notes = Notes()

    differences = determine_differences(
        log.get_items(),
        notes.get_items()
    )

    resolve_differences(differences, log, notes)




def update():
    date = dateHandler.getToday()

    notes = Note()
    notes.get_items()

    # log = Log(date)
    # print(log.get_items(date))

#Fetch the Agenda of the current Day
def fetch():
    date = dateHandler.getToday()
    log = Log(date)

    month_items = log.get_items(scope='month')
    week_items = log.get_items(scope='week')
    day_items = log.get_items(date, 'day')

    agendaString = "Month Goals: \n"

    for item in month_items:
        agendaString = agendaString + "\t -" + item['title'] + "\n"

    agendaString += "\nWeek Objectives: \n"

    for item in week_items:
        agendaString = agendaString + "\t -" + item['title'] + "\n"

    agendaString += "\nDaily Tasks: \n"

    for item in day_items:
        agendaString = agendaString + "\t -" + item['title'] + "\n"

    return agendaString
