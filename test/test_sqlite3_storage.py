import unittest

from botify.sqlite3_storage import SQLite3Storage


class TestPPublisher(unittest.TestCase):

    def test_create_table(self):
        storage = SQLite3Storage()
        storage.create_table() # test if nothing happen

    def test_push(self):
        storage = SQLite3Storage()
        storage.push("a-b-c-d", '{"x":"y"}')

    def test_pop(self):
        storage = SQLite3Storage()
        storage.push("a-b-c-d", '{"x":"y"}')
        job = storage.pop("a-b-c-d")

        self.assertEqual(job, '{"x":"y"}')

    def test_pop_failed(self):
        storage = SQLite3Storage()

        with self.assertRaises(Exception):
            storage.pop("a-b-c-d")

    def test_pop_timeout(self):
        storage = SQLite3Storage()
        storage.push("a-b-c-d", '{"x":"y"}', -1)
        jobs = storage.pop_timeout()

        self.assertEqual(jobs, ['{"x":"y"}'])

    def test_pop_timeout_two_times(self):
        storage = SQLite3Storage()
        storage.push("a-b-c-d", '{"x":"y"}', -1)
        storage.pop_timeout()
        jobs = storage.pop_timeout()

        self.assertEqual(jobs, [])


if __name__ == "__main__":
    unittest.main()
