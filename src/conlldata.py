from myutil import *
from document import *
from parser import AnnParser

class ConllData:
    def __init__(self, conll_file, ann_file):
        self.documents = parse_conll_file(conll_file)

        mistakes = parse_ann_file(ann_file)
        self._add_mistakes_to_docs(self.documents, mistakes)
        self._process_synt()

    def get_ArtOrDet_candidates(self):
        result = []

        for d in self.documents:
            result += d.get_ArtOrDet_candidates()

        return result
    #def coorVV
    #def concordance(self, 
    #    for d in documents:
    #        d.show_the()
    #def show_error(self, err_type):
    #    for d in documents:
    #        d.show_error(err_type)

    #def getArtOrDetErrors(



    def _add_mistakes_to_docs(self, documents, mistakes):
        id2doc = dict([ (d.id, d) for d in documents ])

        for m in mistakes:
            id2doc[ m.nid ].add_mistake(m)

    def _process_synt(self):
        self.documents[0][1][0]._process_synt()
        #for d in self.documents:
        #    for p in d.paragraphs:
        #        for s in p.sentences:
        #            s._process_synt()


    def dump(self):
        for d in self.documents:
            d.dump()

def parse_conll_file(filename):
    results = []

    data = parse_space_separated_file(filename)

    document = None
    for line in data:
        if len(line) == 0:
            continue
        elif len(line) != 9:
            print "Format Error"
            continue

        NID, PID, SID, TOKENID, TOKEN, POS, DPHEAD, DPREL, SYNT = line
        NID = int(NID)
        PID = int(PID)
        SID = int(SID)
        TOKENID = int(TOKENID)

        if document == None or document.id != NID:
            if document != None:
                results.append(document)
            document = Document(NID)

        word = Word(TOKENID, TOKEN, POS, SYNT)
        document.add_word(PID, SID, word)

    results.append(document)
    return results

def parse_ann_file(filename):
    results = []

    f = open(filename, 'r')
    parser = AnnParser()
    raw = f.read()

    parser.feed(raw)
    results =  parser.get_results()
    return results

