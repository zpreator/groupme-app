from groupy import Client
import pandas as pd
import numpy as np
import os
import io
import base64
import seaborn as sns
import holoviews as hv
from chord import Chord
import configparser
from bokeh.io import export_png, export_svg
from bokeh.plotting import show, output_file, save
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
# sns.set(style="ticks", context="talk")
plt.style.use("dark_background")
# sns.set(rc={'axes.facecolor':'black', 'figure.facecolor':'black'})

def getGroup(groupme_key):
    # groupme_key = os.environ.get("GROUPME_KEY")
    client = Client.from_token(groupme_key)
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
    messages_df = messages_df[messages_df['sender_type']=='user'] # Filters out groupme stuff
    list_to_delete = ['GroupMe', 'Zach  Preator', 'Zach Preator 2', 'Donald J. Trump', 'John Cena', 'Shad Karlson, a liberal']
    df_to_delete = messages_df[messages_df['name'].isin(list_to_delete)].index
    messages_df = messages_df.drop(df_to_delete)
    setFavNum(messages_df)
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
    favorited_by = []
    for x in favorites:
        try:
            favs = eval(x)
            favorited_by.append(favs)
            fav_num.append(len(favs))
        except:
            favs = x
            favorited_by.append(favs)
            fav_num.append(len(favs))
    messages_df['fav_num'] = fav_num
    messages_df['favorited_by'] = favorited_by
    return messages_df

def getMostLikedImage(messages_df):
    attach_df = messages_df[messages_df['attachments'].map(len) > 0]
    attach_df = attach_df[attach_df['fav_num'] == 8]
    attach_df = attach_df.sort_values(by='created_at')
    row = attach_df.iloc[-1]
    url = row['attachments'][0]['url']
    user = row['name']
    avatar = row['avatar_url']
    return url, user, avatar

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
    # axis = sns.countplot(data=total_likes_df, y='name', ax=axis)
    axis.set_xlabel("Likes")
    axis.set_ylabel("Name")
    # fig.tight_layout()
    fig.set_tight_layout(True)
    pngImage = io.BytesIO()
    FigureCanvas(fig).print_png(pngImage)
    pngImageB64String = "data:image/png;base64,"
    pngImageB64String += base64.b64encode(pngImage.getvalue()).decode('utf8')
    return pngImageB64String

def getTotalPostsPlot(messages_df):
    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)
    axis.set_title("Total Posts")
    axis.grid()
    # axis.plot(range(5), range(5), "ro-")
    axis = sns.countplot(data=messages_df, x='name', ax=axis, order = messages_df['name'].value_counts().index)
    # axis = sns.countplot(data=total_likes_df, y='name', ax=axis)
    axis.set_xlabel("Name")
    axis.set_ylabel("Posts")
    axis.set_xticklabels(axis.get_xticklabels(), rotation=90)
    # fig.tight_layout()
    fig.set_tight_layout(True)
    pngImage = io.BytesIO()
    FigureCanvas(fig).print_png(pngImage)
    pngImageB64String = "data:image/png;base64,"
    pngImageB64String += base64.b64encode(pngImage.getvalue()).decode('utf8')
    return pngImageB64String

def getLikesPerPost(messages_df):
    df = messages_df[['name', 'fav_num']]
    df = df.groupby('name', as_index=False).mean()
    df = df.sort_values('fav_num', ascending=False)
    # messages_df.groupby('name')['fav_num'].mean()
    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)
    axis.set_title("Average likes per Post")
    axis.grid()
    axis = sns.barplot(data=messages_df, 
                       x='name', 
                       y='fav_num', 
                       ax=axis,
                       order=df['name'].values)
    axis.set_xticklabels(axis.get_xticklabels(), rotation=90)
    axis.set_xlabel("Name")
    axis.set_ylabel("Likes")
    fig.set_tight_layout(True)
    pngImage = io.BytesIO()
    FigureCanvas(fig).print_png(pngImage)
    pngImageB64String = "data:image/png;base64,"
    pngImageB64String = "data:image/png;base64,"
    pngImageB64String += base64.b64encode(pngImage.getvalue()).decode('utf8')
    return pngImageB64String

def getChordDiagram(messages_df):
    # name_id = messages_df[['sender_id', 'name']].astype(str)
    # name_id = name_id.tail(200)
    # name_id = name_id.drop_duplicates().set_index('sender_id').to_dict()
    names_dict = {'17289343': 'Ben Pagel', '18257442': 'Logan Camilletti', '23885372': 'Jake Linford', '41651233': 'Shad Karlson', '41651237': 'Jackson Esplin', '43797901': 'John Hammond', '52396192': 'Jon Michael Ossola', '9803929': 'Zach Preator'}
    df = messages_df[['sender_id', 'favorited_by', 'fav_num']]
    df = df[df['fav_num'] > 0]
    df = df[['sender_id', 'favorited_by']]
    df = df.explode('favorited_by')
    df = df.groupby(df.columns.tolist()).size().reset_index().rename(columns={0:'likes'})
    df['sender_id'] = df['sender_id'].astype(str)
    df['favorited_by'] = df['favorited_by'].astype(str)
    df = df.replace(names_dict)
    names = list(set(df["favorited_by"].unique().tolist() + df["sender_id"].unique().tolist()))
    names_dataset = hv.Dataset(pd.DataFrame(names, columns=["Name"]))
    
    chord = hv.Chord((df, names_dataset))

    #Bokeh
    # hv.extension("bokeh")
    # plot = chord.opts(labels='Name', 
    #                   node_color='Name', 
    #                   edge_color='favorited_by', 
    #                   label_index='sender_id', 
    #                   cmap='Category10', 
    #                   edge_cmap='Category10', 
    #                   width=1000, 
    #                   height=1000, 
    #                   bgcolor="black", 
    #                   label_text_color="white")
    # output_file('templates/likes.html')
    # save(hv.render(chord))
    # hv.save(plot, 'static/likes.svg', fmt='auto')

    #Matplotlib
    hv.extension('matplotlib')
    plot = chord.opts(labels='Name', 
                      node_color='Name', 
                      edge_color='favorited_by', 
                      label_index='sender_id', 
                      cmap='Category10', 
                      edge_cmap='Category10', 
                      bgcolor="black")
    # output_file('templates/likes.html')
    # save(plot)
    hv.save(plot, 'static/likes.svg', fmt='auto')
    hv.save(plot, 'templates/likes.html', fmt='auto')
    # export_svg(plot, filename='static/likes.svg')
    return plot

def getRandomMeme(messages_df, min_likes=0):
    if min_likes == None:
        min_likes = 0
    attach_df = messages_df[messages_df['attachments'].map(len) > 0]
    attach_df = attach_df[attach_df['fav_num'] >= min_likes]
    loop = True
    while loop:
        rand = attach_df.sample()
        row = rand.iloc[0]
        attachments = row['attachments'][0]
        try:
            url = attachments['url']
            loop = False
        except:
            loop = True
    if pd.isna(row['text']):
        text= ''
    else:
        text = '"' + str(row['text']) + '"'
    user = row['name']
    avatar = row['avatar_url']
    return url, user, avatar, text

# config = configparser.ConfigParser()		
# config.read(r"C:\Repos\config\groupmeswag_config.ini")
# keys = config['KEYS']
# GROUPME_KEY = keys['GROUPME_KEY']
# messages = getMessages(getGroup(GROUPME_KEY))
# total_likes_df = getMostPopular(messages)
# getPopularityPlot(total_likes_df)
# getRandomMeme(messages)
# getChordDiagram(messages)