from flask import Flask, render_template, request , redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///text.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

class Text(db.Model):
    name = db.Column(db.String(100), primary_key=True)
    password = db.Column(db.String(100), nullable=False)
    content = db.Column(db.String(4294000000), nullable=True)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<text %r>' % self.name


@app.route('/', methods=['POST','GET'])
def index():
    if request.method == 'POST':
        nameEntered = request.form['name']
        users = Text.query.all()
        for u in users:
            if nameEntered==u.name:
                return redirect('/'+str(nameEntered))

        return redirect('/createpass&' + str(nameEntered))
    else:
        return render_template('index.html')

@app.route('/<string:name>', methods=['POST','GET'])
def enter(name):
    for i in name:
        if i in "! * ' ( ) ; : @ & = + $ , / ? % # [ ]".split(' '):
            return 'Invalid Name'
    try:
        nameEntered = Text.query.get_or_404(name)
    except:
        return redirect('/createpass&' + str(name))
    if request.method == 'POST':
        password = request.form['pass']
        user = Text.query.get_or_404(name)
        if password == user.password:
            return redirect('/' + str(name)+'&'+str(password))
        else:
            msg = "Incorrect Password!"
            return render_template('enter.html', msg=msg, name=name)
    else:
        return render_template('enter.html',name=name)


@app.route('/createpass&<string:name>', methods=['POST','GET'])
def create(name):
    for i in name:
        if i in "! * ' ( ) ; : @ & = + $ , / ? % # [ ]".split(' '):
            return 'Invalid Name'
    if request.method == 'POST':
        password = request.form['pass']
        password2 = request.form['pass2']
        if password == password2:
            entry = Text(name=name,password=password,content='')
            try:
                db.session.add(entry)
                db.session.commit()
                return redirect('/'+str(name)+'&'+str(password))
            except:
                return 'There was an error adding your name!'
        else:
            msg = "Passwords doesn't match!"
            return render_template('create.html',msg=msg,name=name)

    else:
        return render_template('create.html',name=name)

@app.route('/<string:name>&<string:password>', methods=['POST','GET'])
def after(name,password):
    text_to_update = Text.query.get_or_404(name)
    if password == text_to_update.password:
        if request.method == 'POST':
            text_to_update.content = request.form['content']
            try:
                db.session.commit()
                return redirect('/'+str(name)+'&'+str(password))
            except:
                return 'There was an issue updating your text'
        else:
            return render_template('after.html', text=text_to_update,name=name)
    else:
        return 'Invalid Credentials'

@app.errorhandler(404)
def page_not_found(e):
    print(e)
    return render_template('404.html')

if __name__ == '__main__':
    app.run(debug=True)

