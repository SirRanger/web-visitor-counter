"""Web app"""
import datetime

from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__, template_folder='../templates', static_folder='../static')


def get_visitor_count():
    """Function to get last entry"""
    with open('daten.txt', 'r', encoding="utf-8") as file:
        lines = file.readlines()
        if lines:
            last_line = lines[-1].strip()
            parts = last_line.split(':')
            if len(parts) > 1:
                return int(parts[-1])
    return 0


def update_visitor_count(count):
    """Function to update visitor count in file"""
    with open('daten.txt', 'a', encoding="utf-8") as file:
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H')
        file.write(f"{timestamp}: {count}\n")


def count_visitors_last_hour():
    """Function to count visitors"""
    with open('daten.txt', 'r', encoding="utf-8") as file:
        lines = file.readlines()
    current_time = datetime.datetime.now()
    one_hour_ago = current_time - datetime.timedelta(hours=1)   
    count = 0
    for line in lines:
        parts = line.split(':')
        if len(parts) >= 2:
            timestamp = datetime.datetime.strptime(parts[0], '%Y-%m-%d %H')
            if one_hour_ago <= timestamp <= current_time:
                count += int(parts[-1])   
    return count


@app.route('/', methods=['GET', 'POST'])
def index():
    """Web main page"""
    if request.method == 'POST':
        number = request.form['number']
        with open('daten.txt', 'a', encoding="utf-8"):
            update_visitor_count(number)
        return redirect(url_for('index'))
    visitor_count = get_visitor_count()
    visitors_last_hour = count_visitors_last_hour()
    return render_template('/index.html', visitor_count=visitor_count, visitors_last_hour=visitors_last_hour)


@app.route('/admin', methods=['GET', 'POST'])
def admin():
    """Admin page to manage data file"""
    if request.method == 'POST':
        new_content = request.form['new_content']
        # Hier den neuen Inhalt in die Textdatei schreiben
        with open('daten.txt', 'a', encoding="utf-8") as file:
            file.write(new_content + '\n')

    with open('daten.txt', 'r', encoding="utf-8") as file:
        file_content = file.read()

    return render_template('admin.html', file_content=file_content)


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
