import handlers.docHandler as docHandler
import handlers.ledgerHandler as ledgerHandler
import handlers.dateHandler as dateHandler

class Log:
    HEADER_LABELS = ("Week Objectives", "Month Goals")
    BODY_LABELS = (
        "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday",
    )

    def __init__(self, date=None, path=None):
        self.date = date if date else dateHandler.getToday()
        self.path = path if path else ledgerHandler.getWeekLogByDate(self.date)
        self.document = docHandler.get_document(self.path)


    def get_items(self, date=None, scope=None):
        #Note -- there should be an exception here for when a date is requested entirely outside
        #of the date that was used to create this
        items = []
        sections = self.get_sections()

        for section in sections:
            #Only return items with the corresponding scope and date
            if scope and date:
                for entry in section['items']:
                    if entry['date'] == date and entry['scope'] == scope:
                        items.append(entry)
            #Only return items with the corresponding scope, regardless of their date
            elif scope and not date:
                for entry in section['items']:
                    if entry['scope'] == scope:
                        items.append(entry)
            #Only return items of a corresponding date, regardless of their scope
            #This will generally miss the weekly and monthly items, because their dates
            #are set for sunday
            elif not scope and date:
                for entry in section['items']:
                    if entry['date'] == date:
                        items.append(entry)
            # No qualifiers, return everything
            else:
                items = items + section['items']

        items = self.sort_items(items)

        return items


    def add_item(self, item):
        label = self.get_item_label(item)
        section = self.get_section(label, as_dict=False)

        if item['scope'] == "month":
            pass
        elif item['scope'] == "week":
            pass
        elif item['scope'] == "day":
            emptyChar = '—'
            prevGraph = None

            checkString = "Deeds" if item['completed'] else "Tasks"

            for i in range(0, len(section)):
                if section[i].text.find(checkString) != -1:
                    prevGraph = section[i + 1] if not prevGraph else prevGraph

            #Check to see if this is the first "true" addition
            if prevGraph.text.find(emptyChar) != -1:
                prevGraph.clear().add_run(item['title'])
            else:
                prevGraph.insert_paragraph_before(item['title'], style=prevGraph.style)

        #self.__update_doc__()

    def complete_item(self, item):
        label = self.get_item_label(item)
        section = self.get_section(label, as_dict=False)

        for graph in section:
            print(graph.text)

        if item['scope'] == "month":
            pass
        elif item['scope'] == "week":
            pass
        elif item['scope'] == "day":
            emptyChar = '—'
            curGraph = None

            """
                Add the item as a deed
            """

            #Find the graph after the "Deeds" sublabel
            prevGraph = None

            for i in range(0, len(section)):
                if section[i].text.find("Deeds") != -1:
                    prevGraph = section[i + 1]

            #Append or alter the previous graph
            if prevGraph.text.find(emptyChar) != -1:
                prevGraph.clear().add_run(item['title'])
            else:
                prevGraph.insert_paragraph_before(item['title'], style=prevGraph.style)

            """
                Remove it as a task
            """

            #Find the graph corresponding to the item
            for i in range(0, len(section)):
                if section[i].text.find(item['title']) != -1:
                    curGraph = section[i]

            #Remove or reset the current graph
            if section.index(curGraph) == len(section) - 1:
                curGraph.clear().add_run(emptyChar)
            else:
                curGraph._element.getparent().remove(curGraph._element)

        self.__update_doc__()



    # Sort a list of dictionaries
    def sort_items(self, items):
        byDate = lambda item : item['date']

        return sorted(items, key=byDate)


    #Checks if the item actually falls in this week
    def is_correct_week(item):
        return True

    #Return all sections contained
    def get_sections(self):
        sections = []

        for label in Log.HEADER_LABELS:
            sections.append(self.get_section(label))

        for label in Log.BODY_LABELS:
            sections.append(self.get_section(label))

        return sections

    def get_section(self, label, as_dict=True):
        section = {}
        contents = []

        if(label in Log.HEADER_LABELS):
            contents = docHandler.get_header(self.document)
            section = docHandler.get_section(
                label,
                "",
                contents
            )

        if(label in Log.BODY_LABELS):
            contents = docHandler.get_table_contents(self.document)
            section = docHandler.get_section(
                label,
                "",
                contents
            )

        if as_dict:
            section = self.__graph_to_dict__(section)

        return section

    # Searchers

    #Returns the label of the section in which the item is found
    #returns an empty string otherwise
    def find_section(self, item):
        section = ""

        for label in Log.HEADER_LABELS:
            section = self.get_section(label)

            if in_section(item, section):
                if section == "":
                    section = label
                else:
                    raise Error("There was a duplicate item found in %s", self.path)

        for label in Log.BODY_LABELS:
            section = self.get_section(label)

            if in_section(item, section):
                if section == "":
                    section = label
                else:
                    raise Error("There was a duplicate item found in %s", self.path)

        return section

    # Determines if an item is in a section
    def in_section(self, item, section):
        found = False

        for entry in section['items']:
            found = found or entry['title'] == item['title']

        return found

    #Determines the label to be used for an item
    def get_item_label(self, item):
        label = ""

        if item['scope'] == "month":
            label = Log.HEADER_LABELS[1]
        elif item['scope'] == "week":
            label = Log.HEADER_LABELS[0]
        elif item['scope'] == "day":
            label = Log.BODY_LABELS[
                item['date'].weekday()
            ]
        else:
            #Something went wrong!
            pass

        return label

    # Private methods

    def __item_to_label__(self, item):
        label = ""

        if item['scope'] == "month":
            label = Log.HEADER_LABELS[1]
        elif item['scope'] == "week":
            label = Log.HEADER_LABELS[0]
        elif item['scope'] == "day":
            day = item['date'].weekday()

            # weekday() returns the day of the week in the order: sunday, monday, tuesday, wednesday... saturday; with sunday as 0 and saturday as 6
            # I have the days stored as monday, tuesday, wednesday... saturday, sunday, with monday as 0 and sunday as 6
            # a lesser programmer would need more than one line to convert these. I am not a lesser programmer.
            label = Log.BODY_LABELS[day - 1] if day > 0 and day < 6 else Log.BODY_LABELS[5 + (1 -(day / 6))]
        else:
            raise Error("The item %s had unexpected scope %", item['title'], item['scope'])

        return label

    def __graph_to_dict__(self, graphs):
        dict = {}
        dict['items'] = []

        if len(graphs) > 0:
            dict['label'] = graphs[0].text

            if(graphs[0].style.name == "Month Label"):
                listStyles = ('Incomplete Item','Complete Item')

                #For each graph in the list after the label
                for i in range(1, len(graphs)):
                    graph = graphs[i]

                    #If it is a list item, append it to the items array
                    if(graph.style.name in listStyles):
                        #Confirm item is not an emdash
                        if(graph.text.find("—") == -1):
                            #Set completion status based on whether the style is 'Incomplete Item' or 'Complete Item'
                            dict['items'].append({
                                'title': graph.text,
                                'completed': graph.style.name == listStyles[1],
                                'date': dateHandler.setWeekDay('sunday', self.date),
                                'scope': 'month'
                            })

            graphs[0].style.name == "Week Label"
            if ():
                listStyles = ('Incomplete Item','Complete Item')

                #For each graph in the list after the label
                for i in range(1, len(graphs)):
                    graph = graphs[i]

                    #If it is a list item, append it to the items array
                    if(graph.style.name in listStyles):
                        #Confirm item is not an emdash
                        if(graph.text.find("—") == -1):
                            #Set completion status based on whether the style is 'Incomplete Item' or 'Complete Item'
                            dict['items'].append({
                                'title': graph.text,
                                'completed': graph.style.name == listStyles[1],
                                'date': dateHandler.setWeekDay('sunday', self.date),
                                'scope': 'week'
                            })

            # We are dealing with the body contents
            if(graphs[0].style.name == "Day Label" or graphs[0].style.name == "Day Label (Inactive)"):
                listStyles = ('List Item','List Item (Inactive)')
                tasksStart = False
                subsection = 0

                # For each graph in the list after the label
                for i in range(1, len(graphs)):
                    graph = graphs[i]

                    #If it is a list item, append it to the items array
                    if(graph.style.name in listStyles):
                        #Confirm item is not an emdash
                        if(graph.text.find("—") == -1):

                            #Set completion status based on whether we have gone into the tasks list or not
                            dict['items'].append({
                                'title': graph.text,
                                'completed': subsection == 2,
                                'date': dateHandler.setWeekDay(dict['label'], self.date),
                                'scope': 'day'
                            })
                    #If it is not a list item, check if it is the Tasks label to determine
                    else:
                        if graph.text.find("Tasks") != -1:
                            subsection = 1
                        elif graph.text.find("Deeds") != -1:
                            subsection = 2
                        else:
                            subsection = 0

        return dict

    def __update_doc__(self):
        self.document.save(self.path)
        self.document = docHandler.get_document(self.path)
