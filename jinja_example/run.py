
import datetime

from flask import Flask, render_template


app = Flask(__name__)


@app.template_filter()
def datetimefilter(value, format='%Y/%m/%d %H:%M'):
    """Convert a datetime to a different format"""
    return value.strftime(format)


@app.route('/')
def template_test():
    return render_template(
        'template.html', my_string='foobar', my_list=range(6),
        current_time=datetime.datetime.now())


@app.route("/home")
def home():
    return render_template(
        'template.html', my_string="I'm the home page", my_list=range(6),
        current_time=datetime.datetime.now())


@app.route("/about")
def about():
    return render_template(
        'template.html', my_string="I'm the about page", my_list=range(6),
        current_time=datetime.datetime.now())


@app.route("/contact")
def contact():
    return render_template(
        'template.html', my_string="I'm the contact page", my_list=range(6),
        current_time=datetime.datetime.now())


if __name__ == '__main__':
    app.run(debug=True, port=5000)
