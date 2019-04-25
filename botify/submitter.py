from uuid import uuid4
import json
import logging

class Submitter:
    # This class provides a way to push jobs
    def __init__(self, retry, max_queue_length, queue):
        # constructor
        #
        # retry : max number of maximum retry
        # max_queue_length : queue size
        # adapter : class to abstract the queue (ex : redis, rmq, ..)
        self._retry = retry
        self._max_queue_length = max_queue_length
        self._queue = queue
        self._log = logging.getLogger("Submitter <{}>".format(id(self)))

    def submit(self, function_name, **kwargs):
        # submit a task
        #
        # function_name is the function name to be called
        # kwargs : a dict of parameter for the called function
        if self._max_queue_length > 0 and self._queue.job_length() >= self._max_queue_length:
            raise Exception("Queue full")

        job_id = str(uuid4())
        payload = {"function_name":function_name, 
                    "args":kwargs, 
                    "retry":self._retry, 
                    "job_id":job_id}
        payload_str = json.dumps(payload)

        self._queue.push_job(payload_str)

        self._log.info("Push function '{}' with job_id '{}'".format(function_name, job_id))

        return job_id

    def pickup(self):
        # pick up a finished (or aborded/failed/...) job
        #
        if self._queue.result_length() == 0:
            raise Exception("Queue empty")

        job_str = self._queue.pop_result()

        job = json.loads(job_str)
        job_id = job["job_id"]
        function_name = job["function_name"]

        self._log.info("Pop function '{}' with job_id '{}'".format(
            function_name, job_id))

        return job_id, job
