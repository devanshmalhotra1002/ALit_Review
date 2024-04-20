from flask import Flask,render_template,request,redirect
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

class BookPost(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(50),nullable=False)
    summary = db.Column(db.Text,nullable=False)
    author = db.Column(db.String(20),nullable=False,default='N/A')
    datetime = db.Column(db.DateTime,nullable=False,default=datetime.utcnow)

    def __repr__(self):
        return 'Book Post' + str(self.id)

@app.route('/',methods=['GET'])
def landing():
    return render_template('land.html')

@app.route('/Posts',methods=['GET'])
def getpost():
    i = request.args.get('i')
    if i:
        post = BookPost.query.filter(BookPost.title.contains(i.casefold())|BookPost.author.contains(i.casefold()))
    else:
        post = BookPost.query.all()
    return render_template('posts.html',post=post)

@app.route('/Posts/New',methods=['GET','POST'])
def newpost():
    if request.method == 'POST':
        title = request.form['title']
        summary = request.form['summary']
        author = request.form['author']
        post = BookPost(title=title, summary=summary, author=author)
        db.session.add(post)
        db.session.commit()
        return redirect('/Posts')
    else:
        post = BookPost.query.all()
        return render_template('newpost.html')

@app.route('/Posts/Delete/<int:id>')
def delete(id):
    post = BookPost.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()
    return redirect('/Posts')

@app.route('/Posts/Edit/<int:id>',methods=['POST','GET'])
def editpost(id):
    post = BookPost.query.get_or_404(id)
    if request.method == 'POST':
        post.title = request.form['title']
        post.summary = request.form['summary']
        post.author = request.form['author']
        db.session.commit()
        return redirect('/Posts')
    else:
        return render_template('edit.html',post=post)




if __name__ == '__main__':
    app.run(debug=True)