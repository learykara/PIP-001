
from flask import Flask


app = Flask(__name__)


@app.route('/hello')
def hello_world():
    return 'Hello World!'


@app.route('/hello/<name>')
def hello_person(name):
    html = """
        <h1>Hello {}!</h1>
        <p>Here's a picture of a kitten.</p>
        <img src="http://placekitten.com/g/200/300">
    """
    return html.format(name.title())


@app.route('/jedi/<firstname>/<lastname>')
def jedi(firstname, lastname):
   jediname = lastname[:3] + firstname[:2] 
   html = """
       <h1>Hello {}!</h1>
       <p>Here's a picture of a kitten.</p>
       <img src="http://placekitten.com/g/200/300">
   """
   return html.format(jediname.title())


if __name__ == '__main__':
    app.run(port=5000)

