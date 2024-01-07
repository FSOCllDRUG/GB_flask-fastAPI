from flask import Flask, render_template, request, redirect, make_response

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])  # 1.03.23
def form():
    if request.method == 'POST':
        mkrs = make_response(redirect('/hello'))
        mkrs.set_cookie('name', request.form.get('name'))
        mkrs.set_cookie('email', request.form.get('email'))
        return mkrs
    return render_template('form.html')


@app.route('/hello', methods=['GET', 'POST'])
def hello():
    if request.method == 'POST':
        mkrs = make_response(redirect('/'))
        mkrs.delete_cookie('name')
        mkrs.delete_cookie('email')
        return mkrs
    name = request.cookies.get('name')
    return render_template('hello.html', name=name)


if __name__ == '__main__':
    app.run(debug=True)
