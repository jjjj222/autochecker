#!/bin/bash -f
script_dir="/Users/jjjj222/Documents/Dropbox/2016_fall/NLP/project/autochecker/data/nucle3.2/scripts"
m2filter="/Users/jjjj222/Documents/Dropbox/2016_fall/NLP/project/autochecker/src/m2filter.py"

data_dir="/Users/jjjj222/Documents/Dropbox/2016_fall/NLP/project/autochecker/data/simple2"
sgml_file="$data_dir/simple2.sgml"
conll_file="$data_dir/simple2.conll"
ann_file="$conll_file.ann"
m2_file="$data_dir/simple2.m2"

cd $script_dir
python preprocess.py -o $sgml_file $conll_file $ann_file $m2_file
python $m2filter $m2_file  ArtOrDet
#cd /Users/jjjj222/Documents/Dropbox/2016_fall/NLP/project/autochecker/data/nucle3.2/scripts
#python preprocess.py -o /Users/jjjj222/Documents/Dropbox/2016_fall/NLP/project/autochecker/data/simple/simple.sgml /Users/jjjj222/Documents/Dropbox/2016_fall/NLP/project/autochecker/data/simple/simple.conll /Users/jjjj222/Documents/Dropbox/2016_fall/NLP/project/autochecker/data/simple/sipmle.conll.ann /Users/jjjj222/Documents/Dropbox/2016_fall/NLP/project/autochecker/data/simple/simple.m2
#python /Users/jjjj222/Documents/Dropbox/2016_fall/NLP/project/autochecker/src/m2filter.py /Users/jjjj222/Documents/Dropbox/2016_fall/NLP/project/autochecker/data/simple/simple.m2 ArtOrDet
