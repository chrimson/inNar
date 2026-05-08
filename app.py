from flask import Flask, render_template, request
from werkzeug.middleware.proxy_fix import ProxyFix
import json

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)

def load_story():
    with open('story.json', 'r') as f:
        return json.load(f)

@app.route('/', methods=['GET', 'POST'])
def game():
    node = "start"
    if request.method == 'POST':
        node = request.form.get('node', 'start')

    STORY = load_story()
    scene = STORY.get(node, STORY["start"])
    return render_template("index.html", scene=scene)

if __name__ == '__main__':
    # host='0.0.0.0' is required for Docker
    app.run(debug=True, host='0.0.0.0')
