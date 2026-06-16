# Commands
PDFLATEX = pdflatex
BIBTEX = bibtex
PYTHON ?= python3
PLASTEX ?= $(PYTHON) scripts/plastex_gerby.py
PLASTEXFLAGS ?=
PLASTEX_LOG ?= gerby/plastex.log
GERBY_UPDATE_FLAGS ?=
GERBY_ORDER ?= order-chapters.txt
GERBY_FILES ?= basic-math.tex complex-analysis.tex functional-analysis.tex categories.tex commutative-algebra.tex ringed-spaces.tex schemes.tex homological-algebra.tex lie-algebras.tex representation-theory.tex smooth-manifolds.tex differential-topology.tex algebraic-topology.tex differential-geometry.tex algebraic-geometry.tex symplectic-geometry.tex complex-geometry.tex k3.tex deformations.tex vertex-algebras.tex springer.tex infty-categories.tex seminars.tex geometric-prequantization.tex surfaces.tex nakajima-heisenberg-hilbert-schemes.tex stanley-reisner.tex cremona-transformations.tex derived-categories-of-sheaves.tex geometric-invariant-theory.tex geometric-stability-conditions-and-group-actions.tex moduli-spaces-of-sheaves.tex bridgeland-stability-general-theory.tex noncommutative-abelian-surfaces-and-kummer-type-hyperkahler-varieties.tex mumford-tate-groups-in-hodge-theory.tex hodge-birational-atoms-2026.tex
GERBY_PORT ?= 5001
PDFS = $(patsubst %.tex,%.pdf,$(GERBY_FILES)) book.pdf

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

tmp/book.tex: scripts/make_book.py preamble.tex order-chapters.txt $(GERBY_FILES)
	mkdir -p tmp
	$(PYTHON) scripts/make_book.py --order $(GERBY_ORDER) $(GERBY_FILES) > tmp/book.tex

.PHONY: book
book: book.pdf

book.pdf: tmp/book.tex
	pdflatex tmp/book
	bibtex book
	pdflatex tmp/book
	pdflatex tmp/book

.PHONY: gerby-book gerby-tags gerby-render gerby-import gerby-downloads gerby-deploy-build gerby-serve gerby-serve-prod gerby-smoke

gerby-book:
	mkdir -p gerby
	$(PYTHON) scripts/make_gerby_book.py --order $(GERBY_ORDER) $(GERBY_FILES) > gerby/book.tex

gerby-tags: gerby-book
	$(PYTHON) scripts/gerby_tagger.py gerby/book.tex --tags gerby/tags > gerby/tags.tmp
	mv gerby/tags.tmp gerby/tags

gerby-render: gerby-tags
	rm -rf gerby/document
	printf 'y\n' | $(PLASTEX) $(PLASTEXFLAGS) --renderer=Gerby --tags=gerby/tags --dir=gerby/document gerby/book.tex > $(PLASTEX_LOG) 2>&1 || (tail -n 120 $(PLASTEX_LOG); false)

gerby-import: gerby-render
	cd gerby-website/gerby/tools && PYTHONPATH=../.. $(PYTHON) update.py $(GERBY_UPDATE_FLAGS)

gerby-downloads: book.pdf $(patsubst %.tex,%.pdf,$(GERBY_FILES))
	mkdir -p gerby/downloads
	cp book.pdf gerby/downloads/book.pdf
	cp $(patsubst %.tex,%.pdf,$(GERBY_FILES)) gerby/downloads/

gerby-deploy-build: gerby-import gerby-downloads

gerby-serve:
	cd gerby-website && PYTHONPATH=. FLASK_APP=gerby $(PYTHON) -m flask run --host 127.0.0.1 --port $(GERBY_PORT)

gerby-serve-prod:
	cd gerby-website && PYTHONPATH=. gunicorn wsgi:application --bind 0.0.0.0:$(GERBY_PORT)

gerby-smoke:
	curl -fsS http://127.0.0.1:$(GERBY_PORT)/tag/0000 >/dev/null
	curl -fsS http://127.0.0.1:$(GERBY_PORT)/browse >/dev/null


.PHONY: clean-aux

clean-aux:
	find . -type f \( \
		-name '*.aux' -o \
		-name '*.log' -o \
		-name '*.out' -o \
		-name '*.toc' -o \
		-name '*.bbl' -o \
		-name '*.blg' -o \
		-name '*.fls' -o \
		-name '*.fdb_latexmk' -o \
		-name '*.synctex.gz' \
	\) -delete
