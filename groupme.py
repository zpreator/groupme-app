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
    messages_df = convertAttachments(messages_df)
    messages_df = setFavNum(messages_df)
    # print(len(messages_df))
    messages_df.to_csv('data.csv')
    return messages_df

def getAllMessages(group):
    print('Getting all messages, this will take a minute...')
    messageData = []
    for message in group.messages.list_all():
        messageData.append(message.data)
    
    messages_df = pd.DataFrame.from_dict(messageData, orient='columns')
    messages_df.to_csv('data.csv')
    return messages_df

def convertAttachments(messages_df):
    attachments = messages_df['attachments'].values.to_list()
    newList = []
    for x in attachments:
        try:
            newList.append(eval(x))
        except:
            newList.append(x)
    messages_df['attachments'] = newList
    return messages_df

def setFavNum(messages_df):
    favorites = messages_df['favorited_by'].values.to_list()
    fav_num = []
    for x in favorites:
        try:
            fav_num.append(len(eval(x)))
        except:
            fav_num.append(len(x))
    messages_df['fav_num'] = fav_num
    return messages_df

def getMostLikedImage(messages_df):
    # df = getMessages(getGroup())
    attach_df = messages_df[messages_df['attachments'].map(len) > 0]
    attach_df = attach_df.sort_values(by='fav_num', ascending=False)
    # print(attach_df['favorited_by'].head())
    return attach_df.iloc[0]