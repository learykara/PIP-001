from blog import app

from flask import Markup
import mistune


@app.template_filter()
def dateformat(date, format):
    if not date:
        return None
    return date.strftime(format)


@app.template_filter('markdown')
def markdown(text):
    return Markup(mistune.markdown(text))
