.PHONY: all
all: handbook.html

.PHONY: clean
clean:
	rm -f *.html *.pdf *~

handbook.html: $(wildcard *.txt)
	asciidoc -b html5 handbook.txt

.PHONY: upload
upload:
	rsync -av --delete handbook.html images \
		oe-lite.org:/srv/http/doc/handbook/
