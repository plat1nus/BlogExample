from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'

db = SQLAlchemy(app)


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    intro = db.Column(db.String(200), nullable=False)
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow())

    def __repr__(self):
        return f"Article {self.id}"


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/articles')
def articles():
    all_articles = Article.query.order_by(Article.date.desc()).all()
    return render_template("articles.html", articles=all_articles)


@app.route('/articles/<int:id>')
def article(id):
    current_article = Article.query.get(id)
    return render_template("article.html", article=current_article)


@app.route('/articles/<int:id>/delete')
def article_delete(id):
    article = Article.query.get_or_404(id)

    try:
        db.session.delete(article)
        db.session.commit()
        return redirect("/articles")
    except:
        return "Error while deleting an article"


@app.route('/articles/<int:id>/edit', methods=['POST', 'GET'])
def edit_article(id):
    article_edit = Article.query.get(id)
    if request.method == "POST":
        article_edit.title = request.form['title']
        article_edit.intro = request.form['intro']
        article_edit.text = request.form['text']
        try:
            db.session.commit()
            return redirect('/articles')
        except:
            return "Error while editing an article"
    else:
        return render_template("edit-article.html", article=article_edit)


@app.route("/create-article", methods=['POST', 'GET'])
def create_article():
    if request.method == "POST":
        title = request.form['title']
        intro = request.form['intro']
        text = request.form['text']

        new_article = Article(title=title, intro=intro, text=text)
        try:
            db.session.add(new_article)
            db.session.commit()
            return redirect('/articles')
        except:
            return "Error while creating an article"
    else:
        return render_template("create-article.html")


if __name__ == "__main__":
    app.run(debug=True)
