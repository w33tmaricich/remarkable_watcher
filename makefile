install:
	pip3 install -r requirements.txt
test:
	python3 ./tests/tests.py
image:
	docker build -t remarkable_watcher .
drun: image
	docker run -it --rm --name rw remarkable_watcher python ./remarkable_watcher.py
run:
	python3 ./remarkable_watcher.py --watchdir ~/remarkable
