from groupy import Client
import pandas as pd
import os
import io
import base64
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
# sns.set(style="ticks", context="talk")
plt.style.use("dark_background")
# sns.set(rc={'axes.facecolor':'black', 'figure.facecolor':'black'})

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
    attachments = messages_df['attachments'].tolist()
    newList = []
    for x in attachments:
        try:
            newList.append(eval(x))
        except:
            newList.append(x)
    messages_df['attachments'] = newList
    return messages_df

def setFavNum(messages_df):
    favorites = messages_df['favorited_by'].tolist()
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
    # attach_df = attach_df.sort_values(by='fav_num', ascending=False)
    attach_df = attach_df[attach_df['fav_num'] == 8]
    attach_df = attach_df.sort_values(by='created_at')
    # print(attach_df['favorited_by'].head())
    return attach_df.iloc[-1]

def getMostPopular(messages_df):
    df_names = dict()
    for k, v in messages_df.groupby('name'):
        df_names[k] = v
    # print(df_names['Zach Preator'].head())
    # print("")
    total_likes = []
    for key in df_names.keys():
        num = df_names[key]['fav_num'].sum()
        total_likes.append({'name':key, 'total':num})
    total_likes_df = pd.DataFrame.from_dict(total_likes)
    total_likes_df = total_likes_df.sort_values(by='total', ascending=False)
    # print(total_likes_df)
    return total_likes_df

def getPopularityPlot(total_likes_df):
    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)
    axis.set_title("Total Likes")
    axis.grid()
    # axis.plot(range(5), range(5), "ro-")
    axis = sns.barplot(data=total_likes_df, y='name', x='total', ax=axis)
    axis.set_xlabel("Likes")
    axis.set_ylabel("Name")
    fig.tight_layout()
    pngImage = io.BytesIO()
    FigureCanvas(fig).print_png(pngImage)
    pngImageB64String = "data:image/png;base64,"
    pngImageB64String += base64.b64encode(pngImage.getvalue()).decode('utf8')
    return pngImageB64String

# messages = getMessages(getGroup())
# total_likes_df = getMostPopular(messages)
# getPopularityPlot(total_likes_df)