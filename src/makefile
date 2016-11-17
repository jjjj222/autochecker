EXEC = AutoCorrect.py
M2SCORER = ../data/conll14st/m2scorer/scripts/m2scorer.py
SIMPLE_CONLL = ../data/simple/simple.conll
SIMPLE_ANN = ../data/simple/simple.conll.ann
SIMPLE_OUT = ../result/simple.conll.out
SIMPLE_M2 = ../data/simple/simple.m2.ArtOrDet

SIMPLE2_CONLL = ../data/simple2/simple2.conll
SIMPLE2_ANN = ../data/simple2/simple2.conll.ann
SIMPLE2_OUT = ../result/simple2.conll.out
SIMPLE2_M2 = ../data/simple2/simple2.m2.ArtOrDet

FINAL_CONLL = ../data/artOrDet/official-2014.0.conll
FINAL_ANN = ../data/artOrDet/official-2014.0.conll.ann
FINAL_OUT = ../result/official-2014.0.conll.out
FINAL_M2 = ../data/artOrDet/official-2014.0.m2.ArtOrDet

all:
	python $(EXEC) $(SIMPLE_CONLL) $(SIMPLE_ANN) $(SIMPLE_OUT)

run:
	tmux send-keys -t NLP-p-2:make make Enter

simple:
	python $(EXEC) $(SIMPLE_CONLL) $(SIMPLE_ANN) $(SIMPLE_OUT)

simple_m2:
	$(M2SCORER) -v $(SIMPLE_OUT) $(SIMPLE_M2)

simple2:
	python $(EXEC) $(SIMPLE2_CONLL) $(SIMPLE2_ANN) $(SIMPLE2_OUT)

simple2_m2:
	$(M2SCORER) -v $(SIMPLE2_OUT) $(SIMPLE2_M2)

medium:
	python $(EXEC) ../data/$@/$@.conll ../data/$@/$@.conll.ann ../result/$@.out

final:
	python $(EXEC) $(FINAL_CONLL) $(FINAL_ANN) $(FINAL_OUT)

final_m2:
	$(M2SCORER) -v $(FINAL_OUT) $(FINAL_M2)

qq:
	echo $@
