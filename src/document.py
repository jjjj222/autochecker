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
        print "M:", self.nid, self.pid, self.sid, "[%d:%d]" % (self.start_token, self.end_token),\
            "<%s>" % self.err_type, self.correction

class Word:
    def __init__(self, token_id, token, pos):
        self.id = token_id
        self.token = token
        self.pos = pos

    def get_id(self):
        return self.id

    def __str__(self):
        return self.token

    def dump(self):
        pass

class Sentence:
    def __init__(self, sid):
        self.id = sid
        self.words = []
        self.mistakes = []

    def add_word(self, word):
        assert word.get_id() == len(self.words)
        self.words.append(word)

    def add_mistake(self, m):
        assert self.id == m.sid
        self.mistakes.append(m)

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

    def add_word(self, sid, word):
        if (len(self.sentences) == 0 or sid != self.sentences[-1].id):
            self.sentences.append( Sentence(sid) )

        assert self.sentences[-1].id == len(self.sentences) - 1
        self.sentences[-1].add_word( word)

    def add_mistake(self, m):
        assert self.id == m.pid
        self.sentences[m.sid].add_mistake(m)

    def dump(self):
        for s in self.sentences:
            s.dump()
        print ""


class Document:
    def __init__(self, nid):
        self.id = nid
        self.paragraphs = []

    def add_word(self, pid, sid, word):
        if (len(self.paragraphs) == 0 or pid != self.paragraphs[-1].id):
            self.paragraphs.append( Paragraph(pid) )

        assert self.paragraphs[-1].id == len(self.paragraphs) - 1
        self.paragraphs[-1].add_word(sid, word)

    def add_mistake(self, m):
        assert self.id == m.nid
        self.paragraphs[m.pid].add_mistake(m)

    def dump(self):
        for p in self.paragraphs:
            p.dump()
        #for m in self.mistakes:
        #    m.dump()
        print ""

