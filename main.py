"""Initialize Flask Application."""
from flask import Flask, render_template
import io
import base64
from groupme import getGroup, getMessages, getMostLikedImage

app = Flask(__name__)

@app.route('/')
def home():
    """Home page of app with form"""
    group = getGroup()
    messages = getMessages(group)
    length = len(messages)
    row = getMostLikedImage(messages)
    url = row['attachments'][0]['url']
    user_best_image = row['name']
    user_best_image_url = row['avatar_url']
    return render_template('home.html', 
                           title='Large Fry Larry\'s', 
                           total_messages=length,
                           url=url,
                           user_best_image=user_best_image,
                           user_best_image_url=user_best_image_url)


if __name__ == "__main__":
    group = getGroup()
    messages = getMessages(group)
    app.run(host="0.0.0.0", port=5000)
