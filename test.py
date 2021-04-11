from objects.Log import Log

log = Log(path='./weekLog.docx')

items = log.get_items()
log.complete_item(items[0])
