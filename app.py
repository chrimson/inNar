from flask import Flask, render_template, request, url_for, redirect
from flask_httpauth import HTTPBasicAuth
from werkzeug.middleware.proxy_fix import ProxyFix
import json

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)
auth = HTTPBasicAuth()

AUTH_FILE = 'auth.json'


@auth.verify_password
def verify(username, password):
    with open(AUTH_FILE, 'r') as f:
        auth = json.load(f)
    if username in auth and auth[username] == password:
        return username


def load_story(story_file):
    story = {}
    scene = ''
    with open(story_file, 'r') as f:
        lines = f.read().splitlines()
    story['title'] = lines[0]
    story['byline'] = lines[1]

    for i in range(2, len(lines)):
        line = lines[i].strip()

        if line.endswith('---'):
            scene = line.removesuffix("---").strip()
            story[scene] = { 'text' : '', 'choices' : [] };

        elif ' : ' in line:
            choice = line.split(" : ")
            text = choice[0].strip()
            next_scene = choice[1].strip()
            story[scene]['choices'].append({'text':text, 'next':next_scene})

        elif line != '':
            story[scene]['text'] += line + '<p>'

    first = list(story)[2]
    return story, first


def save_story(story_file, data):
    with open(story_file, 'w', newline='\n') as f:
        clean_data = data.replace('\r', '')
        f.write(clean_data)


@app.route('/<story_file>', methods=['GET', 'POST'])
def game(story_file):
    story, first = load_story(story_file)

    node = first
    if request.method == 'POST':
        node = request.form.get('node')

    scene = story.get(node)
    return render_template('index.html',
                           title=story['title'],
                           byline=story['byline'],
                           story_file=story_file,
                           scene=scene)


@app.route('/<story_file>/edit', methods=['GET', 'POST'])
@auth.login_required
def edit_story(story_file):
    if request.method == 'POST':
        story_text = request.form.get('story_text')
        save_story(story_file, story_text)
        story, first = load_story(story_file)

        return redirect(url_for('game', story_file=story_file))

    with open(story_file, 'r') as f:
        content = f.read()

    return render_template('edit.html', story_file=story_file, content=content)

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')
