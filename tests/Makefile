BETA = ../beta.py
BASES = $(basename $(wildcard *.bta))

all: $(addsuffix .output,$(BASES))

%.output: %.input %.bta
	$(BETA) $(addsuffix .bta,$(basename $<)) < $< > $@
	diff $@ $(addsuffix .original,$(basename $<)) 

clean:
	rm *.output

%.original: %.input %.bta
	$(BETA) $(addsuffix .bta,$(basename $<)) < $< > $@
