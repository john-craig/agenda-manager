import sys
import managers.agendaManager as agendaManager
import managers.ledgerManager as ledgerManager

def utility(option):
    if(option == 'agenda'):
        print(agendaManager.fetch())
    else:
        print(ledgerManager.fetch(option))
    # elif(option == 'log'):
    #     print(ledgerManager.fetch(option))
    # elif(option == 'record'):
    #     print(ledgerManager.fetch(option))
    # elif(option == 'regimen'):
    #     print(ledgerManager.fetch(option))
    # elif(option == 'nutrition'):
    #     print(ledgerManager.fetch(option)
    # elif(option == 'budget'):
    #     print(ledgerManager.fetch(option))


utility(sys.argv[1])
