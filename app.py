from flask import Flask, render_template, request, redirect, url_for
from models import db, Article, Goga, Item,Category
from flask_migrate import Migrate
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from form import RegisterForm, LoginForm, ArticleForm


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///identifier.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'Thisissupposedtobesecret!'
db.init_app(app)
migarte = Migrate(app, db)
login = LoginManager(app)


@login.user_loader
def load_user(user_id):
    return Goga.query.get(int(user_id))



@app.route('/')
def index():
    return render_template("index.html", articles=Article.query.all())



@app.route('/login', methods=['GET','POST'])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        email = login_form.email.data
        password = login_form.password.data
        user = Goga.query.filter_by(email=email).first()
        login_user(user, remember=True)
        return redirect('/')
    return render_template('login.html', form=login_form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect('/')


@app.route("/about")
def about():
    return render_template("about.html")


#@app.route("/add", methods=['GET','POST'])
#def add():
  #  if request.method == "POST":
    #    title = request.form['name_item']
      #  about = request.form['about']
      #  adress = request.form['adress']

       # item = Item(about = about, name_item = title, adress = adress)
      #  try:
         #   db.session.add(item)
         #   db.session.commit()
         #   return redirect("/")
       # except:
           # return "Получилась ошибка"
   # else:
      #  return render_template('add.html')




@app.route('/add', methods=['GET', 'POST'])
@login_required
def create_article():
    article_form = ArticleForm()
    if article_form.validate_on_submit():
        title = article_form.title.data
        body = article_form.body.data
        author_id = current_user.name
        category_id = article_form.category_id.data
        article = Article(title=title, body=body,category_id=category_id,author_id=author_id )
        db.session.add(article)
        db.session.commit()
        return redirect('/')
    return render_template('add.html', form=article_form)


@app.route("/privacy")
def privacy():
    return render_template("privacy.html")


@app.route("/terms")
def terms():
    return render_template("terms.html")


@app.route('/index/<int:id>')
def post(id):
    item = Article.query.get(id)
    return render_template("post_detail.html", item = item)


@app.route('/register', methods=['GET', 'POST'])
def register():
    register_form = RegisterForm()
    if register_form.validate_on_submit():
        email = register_form.email.data
        name = register_form.name.data
        password = register_form.password.data
        user = Goga(name=name, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        login_user(user, remember=True)
        return redirect('/')
    return render_template('register.html', form=register_form)


@app.route('/search')
def search():
    text = request.args['text']
    result = Article.query.filter(db.or_(
        Article.title.like(f'%{text}%'),
        Article.body.like(f'%{text}%')
    )).all()

    if len(result) == 1:
        return redirect(url_for('get_article', article_id=result[0].id))

    return render_template('index.html', header=f'Поиск по слову "{text}"', articles=result)


@app.route('/category/<int:category_id>')
def category_articles(category_id):
    category = Category.query.get_or_404(category_id)
    return render_template('category.html', category=category)


@app.route('/home_id')
def home():
    status = Article.query.all()
    status[current_user]
    return render_template('home_id.html', status = status)


if __name__ == '__main__':
    app.run()