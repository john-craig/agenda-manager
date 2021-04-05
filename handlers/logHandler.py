import handlers.docHandler as docHandler

"""
Semantic Functions
    Functionalities:
    -make it so that when an inactive section has a task or deed added
    to it, all of its styles are changed to active versions

    Error conditions:
    -prevent adding multiple items (tasks/deeds/etc) to a section which have
    the same string
    -prevent a method from being used on the wrong type of section by
    adding a check on the style names
    -prevent a task from being completed which is not actually in the task
    list
"""

#Returns a list of tasks for a given section
def getTasks(section):
    taskStart = docHandler.get_text_position("Tasks:", section)
    tasks = docHandler.get_list(section[taskStart:])

    return tasks

def getDeeds(section):
    deeds = docHandler.get_list(section)
    return deeds

#Adds a task to a given section
def addTask(string, section):
    emptyChar = '—'
    tasks = getTasks(section)

    #Check to see if this is the first "true" addition
    if len(tasks) == 1 and tasks[0].text == emptyChar:
        tasks[0].clear().add_run(string)
    else:
        tasks[0].insert_paragraph_before(string, style=tasks[0].style)

#Adds a deed directly to a given section
def addDeed(string, section):
    emptyChar = '—'
    deeds = getDeeds(section)

    #Check to see if this is the first "true" addition
    if len(deeds) == 1 and deeds[0].text == emptyChar:
        deeds[0].clear().add_run(string)
    else:
        deeds[0].insert_paragraph_before(string, style=deeds[0].style)

#Moves a task from "Tasks" to "Deeds"
def completeTask(string, section):
    emptyChar = '—'
    tasks = getTasks(section)

    taskIdx = docHandler.get_text_position(string, section)

    # We are completing the only task
    if len(tasks) == 1:
        addDeed(string, section)

        section[taskIdx].clear().add_run(emptyChar)
    else:
        addDeed(string, section)

        task = section[taskIdx]
        task._element.getparent().remove(task._element)

#Adds a deed to a given section
def addObjective():
    pass

#
def completeObjective():
    pass

def addGoal():
    pass

def completeGoal():
    pass


#==================

def getSectionByDay(string, document):
    contents = docHandler.get_table_contents(document)

    return docHandler.get_section(string, contents)

def getLog(path):
    return docHandler.get_document(path)


"""
    Testing
"""
#
# path = '../weekLog.docx'
# string = "Monday"
# #string = "Weekly Objectives"
#
# #paragraphs = get_body(test)
# document = docHandler.get_document(path)
# paragraphs = docHandler.get_table_contents(document)
#
# section = docHandler.get_section(string, paragraphs)
# #
# # section[0].delete()
#
# print(section[0].text)

#addTask("Test1", section)
#addTask("Test2", section)
#addDeed("Test", section)
#completeTask("Test1", section)
#graph = section[2].insert_paragraph_before("Test",style=WD_STYLE.LIST_BULLET)
#
# graph.style = section[2].style
# #graph.paragraph_format = section[2].paragraph_format
#
#test.save(path)
#
# doc = Document(path)
# paragraphs = doc.paragraphs
# sections = doc.sections
