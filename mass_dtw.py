# -*- coding: utf-8 -*-
import time
from collections import defaultdict
from dtw import Dtw


def gen_dict_label(file_label):
    dict_label = {}
    for line in file_label.split('\n'):
        try:
            index, label = line.split('\t', 1)
            dict_label[index] = label
        except:
            pass
    return dict_label


def gen_dict_base(file_base):
    dict_base = defaultdict(list)
    for line in file_base.split('\n'):
        try:
            index, serie = line.split(' ', 1)
            dict_base[index].append(serie.split(' '))
        except:
            pass
    return dict(dict_base)


def gen_list_compare(file_compare):
    list_compare = []
    for line in file_compare.split('\n'):
        try:
            label, serie = line.split(' ', 1)
            list_compare.append([label, serie.split(' ')])
        except:
            pass
    return list_compare


class MassDtw(object):
    def __init__(self, file_base, file_compare, sc_band=100, file_label=None):
        # Files
        self._file_base = file_base
        self._file_compare = file_compare
        self._file_label = file_label

        # Flag Sakoe‐Chiba band
        self._sc_band = int(sc_band)

        # Dictionaies and lists, generated
        self._dict_label = gen_dict_label(file_label)
        self._dict_base = gen_dict_base(file_base)
        self._list_compare = gen_list_compare(file_compare)

        # Minimum dtw value until now. It's two temporary variables for
        # internal use only. Please, avoid change this outsite `.run()`
        self._min_dtw = float('inf')
        self._min_label = float('inf')

        # ===== Benchmark only. =====
        # Count number of hits and misses on this implementation.
        # If calculated_label == real_label: count_hit+=1; else: count_miss+=1
        self._count_hit = 0
        self._count_miss = 0

        # ===== Benchmark only. =====
        # Time to execute `.run()`
        self._time_last_run = 0

    @property
    def _hit_ratio(self):
        try:
            hit_ratio = self._count_hit / (self._count_hit + self._count_miss)
        except ZeroDivisionError:
            hit_ratio = -1
        return hit_ratio

    def check_hit_miss(self, real_label, calculated_label):
        print('Compare({}\t{})'.format(real_label, calculated_label))
        if real_label == calculated_label:
            self._count_hit += 1
            return True
        else:
            self._count_miss += 1
            return False

    def check_min(self, actual_label, actual_dtw):
        if actual_dtw < self._min_dtw:
            print('NEW MIN: {}\told: {}'.format(actual_label, self._min_label))
            self._min_dtw = actual_dtw
            self._min_label = actual_label
            return True
        print('test min: {}\tnow: {}'.format(actual_label, self._min_label))
        return False

    def run(self):
        # This 'for chain' belhow looks like complexity O(n^3), but actualy it
        # is O(n^2). Two of the 'for' is to access the same data structure (a
        # dictionary), so it dosen't count.

        init_time = time.clock()

        temp = len(self._list_compare)

        # For each series
        for compare_label, compare_serie in self._list_compare[:1]:
            print('{}'.format(temp))
            temp -= 1

            # Reset Values
            self._min_dtw = float('inf')
            self._min_label = float('inf')

            # Iterate all labels
            for base_label, base_series_list in self._dict_base.items():

                # Iterate all series on that label
                for base_serie in base_series_list:
                    actual_dtw = Dtw(base_serie, compare_serie).run()
                    self.check_min(base_label, actual_dtw)

            self.check_hit_miss(compare_label, self._min_label)

        end_time = time.clock()
        self._time_last_run = end_time - init_time
        return self._hit_ratio
