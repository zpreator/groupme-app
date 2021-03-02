"""Initialize Flask Application."""
from flask import Flask, render_template
import io
import base64
from groupme import getGroup, getMessages

app = Flask(__name__)

@app.route('/')
def home():
    """Home page of app with form"""
    group = getGroup()
    messages = getMessages(group)
    length = len(messages)
    return render_template('home.html', title='Large Fry Larry\'s', total_messages=length)


if __name__ == "__main__":
    group = getGroup()
    messages = getMessages(group)
    app.run(host="0.0.0.0", port=80)
