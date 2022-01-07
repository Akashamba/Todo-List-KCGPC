import backf
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('front.html')


@app.route('/viewtasks')
def viewtasks():
    tasks = backf.readtask()
    x = len(tasks)
    return render_template('viewtasks.html', tasks=tasks, l=x)


@app.route('/viewcompleted')
def viewcompleted():
    tasks = backf.readcompleted()
    x = len(tasks)
    return render_template('viewcomplete.html', tasks=tasks, l=x)


@app.route('/completed/<task>')
def completed(task):
    tasks = backf.readtask()
    x = len(tasks)
    for i in range(x):
        if task in tasks[i]:
            backf.complete(tasks[i][0])

    tasks = backf.readtask()
    x = len(tasks)
    return redirect(url_for('viewtasks', tasks=tasks, l=x))


@app.route('/add/', methods=['POST'])
def add():
    x = request.form['data']
    backf.write(x)
    return redirect(url_for('home'))


@app.route('/clearcompleted')
def clearc():
    backf.deleteallcompleted()
    return redirect(url_for('viewcompleted'))


@app.route('/clearall')
def clearall():
    backf.cleartable()
    return redirect(url_for('viewtasks'))


if __name__ == "__main__":
    app.run(debug=True)
