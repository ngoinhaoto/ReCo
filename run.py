from application import create_app
from flask import Flask, render_template, redirect

app = create_app()

@app.route('/')
def index():
    return render_template('homepage.html')

@app.route('/ai-creator')
def link_ai_creator():
    return redirect('http://127.0.0.1:8000/')

@app.route('/search')
def search():
    return render_template('search.html')



@app.route('/chatbot')
def chatbot():
    return render_template('chatbot.html')


@app.route('/homepage-default')
def homepage_default():
    return render_template('homepage-default.html')

if __name__ == '__main__':
    app.run(debug = True)