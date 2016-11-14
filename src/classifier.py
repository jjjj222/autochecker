from collections import defaultdict

class Classifier(object):
    def __init__(self):
        self._labels = []

    def classify_many(self, features_list):
        return [self.classify(f) for f in features_list]

    def labels(self):
        return self._labels

    def accuracy(self, test_set):
        total = 0
        for features, c in test_set:
            if self.classify(features) == c:
                total += 1

        return float(total) / len(test_set)


class MajorityClassifier(Classifier):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.c = None

    def train(self, train_set):
        count = defaultdict(int)
        for features, c in train_set:
            count[c] += 1

        self._labels = count.keys()
        self.c = max(count, key=count.get)

    def classify(self, features):
        return self.c




