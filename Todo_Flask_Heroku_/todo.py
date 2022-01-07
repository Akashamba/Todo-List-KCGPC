import backf
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
logged = {}


@app.route('/')
def index():
    return redirect(url_for('login'))


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/verifylogin', methods=['POST'])
def verifylogin():
    username = request.form['username']
    password = request.form['password']

    if backf.authenticate(username, password):
        global logged
        logged[username] = True
        return redirect(url_for('home', username=username))
    else:
        return redirect(url_for('login', message="Error"))


@app.route('/logout/<username>')
def logout(username):
    global logged
    logged.pop(username)
    return redirect(url_for('index'))


@app.route('/signup')
def signup():
    return render_template('signup.html')


@app.route('/createaccount', methods=['POST'])
def createaccount():
    name = request.form['name']
    username = request.form['username']
    password = request.form['password']
    cpassword = request.form['cpassword']

    if backf.check(name, username, password, cpassword):
        print("passed check")
        backf.create_acc(name, username, password)
        print("passed create")
        return render_template('accountcreated.html')
    else:
        return render_template('signup.html', message="Error")


@app.route('/home/<username>')
def home(username):
    try:
        if logged[username]:
            return render_template('front.html', username=username)
    except Exception:
        return redirect(url_for('login'))


@app.route('/viewtasks/<username>')
def viewtasks(username):
    try:
        if logged[username]:
            tasks = backf.readtask(username)
            x = len(tasks)
            return render_template('viewtasks.html', username=username, tasks=tasks, l=x)
    except Exception:
        return redirect(url_for('login'))


@app.route('/viewcompleted/<username>')
def viewcompleted(username):
    try:
        if logged[username]:
            tasks = backf.readcompleted(username)
            x = len(tasks)
            return render_template('viewcomplete.html', username=username, tasks=tasks, l=x)
    except Exception:
        return redirect(url_for('login'))


@app.route('/completed/<username>/<task>')
def completed(username, task):
    tasks = backf.readtask(username)
    x = len(tasks)
    for i in range(x):
        if task in tasks[i]:

            backf.complete(username, tasks[i][0])

    tasks = backf.readtask(username)
    x = len(tasks)
    return redirect(url_for('viewtasks', username=username))


@app.route('/add/<username>', methods=['POST'])
def add(username):
    x = request.form['data']
    backf.write(username, x)
    return redirect(url_for('home', username=username))


@app.route('/clearcompleted/<username>')
def clearc(username):
    backf.deleteallcompleted(username)
    return redirect(url_for('viewcompleted', username=username))


@app.route('/clearall/<username>')
def clearall(username):
    backf.cleartable(username)
    return redirect(url_for('viewtasks', username=username))


if __name__ == "__main__":
    app.run(debug=True)
