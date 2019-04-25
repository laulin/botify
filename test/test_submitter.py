import unittest
from unittest.mock import Mock

from botify.submitter import Submitter

class TestSubmitter(unittest.TestCase):
    def test_submit(self):
        adapter = Mock()
        s = Submitter(3, 0, adapter)
        s.submit("foo", bar=2)

        self.assertTrue(adapter.push_job.called)

    def test_submit_no_more_room(self):
        adapter = Mock()
        adapter.job_length = Mock(return_value=5)
        s = Submitter(3, 4, adapter)

        with self.assertRaises(Exception):
            s.submit("foo", bar=2)

    def test_submit_return_job_id(self):
        adapter = Mock()
        s = Submitter(3, 0, adapter)
        job_id = s.submit("foo", bar=2)

        self.assertTrue(isinstance(job_id, str))

    def test_pickup(self):
        adapter = Mock()
        adapter.pop_result = Mock(return_value='{"function_name":"y", "job_id":"xx-yy-zz"}')
        s = Submitter(3, 4, adapter)

        job_id, job = s.pickup()

    def test_pickup_empty_queue(self):
        adapter = Mock()
        adapter.result_length = Mock(return_value=0)
        s = Submitter(3, 4, adapter)

        with self.assertRaises(Exception):
            s.pickup()

if __name__ == "__main__":
    unittest.main()
