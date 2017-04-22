#!/usr/bin/python
# -*- coding: UTF-8 -*-


import pickle
from sklearn import svm


class Train(object):
    def __init__(self, is_paraphrase, id1, id2, s1, s2):
        self.id1 = id1
        self.id2 = id2
        self.s1 = s1
        self.s2 = s2
        self.is_paraphrase = is_paraphrase

    def run(self):
        self.features = ParaphraseTest(self.s1, self.s2).get_features()

    def __str__(self):
        return '{0}: {1}'.format(self.is_paraphrase, self.features)


class Classifier(object):
    def __init__(self, clusters, trains, trains_all):
        self.feature_ids = set()
        for cl in clusters:
            self.feature_ids.update(cl.feature_ids)

        X = []
        Y = []
        for cl in clusters:
            for id in cl.train_ids:
                X.append(self._filter_features(trains[id].features))
                Y.append(1 if trains[id].is_paraphrase else 0)
        for tr in trains_all:
            X.append(self._filter_features(tr.features))
            Y.append(1 if tr.is_paraphrase else 0)
        self.clf = svm.SVC()
        self.clf.fit(X, Y)

    def _filter_features(self, features):
        return [f for i, f in enumerate(features) if i in self.feature_ids]

    def predict(self, tests):
        X = [self._filter_features(t.features) for t in tests]
        return self.clf.predict(X)


class Cluster(object):

    def __init__(self, feature_ids, train_ids):
        self.feature_ids = set(feature_ids)
        self.train_ids = set(train_ids)

    def intersect(self, other):
        return Cluster(self.feature_ids.union(other.feature_ids), self.train_ids.intersection(other.train_ids))

    def __hash__(self):
        return hash(tuple(sorted(self.feature_ids))) + hash(tuple(sorted(self.train_ids)))

    def __eq__(self, other):
        return self.feature_ids == other.feature_ids and self.train_ids == other.train_ids


def get_trains():
    with open('train_solved.pkl', 'rb') as input:
        trains_all = pickle.load(input)
    for i, item in enumerate(trains_all):
        item.features[11] /= 500
    trains_pos = [item for item in trains_all if item.is_paraphrase]
    trains_neg = [item for item in trains_all if not item.is_paraphrase]
    for i, item in enumerate(trains_pos):
        item.array_id = i
    for i, item in enumerate(trains_neg):
        item.array_id = i
    return trains_all, trains_pos, trains_neg


def get_tests():
    with open('test_solved.pkl', 'rb') as input:
        tests = pickle.load(input)
    for i, item in enumerate(tests):
        item.features[11] /= 500
    return tests


