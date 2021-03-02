from groupy import Client
import pandas as pd
import os

def getGroup():
    client = Client.from_token('76c456305c8701394dff0a65443c347e')
    groups = list(client.groups.list_all())
    for group in groups:
        print(group.name)
        if group.name == 'Large Fry Larrys':
            lfl = group
    return lfl

def getMessages(group):
    if os.path.exists('data.csv'):
        data = pd.read_csv('data.csv')
        data.sort_values(by='created_at')
        try:
            maxDate = data['created_at'].max()
        except:
            return getAllMessages(group)
    else:
        return getAllMessages(group)
    messageData = []
    for message in group.messages.list_since(maxDate):
        messageData.append(message.data)
    
    messages_df = pd.DataFrame.from_dict(messageData, orient='columns')
    messages_df = messages_df.append(data).sort_values(by='created_at')
    messages_df = messages_df.drop_duplicates(['id'])
    # print(len(messages_df))
    messages_df.to_csv('data.csv')
    return messages_df

def getAllMessages(group):
    messageData = []
    for message in group.messages.list_all():
        messageData.append(message.data)
    
    messages_df = pd.DataFrame.from_dict(messageData, orient='columns')
    messages_df.to_csv('data.csv')
    return messages_df