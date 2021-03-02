from groupy import Client

def getGroup():
    client = Client.from_token('76c456305c8701394dff0a65443c347e')
    groups = list(client.groups.list_all())


    for group in groups:
        print(group.name)
        if group.name == 'Large Fry Larrys':
            lfl = group
    return lfl

def getMessages(group):
    count = 0
    messages = []
    for message in group.messages.list_all():
        count += 1
        messages.append(message)
    return messages