#!/usr/bin/env python
import sys

from flask import Flask, render_template, request, flash
from flask_frozen import Freezer
from flask.ext.mail import Mail
from forms import ContactForm
from flask.ext.mail import Message
import os


DEBUG = True
FLATPAGES_AUTO_RELOAD = DEBUG

MAIL_SERVER = 'smtp.googlemail.com'
MAIL_PORT = 465
MAIL_USE_TLS = False
MAIL_USE_SSL = True
GMAIL_USER = os.environ.get('GMAIL_USER', '')
GMAIL_PASSWORD = os.environ.get('GMAIL_PASSWORD', '')

# administrator list
ADMINS = ['lesliehealray@gmail.com']

app = Flask(__name__)
CSRF_ENABLED = True
secret_key = ''
WTF_CSRF_SECRET_KEY= ''



app.config.from_object(__name__)
app.config['FREEZER_RELATIVE_URLS'] = True

mail = Mail(app)
freezer = Freezer(app)


NAVIGATION = (
    {'title': 'Music Lessons', 'slug': 'about'},
    {'title': 'Audio', 'slug': 'audio'},
    {'title': 'Projects & Performances', 'slug': 'myprojects'},
    {'title': 'Music & Technology', 'slug': 'music_tech'},
    {'title': 'Contact', 'slug': 'contact'},

)



@app.route('/')
def index():
    return render_template('index.html', nav=NAVIGATION)


@app.route('/contact/', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if request.method == 'POST':
        if form.validate() == False:
            flash('All fields are required.')
        else:
            with mail.connect() as conn:
                msg = Message(sender=form.email.data,
                        subject="[lesliehealray.com] %s" % form.subject.data,
                        recipients=['lesliehealray@gmail.com'])
                msg.body = """
From: %s <%s>
%s
""" % (form.name.data, form.email.data, form.message.data)
                conn.send(msg)
            flash('Form posted.')

    return render_template('content/contact.html', form=form, nav=NAVIGATION)



@app.route('/<slug>/')
def page(slug):
    template = 'content/%s.html' % slug
    return render_template(template, nav=NAVIGATION)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "build":
        freezer.freeze()
    else:
        app.secret_key = 'cantarediva'
        app.run()




