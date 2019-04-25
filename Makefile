build_package:
	python3 setup.py build sdist bdist_wheel

unittest:
	export PYTHONPATH="${PYTHONPATH}:botify"; python3 test/test_submitter.py
	export PYTHONPATH="${PYTHONPATH}:botify"; python3 test/test_publisher.py
	export PYTHONPATH="${PYTHONPATH}:botify"; python3 test/test_sqlite3_storage.py
	# test/test_redis_queue.py must be run in docker, redis is needed

build_docker: build_package
	docker build -t test_botify .

run_docker: build_docker 
	docker run -it --rm test_botify /bin/bash

clear:
	rm -rf build dist botify.egg-info