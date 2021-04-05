#import dateHandler
#import logHandler
#import noteHandler
import managers.agendaManager as agendaManager
import managers.ledgerManager as ledgerManager

agendaManager.run()
#ledgerManager.run()


#noteHandler.get_tasks()

# path = './weekLog.docx'
#
# doc = logHandler.getDocument(path)
# paragraphs = logHandler.getParagraphs(doc)
#
# paragraphs[3].insert_paragraph_before("Test")

#
# for graph in paragraphs:
#     print(graph.text)

# for graph in header.paragraphs:
#     print(graph.text)
