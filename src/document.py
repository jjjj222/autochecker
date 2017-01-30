import sys
import pdb

EMPTY_STR = ''
TARGET_DET = [EMPTY_STR, 'a', 'an', 'the']

#-------------------------------------------------------------------------------
#   Mistake
#-------------------------------------------------------------------------------
class Mistake:
    def __init__(self, nid, pid, sid, start_token, end_token, err_type, correction):
        self.nid = nid
        self.pid = pid
        self.sid = sid
        self.start_token = start_token
        self.end_token = end_token
        self.err_type = err_type
        self.correction = correction

        self.sentence = None

    def __eq__(self, other):
        if other is None:
            return False

        return self._all_data() == other._all_data()

    def __ne__(self, other):
        return not __eq__()

    def __hash__(self):
        return hash(self._all_data())

    def _all_data(self):
        return (self.nid, self.pid, self.sid, self.start_token, self.end_token, self.err_type,\
            self.correction.lower())

    def orig_text(self):
        t = []
        for i in range(self.start_token, self.end_token):
            t.append(self.sentence[i].token)

        return ' '.join(t)

    def show_in_sentence(self):
        #pdb.set_trace()
        id2word = dict([(w.id, w.token) for w in self.sentence])

        if self.start_token == self.end_token:
            id2word[self.start_token - 0.5] = "[%s]" % self.correction
        else:
            id2word[self.start_token] = "(%s" % id2word[self.start_token]
            id2word[self.end_token-1] = "%s)" % id2word[self.end_token-1]
            if self.correction != "":
                id2word[self.end_token-1] += "[%s]" % self.correction

        return ' '.join( [w for k, w in sorted(id2word.items())] )

    def dump(self):
        print self.nid, self.pid, self.sid, "[%d:%d]" % (self.start_token, self.end_token),\
            "<%s>" % self.err_type, "(%s)->[%s]" % (self.orig_text(), self.correction)

#-------------------------------------------------------------------------------
#   Word
#-------------------------------------------------------------------------------
class Word:
    def __init__(self, nid, pid, sid, token_id, token, pos, dphead, dprel, synt):
        self.nid = nid
        self.pid = pid
        self.sid = sid
        self.id = token_id
        self.token = token
        self.pos = pos
        self.dphead = dphead
        self.dprel = dprel
        self.synt = synt

        self.sentence = None
        self.node = None

    def prev_word(self):
        if self.id == 0:
            return None
        return self.sentence[self.id-1]

    def __str__(self):
        return "%s/%s/%s" % (self.token, self.pos, self.node)

    def dump(self):
        print self.nid, self.pid, self.sid, self.id, self.token, self.pos, self.dphead, self.dprel


