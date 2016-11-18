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

ALL_CONLL = ../data/nucle3.2/preprocessed_data/nucle3.2-preprocessed.conll
ALL_ANN = ../data/nucle3.2/preprocessed_data/nucle3.2-preprocessed.conll.ann
ALL_OUT = ../result/all.out

RUN_CASE = python $(EXEC) ../data/$@/$@.conll ../data/$@/$@.conll.ann ../result/$@.out
#RUN_CASE = python -m pdb $(EXEC) ../data/$@/$@.conll ../data/$@/$@.conll.ann ../result/$@.out

#tmp:
#	python ResultGather.py simple

tmp2:
	python ParameterSearch.py simple

simple:
	$(RUN_CASE)

simple2:
	$(RUN_CASE)

medium:
	$(RUN_CASE)

final:
	$(RUN_CASE)

all:
	$(RUN_CASE)

simple_m2:
	$(M2SCORER) -v $(SIMPLE_OUT) $(SIMPLE_M2)

simple2_m2:
	$(M2SCORER) -v $(SIMPLE2_OUT) $(SIMPLE2_M2)

	@#python $(EXEC) ../data/$@/$@.conll ../data/$@/$@.conll.ann ../result/$@.out

#final:
#	python $(EXEC) $(FINAL_CONLL) $(FINAL_ANN) $(FINAL_OUT)
#
#all:
#	python $(EXEC) $(ALL_CONLL) $(ALL_ANN) $(ALL_OUT)

final_m2:
	$(M2SCORER) -v $(FINAL_OUT) $(FINAL_M2)
