import handlers.joplinHandler as joplinHandler
import handlers.dateHandler as dateHandler

class Notes:
    """
        In the future this constructor should:
            -start a joplin server instead of interacting with the CLI... or, better yet, read straight
            from markdown files
            -update the date tags on all current tasks
            -move tasks past their due date (or maybe past their week) back to the Queue
    """
    def __init__(self):
        joplinHandler.synchonize()


    def get_items(self):
        items = self.__note_to_dict__(
            joplinHandler.get_notebook_entries("Tasks")
        )

        items = self.sort_items(items)

        joplinHandler.synchonize()

        return items


    def add_item(self, item):
        pass

    def remove_item(self, item):
        pass


    # Sort a list of dictionaries
    def sort_items(self, items):
        byDate = lambda item : item['date']

        return sorted(items, key=byDate)


    def __note_to_dict__(self, notes):
        items = []

        for note in notes:
            # Make sure each of the notes we recieved was a todo, and has some sort of tag
            if note['is_todo'] == '1' and len(note['tags']) > 0:
                """
                    For future reference, the 'todo_completed' actually
                    sets a date/time for the completion, which could
                    be useful for the future.
                """
                item = {
                    'title': note['title'],
                    'completed': note['todo_completed'] != '0',
                    #'date': dateHandler.setWeekDay('sunday', self.date),
                    'scope': 'day'
                }

                date = dateHandler.confirmDateFormat(note['tags'][0])

                if date is not note['tags'][0]:
                    joplinHandler.set_notebook_entry_tags("Tasks", item['title'], [date])
                elif date == "":
                    pass #Parsing failed

                item['date'] = dateHandler.stringToDate(date)

                items.append(item)

        return items
