from sgmllib import SGMLParser
from document import Mistake

class AnnParser(SGMLParser):
    def __init__(self):
        SGMLParser.__init__(self)
        #self.current_mistake = None
        self.mistakes = []
        self.attrs = None
        self.err_type = None
        self.correction = None
        self.data = None

    def get_results(self):
        return self.mistakes

    def start_mistake(self, attrs):
        self.attrs = dict(attrs)

    def end_mistake(self):
        nid = int(self.attrs['nid'])
        pid = int(self.attrs['pid'])
        sid = int(self.attrs['sid'])
        start_token = int(self.attrs['start_token'])
        end_token = int(self.attrs['end_token'])
        err_type = self.err_type
        correction = self.correction

        self.mistakes.append( Mistake(nid, pid, sid, start_token, end_token, err_type, correction) )

    def start_type(self, attrs):
        pass

    def end_type(self):
        self.err_type = self.data

    def start_correction(self, attrs):
        pass

    def end_correction(self):
        self.correction = self.data

    def handle_data(self, data):
        self.data = data

    def dump(self):
        for m in self.mistakes:
            m.dump()


