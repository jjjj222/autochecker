import sys

class Mistake:
    def __init__(self, nid, pid, sid, start_token, end_token, err_type, correction):
        self.nid = nid
        self.pid = pid
        self.sid = sid
        self.start_token = start_token
        self.end_token = end_token
        self.err_type = err_type
        self.correction = correction

    def dump(self):
        print self.nid, self.pid, self.sid, "[%d:%d]" % (self.start_token, self.end_token),\
            "<%s>" % self.err_type, self.correction

class Word:
    def __init__(self, nid, pid, sid, token_id, token, pos, synt):
        self.nid = nid
        self.pid = pid
        self.sid = sid
        self.id = token_id
        self.token = token
        self.pos = pos
        self.synt = synt

        self.node = None

    def __str__(self):
        return "%s/%s/%s" % (self.token, self.pos, self.node)

    def dump(self):
        print self.nid, self.pid, self.sid, self.id, self.token

class Sentence:
    def __init__(self, sid):
        self.id = sid
        self.words = []
        self.mistakes = []

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

    def get_mistake(self, w):
        for m in self.mistakes:
            if m.err_type == "ArtOrDet":
                if m.start_token == m.end_token and m.start_token == w.id:
                    #print "missing", w, "->", m.correction
                    return m
                elif m.start_token == w.id and m.end_token == w.id + 1:
                    #print "wrong det", w, "->", m.correction
                    return m

        return None

    def add_word(self, word):
        assert word.id == len(self.words)
        self.words.append(word)

    def add_mistake(self, m):
        assert self.id == m.sid
        self.mistakes.append(m)

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

    def __getitem__(self, i):
        return self.words[i]

    def get_plain_text(self):
        return ' '.join([w.token for w in self.words])

    def dump(self):
        for w in self.words:
            sys.stdout.write("%s " % w)
        print ""
        for m in self.mistakes:
            m.dump()

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

    def __getitem__(self, i):
        return self.sentences[i]

    def dump(self):
        for s in self.sentences:
            s.dump()
        print ""


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

    def __getitem__(self, i):
        return self.paragraphs[i]

    def dump(self):
        for p in self.paragraphs:
            p.dump()
        #for m in self.mistakes:
        #    m.dump()
        print ""

