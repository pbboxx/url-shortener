
from flask import Flask, request, render_template, redirect
from flask_sqlalchemy import SQLAlchemy
import base64, md5
from urlparse import urlparse


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/pada.db'
host = 'http://localhost:5000/'
db = SQLAlchemy(app)


@app.route('/', methods=['GET', 'POST'])
def home():
    """
    :return: the url shorted
    """
    if request.method == 'POST':
        original_url = str(request.form.get('url'))
        if urlparse(original_url).scheme == '':
            url = 'http://' + original_url  #check if the url contain http
        else:
            url = original_url
        code = base64.b64encode(md5.new(url).digest()[-4:]).replace('=', '').replace('/', '_') # encode the url
        Url = urls(url,code)
        db.session.add(Url)
        db.session.commit()
        return render_template('index.html', short_url= host + code)
    return render_template('index.html')


@app.route('/<url>')
def redirect_short_url(url):
    """
    :param url: shortening url
    :return: redirect to the url
    """
    url_query = urls.query.filter_by(code=url).first_or_404()
    url = url_query.url
    return redirect(url)



class urls(db.Model):
    __tablename__ = 'urls'

    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(100))
    code = db.Column(db.String(120))


    def __init__(self, url,code):
        self.url = url
        self.code = code

    def __repr__(self):
        return '<url %d>' % self.id


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)