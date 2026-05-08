from flask import Flask, render_template, request, url_for, redirect
from flask_httpauth import HTTPBasicAuth
from werkzeug.middleware.proxy_fix import ProxyFix
import json

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)
auth = HTTPBasicAuth()

STORY_FILE = 'story.json'
AUTH_FILE = 'auth.json'

@auth.verify_password
def verify(username, password):
    with open(AUTH_FILE, 'r') as f:
        auth = json.load(f)
    if username in auth and auth[username] == password:
        return username

def load_story():
    with open(STORY_FILE, 'r') as f:
        return json.load(f)

def save_story(data):
    with open(STORY_FILE, 'w') as f:
        json.dump(data, f, indent=4)

STORY = load_story()

@app.route('/', methods=['GET', 'POST'])
def game():
    node = "start"
    if request.method == 'POST':
        node = request.form.get('node', 'start')

    scene = STORY.get(node, STORY["start"])
    return render_template("index.html", scene=scene)

@app.route('/edit', methods=['GET', 'POST'])
@auth.login_required
def edit_story():
    global STORY
    if request.method == 'POST':
        new_story_text = request.form.get('story_json')
        new_story_data = json.loads(new_story_text)

        save_story(new_story_data)
        STORY = new_story_data

        return redirect(url_for('game'))

    with open(STORY_FILE, 'r') as f:
        content = f.read()

    return render_template("edit.html", content=content)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
