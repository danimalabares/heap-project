DECKS := lecture-23 lecture-24

.PHONY: all clean $(DECKS)
all: $(DECKS)

$(DECKS):
	cd $@ && pdflatex -interaction=nonstopmode -halt-on-error $@.tex
	cd $@ && pdflatex -interaction=nonstopmode -halt-on-error $@.tex

clean:
	for d in $(DECKS); do for ext in aux log nav out snm toc vrb fls fdb_latexmk; do rm -f "$$d/$$d.$$ext"; done; done
