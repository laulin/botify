import json
from uuid import uuid4
import time
import logging


class Publisher:
    def __init__(self, queue, storage):

        self._queue = queue
        self._storage = storage
        self._log = logging.getLogger("Publisher <{}>".format(id(self)))

    def _manage_fail(self, job):

        job["retry"] = job["retry"] - 1
        job_str = json.dumps(job)
        if job["retry"] <= 0:
            self._queue.push_result(job_str)
            self._log.info(
                "job_id '{}' failed".format(job["job_id"]))
        else:
            self._queue.push_job(job_str)
            self._log.info(
                "job_id '{}' retry".format(job["job_id"]))

    def _purge_timeout(self):
        for job_str in self._storage.pop_timeout():
            job = json.loads(job_str)
            self._log.info(
                "timeout of job_id '{}'".format(job["job_id"]))
            self._manage_fail(job)


    def pickup(self):
        # get a task to do
        #
        # return a instance_id (an id to try to acheve a job) 
        # and a job dict
        if self._queue.job_length() == 0:
            raise Exception("Queue empty")

        job_str = self._queue.pop_job()
        job = json.loads(job_str)
        timeout = job.get("timeout", 30)

        instance_id = str(uuid4())

        self._storage.push(instance_id, job_str, timeout)

        function_name = job["function_name"]
        job_id = job["job_id"]
        self._log.info("Pop function '{}' with job_id '{}' and instance_id '{}'".format(
            function_name, job_id, instance_id))

        return instance_id, job

    def deliver(self, instance_id, result):
        # push a result
        #
        # instance_id : string 
        # result : a dict with keys :
        # * "status": {"success", "failed", "refused"}
        # * ["exception" : "string why it failed"]
        # * "return" : [value, value, ...]

        # next function must raise an exception is instance_id doesn't exist
        job_str = self._storage.pop(instance_id)
        job = json.loads(job_str)
        status = result["status"]

        # good
        if status == "success":
            job["result"] = result # append result to the job
            job_str = json.dumps(job)
            self._queue.push_result(job_str)
            self._log.info("Push success job_id '{}'".format(job["job_id"]))
        # the bot is allowed to refused a job
        elif status == "refused" : 
            self._queue.push_job(job_str) # retry with no fit
            self._log.info("job_id '{}' refused".format(job["job_id"]))
        else: # on failed
            self._manage_fail(job)


