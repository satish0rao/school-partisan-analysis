
init:
	virtualenv env

env: requirements.txt
	env/bin/pip install -r requirements.txt

data: data.txt
	cat data.txt | xargs wget -P ./seda/


