"""Initialize Flask Application."""
from flask import Flask, render_template
import io
import base64
from groupme import *
from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired

app = Flask(__name__)

class memeForm():
    num = IntegerField('Minimum likes?', validators=[DataRequired()])
    name = StringField('Filter by username, or leave blank for all')

@app.route('/', methods=['GET', 'POST'])
def home():
    """Home page of app with form"""
    group = getGroup()
    messages = getMessages(group)
    length = len(messages)
    row = getMostLikedImage(messages)
    url = row['attachments'][0]['url']
    user_best_image = row['name']
    user_best_image_url = row['avatar_url']
    popular_df = getMostPopular(messages)
    image = getPopularityPlot(popular_df)
    mForm = memeForm()
    return render_template('home.html', 
                           title='Large Fry Larry\'s', 
                           total_messages=length,
                           url=url,
                           user_best_image=user_best_image,
                           user_best_image_url=user_best_image_url,
                           most_popular_image=image,
                           memeForm = mForm)


if __name__ == "__main__":
    group = getGroup()
    messages = getMessages(group)
    app.run(host="0.0.0.0", port=80)
