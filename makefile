MAIN = report
IMAGES := $(wildcard report_images/*)
# Compilers
LATEX = pdflatex
BIBTEX = bibtex

all:$(MAIN).pdf

$(MAIN).pdf: $(MAIN).tex references.bib $(IMAGES)
	$(LATEX) $(MAIN).tex
	$(BIBTEX) $(MAIN)
	$(LATEX) $(MAIN).tex
	$(LATEX) $(MAIN).tex

# Clean aux files
.PHONY: clean

clean:
	rm -f *.aux *.log *.out *.toc *.lof *.lot *.bbl *.blg *.fls *.fdb_latexmk *.synctex.gz *.xml *-blx.bib