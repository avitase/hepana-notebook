.PHONY: all clean notebook fixpolicy.sh

all: notebook 

fixpolicy.sh:
	wget https://raw.githubusercontent.com/avitase/docker-imagemagick/master/fixpolicy.sh -O fixpolicy.sh
	chmod u+x fixpolicy.sh

clean:
	rm fixpolicy.sh

notebook: fixpolicy.sh
	docker build --rm -t hepana-notebook:local .