def classify(trains, eps, l_max, top=200):
    trains = trains[:]
    lvls = {1: set()}
    for feature_id in range(len(trains[0].features)):
        trains = sorted(trains, key=lambda item: item.features[feature_id])
        def dummy_split(start):
            h = start
            while h < trains[-1].features[feature_id]: # max feature value
                current_train_ids = [
                    item.array_id
                    for item in trains
                    if item.features[feature_id] >= h and item.features[feature_id] <= h + eps
                ]
                lvls[1].add(Cluster([feature_id], current_train_ids))
                h += eps
        dummy_split(0)
        dummy_split(eps/2)
    lvls[1] = list(lvls[1])
    lvls[1] = sorted(lvls[1], key=lambda cl: len(cl.train_ids), reverse=True)[:top]

    for level in range(2, l_max + 1):
        lvls[level] = set()
        for level1 in range(1, (level + 1) // 2 + 1):
            level2 = level - level1
            for cl1 in lvls[level1]:
                for cl2 in lvls[level2]:
                    if len(cl1.feature_ids.union(cl2.feature_ids)) == level:
                        lvls[level].add(cl1.intersect(cl2))
        lvls[level] = list(lvls[level])
        lvls[level] = sorted(lvls[level], key=lambda cl: len(cl.train_ids), reverse=True)[:top]
        # print ''
        # for cl in lvls[level][:20]:
            # print cl.feature_ids, len(cl.train_ids), sorted(list(cl.train_ids))[:10]
    return lvls


def split_by_clusters(trains):
    clusters = []
    used = {item.array_id: 0 for item in trains}

    for eps in range(1, 40):
        print "eps: ", float(eps) / 100
        print "used: ", len([k for k, v in used.items() if v >= 2])

        trains_ = [item for item in trains if used[item.array_id] < 2]
        if len(trains_) == 0:
            break

        l = 3
        cls = classify(trains_, float(eps) / 100, l_max=l, top=100)[l]
        for cl in cls:
            sz = len(cl.train_ids)
            if sz > 200:
                print cl.feature_ids, len(cl.train_ids)
                for id in cl.train_ids:
                    used[id]+=1
                clusters.append(cl)

    print len(clusters)
    for cl in clusters:
        print cl.feature_ids, len(cl.train_ids), sorted(list(cl.train_ids))[:10]

    check_used = {}
    for cl in clusters:
        for item in cl.train_ids:
            check_used[item] = check_used[item] + 1 if item in check_used else 1
    print "\nwithout cluster: ", len([0 for _, v in check_used.items() if v == 0])

    return clusters


def test_one_layer_classifier():
    trains_all, trains_pos, trains_neg = get_trains()

    X = [
        v.features
        for v in trains_all
    ]
    Y = [
        1 if v.is_paraphrase else 0
        for v in trains_all
    ]
    clf = svm.SVC()
    clf.fit(X, Y)

    tests = get_tests()
    count = [[.0, .0], [.0, .0]]
    for i, answer in enumerate(clf.predict([t.features for t in tests])):
        count[1 if tests[i].is_paraphrase else 0][answer] += 1
    precision = count[1][1] / (count[1][1] + count[0][1])
    recall = count[1][1] / (count[1][1] + count[1][0])
    accuracy = (count[0][0] + count[1][1]) / len(tests)
    F = 2 * precision * recall / (precision + recall)
    print "one layer classifier"
    print "precision: {}, recall: {}, accuracy: {}, F: {}".format(precision, recall, accuracy, F)


def test_two_layer_classifier():
    trains_all, trains_pos, trains_neg = get_trains()

    # clusters_pos = split_by_clusters(trains_pos)
    # clusters_neg = split_by_clusters(trains_neg)
    # with open('clusters.pkl', 'wb') as output:
    #     pickle.dump(clusters_pos, output, pickle.HIGHEST_PROTOCOL)
    #     pickle.dump(clusters_neg, output, pickle.HIGHEST_PROTOCOL)
    # return

    def expand_features(clfs, feature_set):
        X = [tr.features for tr in feature_set]
        Y = [1 if tr.is_paraphrase else 0 for tr in feature_set]
        for clf in clfs:
            predictions = clf.predict(feature_set)
            for i, pr in enumerate(predictions):
                X[i].append(pr)
                X[i].extend(clf._filter_features(feature_set[i].features))
        return X, Y

    def make_classifier_lvl2():
        with open('clusters.pkl', 'rb') as input:
            clusters_pos = pickle.load(input)
            clusters_neg = pickle.load(input)

        clfs = []
        for cluster in clusters_pos:
            clfs.append(Classifier([cluster], trains_pos, trains_neg))
        for cluster in clusters_neg:
            clfs.append(Classifier([cluster], trains_neg, trains_pos))

        X, Y = expand_features(clfs, trains_all)
        clf_lvl2 = svm.SVC()
        clf_lvl2.fit(X, Y)
        return clfs, clf_lvl2

    def test(clfs, clf_lvl2):
        tests = get_tests()
        X, Y = expand_features(clfs, tests)

        count = [[.0, .0], [.0, .0]]
        for i, pr in enumerate(clf_lvl2.predict(X)):
            count[Y[i]][pr] += 1
        precision = count[1][1] / (count[1][1] + count[0][1])
        recall = count[1][1] / (count[1][1] + count[1][0])
        accuracy = (count[0][0] + count[1][1]) / len(tests)
        F = 2 * precision * recall / (precision + recall)
        print "two layers classifier"
        print "precision: {}, recall: {}, accuracy: {}, F: {}".format(precision, recall, accuracy, F)

    clfs, clf_lvl2 = make_classifier_lvl2()
    test(clfs, clf_lvl2)


if __name__ == "__main__":
    test_one_layer_classifier()
    test_two_layer_classifier()
