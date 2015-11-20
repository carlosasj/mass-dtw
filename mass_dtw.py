# -*- coding: utf-8 -*-
import time
from dtw import Dtw
from math import sqrt


def distance_1d(a, b):
    return abs(float(a[0]) - float(b[0]))


def distance_nd(a, b):
    temp = 0
    for i in range(1, len(a)):
        temp += (a[i] - b[i])**2
    return sqrt(temp)


def gen_list_serie(file_serie, dimension=1):
    list_serie = []
    for line in file_serie.split('\n'):
        try:
            label, serie = line.split(' ', 1)
            list_serie.append([label, list(zip(*[iter(serie.split(' '))] * dimension))])
        except:
            pass
    return list_serie


class MassDtw(object):
    def __init__(self,
                 file_base,
                 file_compare,
                 sc_band=100,
                 file_label=None,
                 dimension=1):

        # Flag Sakoe‐Chiba band
        self._sc_band = int(sc_band) / 100

        if dimension is 1:
            self._func_distance = distance_1d
        else:
            self._func_distance = distance_nd

        # Dictionaries and lists, generated
        self._dict_label = dict(gen_list_serie(file_label))
        self._list_base = gen_list_serie(file_base, dimension)
        self._list_compare = gen_list_serie(file_compare, dimension)

        # Minimum dtw value until now. It's two temporary variables for
        # internal use only. Please, avoid change this outside `.run()`
        self._min_dtw = self._min_label = float('inf')

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
            hit_ratio = \
                (100 * self._count_hit) / (self._count_hit + self._count_miss)
        except ZeroDivisionError:
            hit_ratio = -1
        return hit_ratio

    @property
    def get_time_last_run(self):
        return self._time_last_run

    def check_hit_miss(self, real_label, calculated_label):
        print('Compare({}\t{})'.format(real_label, calculated_label))
        if real_label == calculated_label:
            self._count_hit += 1
        else:
            self._count_miss += 1

    def check_min(self, actual_label, actual_dtw):
        if actual_dtw < self._min_dtw:
            self._min_dtw = actual_dtw
            self._min_label = actual_label

    def run(self):
        init_time = time.clock()

        temp = len(self._list_compare)

        # For each series
        for compare_label, compare_serie in self._list_compare:
            print('{}'.format(temp))
            temp -= 1

            # Reset Values
            self._min_dtw = self._min_label = float('inf')

            # Iterate all labels
            for base_label, base_serie in self._list_base:
                actual_dtw = Dtw(base_serie,
                                 compare_serie,
                                 self._func_distance,
                                 self._sc_band).run()
                self.check_min(base_label, actual_dtw)

            self.check_hit_miss(compare_label, self._min_label)

        end_time = time.clock()
        self._time_last_run = end_time - init_time
        return self._hit_ratio
