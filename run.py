from application import create_app
from flask import Flask, render_template

app = create_app()

@app.route('/')



def index():
    return render_template('homepage.html')


@app.route('/search')
def search():
    return render_template('search.html')



@app.route('/chatbot')
def chatbot():
    return render_template('chatbot.html')

if __name__ == '__main__':
    app.run(debug = True)