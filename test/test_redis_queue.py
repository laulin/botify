import redis
import unittest

from botify.redis_queue import RedisQueue


class TestPPublisher(unittest.TestCase):
    def setUp(self):
        r = redis.Redis()
        r.delete("job")
        r.delete("result")
        self._redis_queue = RedisQueue(r, "job", "result")

    def test_push_pop_job(self):
        self._redis_queue.push_job("xxx")
        result = self._redis_queue.pop_job()

        self.assertEqual(result, "xxx")

    def test_push_pop_job_2(self):
        self._redis_queue.push_job("xxx")
        self._redis_queue.push_job("yyy")
        result = self._redis_queue.pop_job()

        self.assertEqual(result, "xxx")

    def test_job_length(self):
        self._redis_queue.push_job("xxx")
        self._redis_queue.push_job("yyy")
        length = self._redis_queue.job_length()

        self.assertEqual(length, 2)

    def test_push_pop_result(self):
        self._redis_queue.push_result("xxx")
        result = self._redis_queue.pop_result()

        self.assertEqual(result, "xxx")

    def test_push_pop_result_2(self):
        self._redis_queue.push_result("xxx")
        self._redis_queue.push_result("yyy")
        result = self._redis_queue.pop_result()

        self.assertEqual(result, "xxx")


if __name__ == "__main__":
    unittest.main()
