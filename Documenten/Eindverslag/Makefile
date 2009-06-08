DOC=eindverslag

all: clean pdf cleanmess openfile

$(DOC).pdf: $(DOC).tex
	texi2pdf $(DOC).tex
clean:
	rm -f $(DOC).dvi $(DOC).ps $(DOC).pdf *.toc *.log *.blg *.bbl *.aux *~

openfile:
	/usr/bin/open $(DOC).pdf

mess: clean pdf

cleanmess:
	rm -f $(DOC).dvi $(DOC).ps *.toc *.log *.blg *.bbl *.aux *~

pdf: $(DOC).pdf