import unittest
from unittest.mock import Mock

from botify.publisher import Publisher

class TestPPublisher(unittest.TestCase):
    def test_pickup(self):
        queue = Mock()
        queue.pop_job = Mock(return_value='{"job_id":"aze", "function_name":"y"}')
        storage = Mock()
        p = Publisher(queue, storage)
        instance_id, job = p.pickup()

    def test_pickup_check_storage(self):
        queue = Mock()
        queue.pop_job = Mock(return_value='{"job_id":"aze", "function_name":"y"}')
        storage = Mock()
        p = Publisher(queue, storage)
        p.pickup()

        self.assertTrue(storage.push.called)

    def test_deliver_success(self):
        queue = Mock()
        storage = Mock()
        storage.pop = Mock(return_value='{"job_id":"aze", "function_name":"y", "retry":3}')
        p = Publisher(queue, storage)

        instance_id = "aazzeerrttyy"
        result = {"status":"success"}
        p.deliver(instance_id, result)

        self.assertTrue(queue.push_result.called)

    def test_deliver_refused(self):
        queue = Mock()
        storage = Mock()
        storage.pop = Mock(return_value='{"job_id":"aze", "function_name":"y", "retry":3}')
        p = Publisher(queue, storage)

        instance_id = "aazzeerrttyy"
        result = {"status": "refused"}
        p.deliver(instance_id, result)

        self.assertTrue(queue.push_job.called)

    def test_deliver_failed_but_retry(self):
        queue = Mock()
        storage = Mock()
        storage.pop = Mock(return_value='{"job_id":"aze", "function_name":"y", "retry":2}')
        p = Publisher(queue, storage)

        instance_id = "aazzeerrttyy"
        result = {"status": "failed"}
        p.deliver(instance_id, result)

        self.assertTrue(queue.push_job.called)

    def test_deliver_failed(self):
        queue = Mock()
        storage = Mock()
        storage.pop = Mock(return_value='{"job_id":"aze", "function_name":"y", "retry":1}')
        p = Publisher(queue, storage)

        instance_id = "aazzeerrttyy"
        result = {"status": "failed"}
        p.deliver(instance_id, result)

        self.assertTrue(queue.push_result.called)

if __name__ == "__main__":
    unittest.main()
