from flask import Flask, render_template,url_for,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db=SQLAlchemy(app)


class Article(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    intro= db.Column(db.String(300),nullable=False)
    text = db.Column(db.Text(300), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    def __repr__(self):
        return '<Article %r>' % self.id


@app.route('/')
@app.route('/home')
# @app.route('/home/new')
def index():
    # return "hello world"
    return render_template("index.html")


@app.route('/user/<string:name>/<int:id>')
def user(name,id):
    return "user page: " + name + ' - ' + str(id)



@app.route('/about')
def about():
    # return "about page"
    return render_template("about.html")



@app.route('/posts/<int:id>')
def posts_detail(id):
    articles = Article.query.get(id)
    return render_template("post_detail.html",articl=article)




@app.route('/posts')
def posts():
    # return "about page"
    # articles=Article.query.first()
    articles = Article.query.order_by(Article.date.desc()).all()
    return render_template("posts.html",articles=articles)


@app.route('/posts/<int:id>/delete')
def post_delete(id):
    # return "about page"
    # articles=Article.query.first()
    article = Article.query.get_or_404(id)
    try:
        db.session.delete(article)
        db.session.add(article)
        db.session.commit()
        return redirect('/posts')
    except:
        'при удалении статьи ппроизошла ошибка'



@app.route('/posts/<int:id>/update',methods=["POST","GET"])
def post_update(id):
    article = Article.query.get(id)
    if request.method == 'POST':
        article.title=request.form['title']
        article.intro = request.form['intro']
        article.text = request.form['text']
        # article = Article(title=title,intro=intro,text=text,)
        try:
            # db.session.add(article)
            db.session.commit()
            return redirect('/posts')
        except:
            'при редактировании статьи ппроизошла ошибка'
    else:

        return render_template("post-update.html",article=article)



@app.route('/create-article',methods=["POST","GET"])
def create():
    if request.method == 'POST':
        title=request.form['title']
        intro = request.form['intro']
        text = request.form['text']
        article = Article(title=title,intro=intro,text=text,)
        try:
            db.session.add(article)
            db.session.commit()
            return redirect('/posts')
        except:
            'при добавлении статьи ппроизошла ошибка'
    else:
        return render_template("create-article.html")
    # return "about page"


if __name__ == '__main__':
    app.run(debug=True)