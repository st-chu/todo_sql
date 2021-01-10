from flask import Flask, render_template, redirect, url_for
from myapp.forms import TodoForm
from myapp.models import todos_sql


app = Flask(__name__)
app.config.from_pyfile('./instance/config.py')


@app.route("/todos/", methods=["GET"])
def todos_list():
    form = TodoForm()
    return render_template("todos.html", form=form, todos=todos_sql.all())


@app.route("/todos/", methods=["POST"])
def todos_new():
    form = TodoForm()
    if form.validate_on_submit():
        todos_sql.create(form.data)
        return redirect(url_for("todos_list"))


@app.route("/todos/<int:todo_id>/", methods=["GET"])
def todo_details(todo_id):
    todo = todos_sql.get(todo_id - 1)
    form = TodoForm(data=todo)
    return render_template("todo.html", form=form, todo_id=todo_id)


@app.route("/todos/<int:todo_id>/", methods=["POST"])
def todo_update(todo_id):
    todo = todos_sql.get(todo_id - 1)
    form = TodoForm(data=todo)
    if form.validate_on_submit():
        todos_sql.update(todo_id, form.data)
    return redirect(url_for("todos_list"))


if __name__ == "__main__":
    app.run(debug=True)
