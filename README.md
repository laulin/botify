Botify is a library to create a botnet infrastructure. It is 
scalable and easy to use. Now let's look how !

# Example

submitter.py :

~~~~
import redis
from botify.redis_queue import RedisQueue
from botify.submitter import Submitter

r = redis.Redis()
redis_queue = RedisQueue(r, "job", "result")
submitter = Submitter(2, 1024, redis_queue)

# ...

submitter.submit("ping", ip="127.0.0.1")

# ...

job_id, job = submitter.pickuo()
~~~~

publisher.py

~~~~
import redis
from botify.redis_queue import RedisQueue
from botify.publisher import Publisher
from botify.sqlite3_storage import SQLite3Storage

r = redis.Redis()
redis_queue = RedisQueue(r, "job", "result")
sqlite_storage = SQLite3Storage()
publisher = Publisher(redis_queue, sqlite_storage)

# ...

instance_id, job = publisher.pickup()

# ...

publisher.deliver(instance_id, result)
~~~~
