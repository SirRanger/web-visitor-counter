"""Web app"""
import datetime

from flask import Flask, render_template, request

app = Flask(__name__, template_folder='../templates', static_folder='../static')


@app.route('/', methods=['GET', 'POST'])
def index():
    """Web app"""
    if request.method == 'POST':
        number = request.form['number']
        timestamp = datetime.datetime.now()
        data = f"{timestamp}: {number}\n"
        with open('daten.txt', 'a', encoding="utf-8") as file:
            file.write(data)
    return render_template('/index.html')


if __name__ == '__main__':
    app.run(debug=True)
