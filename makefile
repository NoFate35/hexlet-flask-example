starta:
	poetry run flask --app app --debug run --port 8000

starte:
	poetry run flask --app example --debug run --port 8000
	
build:
	./build.sh