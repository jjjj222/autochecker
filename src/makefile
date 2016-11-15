M2SCORER = ../data/conll14st/m2scorer/scripts/m2scorer.py
SIMPLE_CONLL = ../data/simple/simple.conll
SIMPLE_ANN = ../data/simple/simple.conll.ann
SIMPLE_M2 = ../data/simple/simple.m2
SIMPLE_OUT = ../result/simple.conll.out

run:
	python AutoCorrect.py $(SIMPLE_CONLL) $(SIMPLE_ANN) $(SIMPLE_OUT)

m2_simple:
	$(M2SCORER) $(SIMPLE_OUT) $(SIMPLE_M2)

m2_simple_v:
	$(M2SCORER) -v $(SIMPLE_OUT) $(SIMPLE_M2)
