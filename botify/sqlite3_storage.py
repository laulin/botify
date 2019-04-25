import sqlite3
from time import time


class SQLite3Storage:

    def __init__(self, filename=":memory:"):

        self._connection = sqlite3.connect(filename)
        self.create_table()

    def create_table(self):
        command = 'CREATE TABLE IF NOT EXISTS hash (instance_id text UNIQ PRIMARY KEY, timeout integer, job text)'
        self._connection.execute(command)
        self._connection.commit()

    def push(self, instance_id, job, timeout=30):
        command = "INSERT INTO hash VALUES (?, ?, ?)"
        t = int(time()) + timeout
        self._connection.execute(command, (instance_id, t, job))
        self._connection.commit()

    def pop(self, instance_id):
        job = None
        for row in self._connection.execute('SELECT job FROM hash WHERE instance_id=?', (instance_id,)):
            job = row[0]
            break
        
        command = 'DELETE FROM hash WHERE instance_id=?'
        self._connection.execute(command, (instance_id,))
        self._connection.commit()

        if not job:
            raise Exception("Instance_id {} doesn't exists".format(instance_id))

        return job

    def pop_timeout(self):
        command = 'SELECT job FROM hash WHERE timeout<=?'
        t = int(time())
        output = []
        output = [row[0] for row in self._connection.execute(command, (t,))]

        command = 'DELETE FROM hash WHERE timeout<=?'
        self._connection.execute(command, (t,))
        self._connection.commit()

        return output
