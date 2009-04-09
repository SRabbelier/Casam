DOC=PvA
BIB=PvA.bib

all: pdf ps

$(DOC).dvi: $(DOC).tex
	latex $(DOC)
	bibtex $(DOC)
	latex $(DOC)
	latex $(DOC)

clean:
	rm -f $(DOC).dvi $(DOC).ps $(DOC).pdf *.toc *.log *.blg *.bbl *.aux *~

%.ps: %.dvi
	dvips -f $(DOC).dvi > $(DOC).ps

%.pdf: %.ps
	ps2pdf $(DOC).ps $(DOC).pdf

pdf: $(DOC).pdf

ps: $(DOC).ps
