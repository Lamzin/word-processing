#!/usr/bin/python
# -*- coding: UTF-8 -*-


import pickle


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


if __name__ == "__main__":
    print "loaded: "
    with open('train_solved.pkl', 'rb') as input:
        loaded_trains = pickle.load(input)
        # for t in loaded_trains:
            # print t

    trains = [item for item in loaded_trains if not item.is_paraphrase]
    print "trains.len: ", len(trains)

    clone = trains[:]
    for i, item in enumerate(clone):
        item.array_id = i
        item.features[11] /= 500

    eps = 0.001
    metric_count = len(trains[0].features)

    clusters_lvl1 = []
    for feature_id in range(metric_count):
        clone = sorted(clone, key=lambda item: item.features[feature_id])
        min_feature, max_feature = clone[0].features[feature_id], clone[-1].features[feature_id]

        # current_train_ids = []
        # for i in range(len(clone)):
        #     if len(current_train_ids) == 0:
        #         current_train_ids.append(clone[i].array_id)
        #     else:
        #         if clone[i].features[feature_id] - trains[current_train_ids[0]].features[feature_id] < eps:
        #             current_train_ids.append(clone[i].array_id)
        #         else:
        #             clusters_lvl1.append(Cluster([feature_id], current_train_ids))
        #             current_train_ids = []
        # if len(current_train_ids) != 0:
        #     clusters_lvl1.append(Cluster([feature_id], current_train_ids))
        def dummy_split(start):
            h = start
            while h < max_feature:
                current_train_ids = [
                    item.array_id
                    for item in clone
                    if item.features[feature_id] >= h and item.features[feature_id] <= h + eps
                ]
                clusters_lvl1.append(Cluster([feature_id], current_train_ids))
                h += eps
        dummy_split(0)
        dummy_split(eps/2)


    clusters_lvl1 = sorted(clusters_lvl1, key=lambda cl: len(cl.train_ids), reverse=True)
    print "clusters_lvl1: ", len(clusters_lvl1)
    clusters_lvl1 = clusters_lvl1[:5000]

    print len(clusters_lvl1)
    for cl in clusters_lvl1[:50]:
        print cl.feature_ids, len(cl.train_ids)


    clusters_lvl2 = set()
    for i in range(len(clusters_lvl1)):
        for j in range(i + 1, len(clusters_lvl1)):
            if len(clusters_lvl1[i].feature_ids.union(clusters_lvl1[j].feature_ids)) == 2:
                clusters_lvl2.add(clusters_lvl1[i].intersect(clusters_lvl1[j]))
    clusters_lvl2 = list(clusters_lvl2)
    clusters_lvl2 = sorted(clusters_lvl2, key=lambda cl: len(cl.train_ids), reverse=True)
    print "clusters_lvl2: ", len(clusters_lvl2)
    clusters_lvl2 = clusters_lvl2[:5000]

    print len(clusters_lvl2)
    for cl in clusters_lvl2[:50]:
        print cl.feature_ids, len(cl.train_ids)


    clusters_lvl3 = set()
    for cl1 in clusters_lvl1:
        for cl2 in clusters_lvl2:
            if len(cl1.feature_ids.union(cl2.feature_ids)) == 3:
                clusters_lvl3.add(cl1.intersect(cl2))
    clusters_lvl3 = list(clusters_lvl3)
    clusters_lvl3 = sorted(clusters_lvl3, key=lambda cl: len(cl.train_ids), reverse=True)
    clusters_lvl3 = clusters_lvl3[:5000]

    print len(clusters_lvl3)
    for cl in clusters_lvl3[:100]:
        print cl.feature_ids, len(cl.train_ids), list(cl.train_ids)[:10]


    clusters_lvl4 = set()
    for cl1 in clusters_lvl1:
        for cl3 in clusters_lvl3:
            if len(cl1.feature_ids.union(cl3.feature_ids)) == 4:
                clusters_lvl4.add(cl1.intersect(cl3))
    for i in range(len(clusters_lvl2)):
        for j in range(i + 1, len(clusters_lvl2)):
            if len(clusters_lvl2[i].feature_ids.union(clusters_lvl2[j].feature_ids)) == 4:
                clusters_lvl4.add(clusters_lvl2[i].intersect(clusters_lvl2[j]))
    clusters_lvl4 = list(clusters_lvl4)
    clusters_lvl4 = sorted(clusters_lvl4, key=lambda cl: len(cl.train_ids), reverse=True)
    clusters_lvl4 = clusters_lvl4[:5000]

    print len(clusters_lvl4)
    for cl in clusters_lvl4[:100]:
        print cl.feature_ids, len(cl.train_ids), list(cl.train_ids)[:10]
