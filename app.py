from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import shortuuid

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///urls.db'
db = SQLAlchemy(app)

class URL(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    long_url = db.Column(db.String(2048))
    short_url = db.Column(db.String(50), unique=True)

with app.app_context():
    db.create_all()
@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/shorten', methods=['POST'])
def shorten():
    long_url = request.form['long_url']
    short_id = shortuuid.uuid()[:8] #generate a short 8 character id
    short_url = request.host_url + short_id

    new_url = URL(long_url=long_url, short_url=short_url)
    db.session.add(new_url)
    db.session.commit()

    return render_template('index.html', short_url=short_url)

@app.route('/<short_id>')
def redirect_url(short_id):
    short_url = request.host_url + short_id
    url = URL.query.filter_by(short_url=short_url).first()
    if url:
        return redirect(url.long_url)
    else:
        return "URL not found", 404

if __name__ == '__main__':
    app.run(debug=True)