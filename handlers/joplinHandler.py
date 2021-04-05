from joplin_api import JoplinApi
import asyncio, httpx, json
import os

# joplin auth token
# 80376f6f0db4ca234402e06204a046083e69d22e7f0181c4226a48ce6f366fceefdb8ae644f5d67fcd699b5f2135c1cde9e884b29d325dcd5abd6c6988c1a286

TOKEN = "80376f6f0db4ca234402e06204a046083e69d22e7f0181c4226a48ce6f366fceefdb8ae644f5d67fcd699b5f2135c1cde9e884b29d325dcd5abd6c6988c1a286"


# for later--

# import os
# f=os.popen("ls -l")
# for i in f.readlines():
#      print "myresult:",i,

# https://linux.byexamples.com/archives/366/python-how-to-run-a-command-line-within-python/

def synchonize():
    os.popen("joplin sync")


def get_notebook_entries(notebook):
    entries = []

    os.popen("joplin use '" + notebook + "'")
    ids = get_notebook_ids(notebook)

    for id in ids:
        entry = __strings_to_dict__(
            os.popen("joplin cat " + id + " -v").readlines()
        )

        entry['tags'] = __parse_tags__(
            os.popen("joplin tag notetags " + id).readlines()
        )

        entries.append(entry)

    return entries

def add_notebook_entry(notebook, title):
    os.popen("joplin use '" + notebook + "'")

    os.popen("joplin mktodo " + title)

def remove_notebook_entry(notebook, title):
    os.popen("joplin use '" + notebook + "'")
    id = get_note_id(title)

    os.popen("joplin rmnote " + id)

def set_notebook_entry_tags(notebook, title, new_tags):
    os.popen("joplin use '" + notebook + "'")
    id = get_note_id(title)

    prev_tags = __parse_tags__(
        os.popen("joplin tag notetags " + id ).readlines()
    )

    for tag in prev_tags:
        os.popen("joplin tag remove " + tag + " " + id)

    for tag in new_tags:
        os.popen("joplin tag add " + tag + " " + id)

"""
    Utilities
"""

def get_notebook_ids(notebook):
    result = os.popen("joplin ls -l")
    ids = []

    for string in result:
        tokens = list(string.split(' '))
        ids.append(tokens[0])

    return ids



def get_note_id(title):
    result = os.popen("joplin ls -l")
    id = None

    for string in result:
        if string.find(title) != -1:
            id = list(string.split(' '))[0]

    return id



def __parse_tags__(lines):
    tags = []

    for line in lines:
        tags.append(line[:-1])

    return tags

def __parse_ids__(lines):
    ids = []

    for line in lines:
        ids.append(list(line.split(' '))[0])

    return ids

def __strings_to_dict__(lines):
    entry = {}

    for line in lines:
        #Trim off ending '\n'
        line = line[:-1]
        fragments = list(line.split(": "))

        if len(fragments) == 1:
            if fragments[0] != '':
                entry['title'] = fragments[0]
        else:
            entry[fragments[0]] = fragments[1]


    return entry



def get_tasks():
    joplin = JoplinApi(token=TOKEN)
    taskFolder = None
    taskNotes = None

    loop = asyncio.get_event_loop()
    try:
        taskFolder = loop.run_until_complete(get_folder_by_name("Tasks", joplin))

        taskNotes = loop.run_until_complete(get_folder_notes(taskFolder['id'], joplin))
    finally:
        loop.close()

    return taskNotes





#
async def get_folder_by_name(name, connection):
    folders = await connection.get_folders()

    #await connection.client.aclose()

    folders = folders.json()['items']
    by_name = lambda folder : folder['title'] == name

    return list(filter(by_name, folders))[0]


async def get_folder_notes(folder_id, connection):
    notes = await connection.get_folders_notes(folder_id)

    await connection.client.aclose()

    return notes.json()


# get_notes and get_folders both return a full list of the folders and notes
async def print_notes():
    response = await joplin.get_folders().json()

    await joplin.client.aclose()

    return response
