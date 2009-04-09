DOC=PvA

all: clean pdf cleanmess

$(DOC).pdf: $(DOC).tex
	texi2pdf $(DOC).tex
clean:
	rm -f $(DOC).dvi $(DOC).ps $(DOC).pdf *.toc *.log *.blg *.bbl *.aux *~

cleanmess:
	rm -f $(DOC).dvi $(DOC).ps *.toc *.log *.blg *.bbl *.aux *~

pdf: $(DOC).pdf