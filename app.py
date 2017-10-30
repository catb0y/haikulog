# coding:utf-8
from flask import Flask, render_template, request, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from textstat.textstat import textstat
from textstat.textstat import textstat
import os
import random
import math
import postgresql



# Create SQLAlchemy object
basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.secret_key = "super secret key"
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://dayjxqmgfwirvj:8abcb93a65e01d03d23c9c43e43e74a187fd464c2198a122fbbcd9006d91ce3b@ec2-54-83-40-208.compute-1.amazonaws.com:5432/datd52rju45245
'
db = SQLAlchemy(app)

# Models
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    line1 = db.Column(db.Text)
    line2 = db.Column(db.Text)
    line3 = db.Column(db.Text)
    nickname = db.Column(db.String(80))


    def __repr__(self):
        return '<Post %r>' % self.title


# Views
@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def main():
        posts = Post.query.all()
        random.shuffle(posts)
        return render_template('index.html', posts=posts)


# Submit route to update with lines instead of body
@app.route('/submit', methods=['GET', 'POST'])
def submit():
    if request.method == 'POST':
        title = request.form['title']
        line1 = request.form['line1']
        line2 = request.form['line2']
        line3 = request.form['line3']
        nickname = request.form['nickname']

        post = Post(title=title, line1=line1, line2=line2, line3=line3, nickname=nickname)

        # Enter haiku love

        if math.ceil(textstat.syllable_count(request.form['line1'])) == 5 and \
            math.ceil(textstat.syllable_count(request.form['line2'])) == 7 and \
            math.ceil(textstat.syllable_count(request.form['line3'])) == 5:
                db.session.add(post)
                db.session.commit()
        else:
            flash("Your lines should contain exactly 5, 7, and 5 syllables!")
            return redirect(url_for('submit'))


        return redirect(url_for('main'))
    return render_template('submit.html')


if __name__== '__main__':
    app.run(debug=True)



# Breakdown:

# Change database? + add decent haikus?
# HTML : add about page and links?
# Tweak CSS: font, details
# Add randomized radio avatars to nicknames (pls): <img src="{{url_for('static'), filename='imgs/av1.png'}}" style="border-radius:50%">

# Test post:
#post1 = Post(title="Haiku", line1="accomodation", line2="similitudinary", line3="accomodation", nickname="Spacecow")

#The Birds In The Trees ~ Haiku 5-7-5
#by Barbara Lynn Terry


#I sit here and see
#The birds singing in the trees
#Flitting back and forth.
