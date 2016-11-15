EXEC = AutoCorrect.py
M2SCORER = ../data/conll14st/m2scorer/scripts/m2scorer.py
SIMPLE_CONLL = ../data/simple/simple.conll
SIMPLE_ANN = ../data/simple/simple.conll.ann
SIMPLE_M2 = ../data/simple/simple.m2
SIMPLE_OUT = ../result/simple.conll.out
SIMPLE_M2_DET = ../data/simple/simple.m2.ArtOrDet

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
	$(M2SCORER) $(SIMPLE_OUT) $(SIMPLE_M2_DET)

simple_m2_v:
	$(M2SCORER) -v $(SIMPLE_OUT) $(SIMPLE_M2_DET)

final:
	python $(EXEC) $(FINAL_CONLL) $(FINAL_ANN) $(FINAL_OUT)

final_m2:
	m2scorer -v $(FINAL_OUT) $(FINAL_M2)
