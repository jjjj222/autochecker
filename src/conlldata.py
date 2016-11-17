from myutil import *
from document import *
from parser import AnnParser

class Candidate:
    def __init__(self, word):
        self.word = word
        #self.klass = None

    def get_determiner(self):
        if self.word.pos == "DT":
            return self.word.token.lower()

        prev_word = self.word.prev_word()
        if prev_word != None and prev_word.pos == "DT":
            return prev_word.token.lower()

        return EMPTY_STR

    def get_determiner_class(self):
        result = self.get_correct_determiner()
        if result == "an":
            result = "a"
        return result

    def get_correct_determiner(self):
        m = self.word.sentence.get_mistake(self.word, "ArtOrDet")

        if m == None:
            return self.get_determiner()
        else:
            if m.correction == "":
                return EMPTY_STR
            return m.correction.lower()

    def generate_mistake(self, result):
        c = self.get_determiner()
        if result == c:
            return None

        if result == "a" and c == "an":
            return None

        if result == EMPTY_STR:
            m = Mistake(self.word.nid, self.word.pid, self.word.sid, self.word.id,\
                self.word.id+1, "ArtOrDet", "")
        else:
            if c == EMPTY_STR:
                m = Mistake(self.word.nid, self.word.pid, self.word.sid, self.word.id,\
                    self.word.id, "ArtOrDet", result)
            else:
                m = Mistake(self.word.nid, self.word.pid, self.word.sid, self.word.id,\
                    self.word.id+1, "ArtOrDet", result)

        m.sentence = self.word.sentence
        #m.dump()
        #if m.pid == 3 and m.sid == 4:
        #    pdb.set_trace()
        return m

    def is_target(self):
        return self.get_determiner() in TARGET_DET and self.get_correct_determiner() in TARGET_DET

    def dump(self):
        self.word.dump()
        #print self.word.sentence
        #print self.word.sentence.tagged_text()
        #print self.word, self.get_determiner(), self.get_correct_determiner()


def get_candidates(documents):
    words = []
    for d in documents:
        words += d.get_ArtOrDet_candidates()

    candidates = [Candidate(w) for w in words if Candidate(w).is_target()]
    return candidates

def get_target_mistakes(documents):
    result = []
    for d in documents:
        for m in d.mistakes("ArtOrDet"):
            if not m.correction in TARGET_DET:
                continue

            if not m.orig_text() in TARGET_DET:
                continue

            result.append(m)

    return result

#def get_mistakes(documents):
#    result = []
#    for d in documents:
#        for m in d.mistakes("ArtOrDet"):
#            result.append(m)
#
#    return result


class ConllData:
    def __init__(self, conll_file, ann_file):
        self.documents = []
        self.id2doc = {}

        self.documents = parse_conll_file(conll_file)
        mistakes = parse_ann_file(ann_file)
        self._add_mistakes_to_docs(self.documents, mistakes)
        self._process_synt()

    def get_ArtOrDet_candidates(self):
        result = []

        for d in self.documents:
            result += d.get_ArtOrDet_candidates()

        return result

    def get_mistake(self, w):
        s = self.get_sentence(w.nid, w.pid, w.sid)
        return s.get_mistake(w)

    def get_sentence(self, nid, pid, sid):
        return self.id2doc[nid][pid][sid]

    def mistakes(self, err_type = None):
        for d in self.documents:
            for m in d.mistakes(err_type):
                yield m

    def sentences(self):
        for d in self.documents:
            for s in d.sentences():
                yield s

    def filter_mistakes(self):
        for s in self.sentences():
            s.filter_mistakes()

    def _add_mistakes_to_docs(self, documents, mistakes):
        self.id2doc = dict([ (d.id, d) for d in documents ])

        for m in mistakes:
            self.id2doc[ m.nid ].add_mistake(m)

    def _process_synt(self):
        #self.documents[0][1][0]._process_synt()
        for d in self.documents:
            for p in d.paragraphs:
                for s in p.sentences:
                    s._process_synt()

    #def for_all_sentences(self, fn):
    #    for d in self.documents:
    #        for p in d.paragraphs:
    #            for s in p.sentences:
    #                fn(s)

    def __getitem__(self, i):
        return self.documents[i]


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

        word = Word(NID, PID, SID, TOKENID, TOKEN, POS, SYNT)
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

