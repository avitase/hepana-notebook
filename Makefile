.PHONY: all clean notebook

all: notebook 

clean:
	docker rmi phd-notebook

notebook: 
	docker build --rm -t hepana-notebook:local .
