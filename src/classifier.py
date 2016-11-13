from collections import defaultdict

class MajorityClassifier:
    def __init__(self):
        self.c = None
        pass

    def train(self, train_set):
        count = defaultdict(int)
        for features, c in train_set:
            count[c] += 1

        self.c = max(count, key=count.get)

    def classify(self, features):
        return self.c

    def accuracy(self, test_set):
        total = 0
        for features, c in test_set:
            if self.classify(features) == c:
                total += 1

        return float(total) / len(test_set)


