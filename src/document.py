import sys

class Word:
    def __init__(self, token_id, token, pos):
        self.id = token_id
        self.token = token
        self.pos = pos

    def __str__(self):
        return self.token

    def dump(self):
        pass

class Sentence:
    def __init__(self, sid):
        self.id = sid
        self.words = []

    def get_id(self):
        return self.id

    def add_word(self, word):
        self.words.append(word)

    def dump(self):
        for w in self.words:
            sys.stdout.write("%s " % w)
        print ""

class Paragraph:
    def __init__(self, pid):
        self.id = pid
        self.sentences = []

    def get_id(self):
        return self.id

    def add_word(self, sid, word):
        if (len(self.sentences) == 0 or sid != self.sentences[-1].get_id()):
            self.sentences.append( Sentence(sid) )

        self.sentences[-1].add_word( word)

    def dump(self):
        for s in self.sentences:
            s.dump()
        print ""


class Document:
    def __init__(self, nid):
        self.id = nid
        self.paragraphs = []

    def get_id(self):
        return self.id

    def add_word(self, pid, sid, word):
        if (len(self.paragraphs) == 0 or pid != self.paragraphs[-1].get_id()):
            self.paragraphs.append( Paragraph(pid) )

        self.paragraphs[-1].add_word(sid, word)

    def dump(self):
        for p in self.paragraphs:
            p.dump()
        print ""

