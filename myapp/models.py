import sqlite3
create_todos_sql = """
--projects table
CREATE TABLE IF NOT EXISTS todos
(
id integer PRIMARY KEY,
title varchar(200) NOT NULL,
description text,
done integer
);
"""
conn = sqlite3.connect('todos.db')
with conn:
    cur = conn.cursor()
    cur.execute(create_todos_sql)


class TodosSQLite:

    def __init__(self):
        try:
            _conn = sqlite3.connect('todos.db')
            with _conn:
                _cur = conn.cursor()
                _cur.execute("SELECT * FROM todos")
                _todos = _cur.fetchall()
                _todo_dic = [
                    {'id': item[0],
                     'title': item[1],
                     'description': item[2],
                     'done': bool(item[3])
                     } for item in _todos]
                self._todos = _todo_dic
        except:
            self._todos = []

    def all(self) -> object:
        return self._todos

    def create(self, data):
        data.pop('csrf_token')
        sql = """
                INSERT INTO todos(title, description, done)
                VALUES (:title, :description, :done)
                """
        _conn = sqlite3.connect('todos.db')
        with _conn:
            _cur = _conn.cursor()
            _cur.execute(sql, data)
            _conn.commit()
            last_id = _cur.lastrowid
            _cur.execute(f"SELECT * FROM todos WHERE id = {last_id}")
            rows = _cur.fetchall()
        rows_dic = [
                    {'id': item[0],
                     'title': item[1],
                     'description': item[2],
                     'done': bool(item[3])
                     } for item in rows]
        self._todos.append(rows_dic[0])

    def get(self, id):
        return self._todos[id]

    def update(self, todo_id, data):
        data.pop('csrf_token')
        data['id'] = todo_id
        self._todos[todo_id-1] = data
        data['done'] = int(data['done'])
        parameters = [f"{k} = :{k}" for k in data]
        parameters = ", ".join(parameters)
        sql = f"""
        UPDATE todos
        SET {parameters}
        WHERE id = {todo_id}
        """
        _conn = sqlite3.connect('todos.db')
        with _conn:
            _cur = _conn.cursor()
            _cur.execute(sql, data)
            _conn.commit()
        data['done'] = bool(data['done'])


todos_sql = TodosSQLite()