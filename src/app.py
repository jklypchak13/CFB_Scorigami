from flask import Flask, request, render_template, redirect, url_for
import table

app = Flask(__name__)
data = table.get_table()


@app.route('/')
def hello():

    return render_template("index.html.jinja", data=data)


if __name__ == '__main__':

    app.run(host="0.0.0.0", port=5000)
