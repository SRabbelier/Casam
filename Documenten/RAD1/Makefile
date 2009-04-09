DOC=rad1

all: clean pdf cleanmess

$(DOC).pdf: $(DOC).tex
	texi2pdf $(DOC).tex
clean:
	rm -f $(DOC).dvi $(DOC).ps $(DOC).pdf *.toc *.log *.blg *.bbl *.aux *~

mess: clean pdf

cleanmess:
	rm -f $(DOC).dvi $(DOC).ps *.toc *.log *.blg *.bbl *.aux *~

pdf: $(DOC).pdf