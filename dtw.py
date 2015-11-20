# -*- coding: utf-8 -*-
from pprint import pprint
from math import sqrt, ceil


class Dtw(object):

    def __init__(self, base_serie, compare_serie):
        self._matrix_distance = {}
        self._matrix_dtw = {(-1, -1): 0.0}
        self._base_serie = base_serie
        self._compare_serie = compare_serie

    def distance(self, p, q):
        dist = self._matrix_distance.get((p, q))
        if not dist:
            dist = abs(
                float(self._base_serie[p]) -
                float(self._compare_serie[q]))
            self._matrix_distance[(p, q)] = dist
        return dist

    def dtw(self, base, compare):
        recovery = self._matrix_dtw.get((base, compare))
        if recovery is not None:
            return recovery

        if base == -1 or compare == -1:
            self._matrix_dtw[(base, compare)] = float('inf')
            return float('inf')

        dtw_south = self.dtw(base - 1, compare)
        dtw_west = self.dtw(base, compare - 1)
        dtw_southwest = self.dtw(base - 1, compare - 1)
        dtw_min = min(dtw_south, dtw_west, dtw_southwest)

        result = self.distance(base, compare) + dtw_min
        self._matrix_dtw[(base, compare)] = result

        return result

    def run(self):
        return self.dtw(
            len(self._base_serie) - 1, len(self._compare_serie) - 1)

