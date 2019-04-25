class RedisQueue:
    # adapter for Redis
    # Do no test
    def __init__(self, redis_interface, job_name, result_name):
        # constructor
        #
        # redis_interface : Redis object from redis-py
        # job_name : the key name of job queue
        # result_name : the key name of result queue
        self._redis_interface = redis_interface
        self._job_name = job_name
        self._result_name = result_name

    def job_length(self):
        return self._redis_interface.llen(self._job_name)

    def push_job(self, messsage):
        self._redis_interface.lpush(self._job_name, messsage)

    def pop_job(self):
        message =  self._redis_interface.rpop(self._job_name)
        if message :
            message = message.decode("utf8")
        return message

    def push_result(self, messsage):
        self._redis_interface.lpush(self._result_name, messsage)

    def pop_result(self):
        message = self._redis_interface.rpop(self._result_name)
        if message:
            message = message.decode("utf8")
        return message
