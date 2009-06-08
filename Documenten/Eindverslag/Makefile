DOC=eindverslag

UNAME_S := $(shell sh -c 'uname -s 2>/dev/null || echo not')

ifeq ($(UNAME_S), Linux)
    OPENER=evince
else
    OPENER=/usr/bin/open
endif

all: clean pdf cleanmess openfile

$(DOC).pdf: $(DOC).tex
	texi2pdf $(DOC).tex

pdf: $(DOC).pdf

cleanmess:
	rm -f $(DOC).dvi $(DOC).ps *.toc *.log *.blg *.bbl *.aux *~

clean: cleanmess
	rm -f $(DOC).pdf

mess: clean pdf

openfile:
	$(OPENER) $(DOC).pdf

