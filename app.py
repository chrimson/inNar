import json
from flask import Flask, render_template

app = Flask(__name__)

def load_story():
    with open('story.json', 'r') as f:
        return json.load(f)

@app.route('/')
@app.route('/<node>')
def game(node="start"):
    STORY = load_story()
    scene = STORY.get(node, STORY["start"])
    return render_template("index.html", scene=scene)

if __name__ == '__main__':
    # host='0.0.0.0' is required for Docker
    app.run(debug=True, host='0.0.0.0')
