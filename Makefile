# List your source files (no extensions)
LIJST = differential-geometry algebraic-geometry complex-geometry physics book

# Automatic file expansions
PDFS = $(patsubst %,%.pdf,$(LIJST))
AUXS = $(patsubst %,%.aux,$(LIJST))

# Commands
PDFLATEX = pdflatex
BIBTEX = bibtex
PYTHON ?= /usr/local/bin/python3.11
PLASTEX ?= /usr/local/bin/plastex
GERBY_FILES ?= basic-math.tex commutative-algebra.tex number-theory.tex differential-geometry.tex differential-topology.tex algebraic-geometry.tex algebraic-topology.tex categories.tex infty-categories.tex complex-analysis.tex complex-geometry.tex symplectic-geometry.tex lie-algebras.tex representation-theory.tex vertex-algebras.tex homological-algebra.tex deformations.tex physics.tex seminars.tex surfaces.tex mumford-tate-groups-in-hodge-theory.tex birational-maps-commutative-algebra.tex cremona-transformations.tex
GERBY_PORT ?= 5001

# Default target: build all PDFs
.PHONY: all
all: $(PDFS)

# Rule to build a PDF from a .tex + .bib
%.pdf: %.tex %.aux
	$(PDFLATEX) $*
	-$(BIBTEX) $*
	$(PDFLATEX) $*
	$(PDFLATEX) $*

# Generate .aux (used by bibtex)
%.aux: %.tex
	$(PDFLATEX) $*

# Clean up all intermediate files
.PHONY: clean
clean:
	rm -f *.aux *.log *.out *.toc *.bbl *.blg *.pdf *.fdb_latexmk *.fls tmp/book.tex

tmp/book.tex:
	python3 scripts/make_book.py > tmp/book.tex

.PHONY: book
book: book.pdf

book.pdf: tmp/book.tex
	pdflatex tmp/book
	bibtex book
	pdflatex tmp/book
	pdflatex tmp/book

.PHONY: gerby-book gerby-tags gerby-render gerby-import gerby-serve gerby-serve-prod gerby-smoke

gerby-book:
	mkdir -p gerby
	$(PYTHON) scripts/make_gerby_book.py $(GERBY_FILES) > gerby/book.tex

gerby-tags: gerby-book
	$(PYTHON) scripts/gerby_tagger.py gerby/book.tex --tags gerby/tags > gerby/tags.tmp
	mv gerby/tags.tmp gerby/tags

gerby-render: gerby-tags
	rm -rf gerby/document
	printf 'y\n' | $(PLASTEX) --renderer=Gerby --tags=gerby/tags --dir=gerby/document gerby/book.tex

gerby-import: gerby-render
	cd gerby-website/gerby/tools && PYTHONPATH=../.. $(PYTHON) update.py

gerby-serve:
	cd gerby-website && PYTHONPATH=. FLASK_APP=gerby $(PYTHON) -m flask run --host 127.0.0.1 --port $(GERBY_PORT)

gerby-serve-prod:
	cd gerby-website && PYTHONPATH=. gunicorn wsgi:application --bind 0.0.0.0:$(GERBY_PORT)

gerby-smoke:
	curl -fsS http://127.0.0.1:$(GERBY_PORT)/tag/0000 >/dev/null
	curl -fsS http://127.0.0.1:$(GERBY_PORT)/browse >/dev/null
