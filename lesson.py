import sqlite3

from flask import Flask
from flask import render_template

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'top'

@app.route('/hello')
@app.route('/hello/<username>')
def hello_world_html(username=None):
    return render_template('hello.html', username=username)

@app.route('/kensaku', methods=['POST'])
def kensaku_html():
    return render_template('kensaku.html')

@app.route('/ichiran', methods=['POST'])
def ichiran_html():
    return render_template('ichiran.html')

@app.route('/toroku', methods=['POST'])
def toroku_html():
    return render_template('toroku.html')



def main():
    app.debug = True
    app.run()

if __name__=='__main__':
    main()