#-------------------------------------------------------------------------------
#   Sentence
#-------------------------------------------------------------------------------
class Sentence:
    def __init__(self, sid):
        self.id = sid
        self.words = []
        self._mistakes = []

    def get_ArtOrDet_candidates(self):
        result = []

        in_np = False
        for w in self.words:
            if w.node == "NP":
                if not in_np:
                    in_np = True
                    result.append(w)
            else:
                in_np = False

        return result

    def get_mistake(self, w, err_type=None):
        for m in self._mistakes:
            if m.err_type == err_type:
                if m.start_token == m.end_token and m.start_token == w.id:
                    return m
                elif w.id in range(m.start_token, m.end_token):
                    return m

        return None

    def add_word(self, word):
        assert word.id == len(self.words)
        self.words.append(word)
        word.sentence = self

    def add_mistake(self, m):
        assert self.id == m.sid
        self._mistakes.append(m)
        m.sentence = self

    def mistakes(self, err_type = None):
        for m in self._mistakes:
            if err_type == None or m.err_type == err_type:
                yield m

    def filter_mistakes(self):
        new_mistakes = []
        for m in self._mistakes:
            if m.err_type != "ArtOrDet":
                continue

            orig = m.orig_text().lower()
            correction = m.correction.lower()

            if not correction in TARGET_DET:
                continue

            if not orig in TARGET_DET:
                continue

            if correction == "an" and orig == "a":
                continue

            if correction == "a" and orig == "an":
                continue

            if correction == "an":
                m.correction = 'a'

            new_mistakes.append(m)

        self._mistakes = new_mistakes


    def _process_synt(self):
        tree_text = ""
        node = ""
        i = 0

        for w in self.words:
            tree_text += w.synt
            while tree_text[i] != '*':
                if tree_text[i] == '(' or tree_text[i] == ')':
                    node = ""
                else:
                    node += tree_text[i]
                i += 1
            i += 1
            w.node = node

    def __len__(self):
        return len(self.words)

    def __getitem__(self, i):
        return self.words[i]

    def __str__(self):
        return ' '.join([w.token for w in self.words])

    def tagged_text(self):
        return ' '.join([w.__str__() for w in self.words])

    def correct_text(self, err_type = None):
        id2word = dict([(w.id, w.token) for w in self.words])
        #print id2word

        #print id2word
        for m in self._mistakes:
            if err_type != None and m.err_type != err_type:
                continue

            if m.start_token == m.end_token:
                id2word[m.start_token - 0.5] = "%s" % m.correction
            else:
                for i in range(m.start_token, m.end_token):
                    del id2word[i]
                id2word[m.start_token] = m.correction

        #if self.start_token == self.end_token:
        #    id2word[self.start_token + 0.5] = "[%s]" % self.correction
        #else:
        #    id2word[self.start_token] = "(%s" % id2word[self.start_token]
        #    id2word[self.end_token-1] = "%s)" % id2word[self.end_token-1]
        #    if self.correction != "":
        #        id2word[self.end_token-1] += "[%s]" % self.correction
        #print id2word

        return ' '.join( [w for k, w in sorted(id2word.items())] )
        #pass
 


    def dump(self):
        for w in self.words:
            sys.stdout.write("%s " % w)
        print ""
        for m in self._mistakes:
            m.dump()

#-------------------------------------------------------------------------------
#   Paragraph
#-------------------------------------------------------------------------------
class Paragraph:
    def __init__(self, pid):
        self.id = pid
        self.sentences = []

    def get_ArtOrDet_candidates(self):
        result = []

        for s in self.sentences:
            result += s.get_ArtOrDet_candidates()

        return result

    def add_word(self, sid, word):
        if (len(self.sentences) == 0 or sid != self.sentences[-1].id):
            self.sentences.append( Sentence(sid) )

        assert self.sentences[-1].id == len(self.sentences) - 1
        self.sentences[-1].add_word( word)

    def add_mistake(self, m):
        assert self.id == m.pid
        self.sentences[m.sid].add_mistake(m)

    def mistakes(self, err_type = None):
        for s in self.sentences:
            for m in s.mistakes(err_type):
                yield m

    def __getitem__(self, i):
        return self.sentences[i]

    def dump(self):
        for s in self.sentences:
            s.dump()
        print ""


#-------------------------------------------------------------------------------
#   Document
#-------------------------------------------------------------------------------
class Document:
    def __init__(self, nid):
        self.id = nid
        self.paragraphs = []

    def get_ArtOrDet_candidates(self):
        result = []

        for p in self.paragraphs:
            result += p.get_ArtOrDet_candidates()

        return result

    def add_word(self, pid, sid, word):
        if (len(self.paragraphs) == 0 or pid != self.paragraphs[-1].id):
            self.paragraphs.append( Paragraph(pid) )

        assert self.paragraphs[-1].id == len(self.paragraphs) - 1
        self.paragraphs[-1].add_word(sid, word)

    def add_mistake(self, m):
        assert self.id == m.nid
        self.paragraphs[m.pid].add_mistake(m)

    def mistakes(self, err_type = None):
        for p in self.paragraphs:
            for m in p.mistakes(err_type):
                yield m

    def sentences(self):
        for p in self.paragraphs:
            for s in p.sentences:
                yield s

    def __getitem__(self, i):
        return self.paragraphs[i]

    def dump(self):
        for p in self.paragraphs:
            p.dump()
        print ""

