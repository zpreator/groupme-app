"""Initialize Flask Application."""
from flask import Flask, render_template
import io
import base64
from groupme import *
from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired
from flask_wtf import FlaskForm
from flask_bootstrap import Bootstrap

app = Flask(__name__)
bootstrap = Bootstrap(app)
app.config['SECRET_KEY'] = 'C2HWGVoMGfNTBsrYQg8EcMrdTimkZfAb'

class memeForm(FlaskForm):
    likes = IntegerField('likes', validators=[DataRequired()])

@app.route('/', methods=['GET', 'POST'])
def home():
    """Home page of app with form"""
    group = getGroup()
    messages = getMessages(group)
    length = len(messages)
    url, user_best_image, user_best_image_url = getMostLikedImage(messages)
    setFavNum(messages)
    popular_df = getMostPopular(messages)
    total_posts_image = getTotalPostsPlot(messages)
    most_popular_image = getPopularityPlot(popular_df)
    likes_per_post_image = getLikesPerPost(messages)
    form = memeForm()
    rand_url, user_rand_image, user_rand_image_url = getRandomMeme(messages, form.likes.data)
    return render_template('home.html', 
                        title='Large Fry Larry\'s', 
                        total_messages=length,
                        url=url,
                        user_best_image=user_best_image,
                        user_best_image_url=user_best_image_url,
                        total_posts_image=total_posts_image,
                        most_popular_image=most_popular_image,
                        likes_per_post_image=likes_per_post_image,
                        form = form,
                        rand_url=rand_url,
                        user_rand_image=user_rand_image,
                        user_rand_image_url=user_rand_image_url)


if __name__ == "__main__":
    group = getGroup()
    messages = getMessages(group)
    app.run(host="0.0.0.0", port=80)
