# -*- coding: utf-8 -*-


class Dtw(object):
    matrix_distance = {}

    def __init__(self, base_serie, compare_serie):
        self._base_serie = base_serie
        self._compare_serie = compare_serie
        self._matrix_dtw = {(-1, -1): 0.0}

    def distance(self, p, q):
        # dist = self.matrix_distance.get(
        #     (p, q),
        #     self.matrix_distance.get((q, p))
        # )
        dist = self.matrix_distance.get((p, q))
        if not dist:
            dist = abs(
                float(self._base_serie[p]) - float(self._compare_serie[q]))
            self.matrix_distance[(p, q)] = dist
        return dist

    def dtw(self, base, compare):
        recovery = self._matrix_dtw.get((base, compare))
        if recovery is not None:
            return recovery

        if base < 0 or compare < 0:
            self._matrix_dtw[(base, compare)] = float('inf')
            return float('inf')

        dtw_south = self.dtw(base - 1, compare)
        dtw_southwest = self.dtw(base - 1, compare - 1)
        dtw_west = self.dtw(base, compare - 1)
        dtw_min = min(dtw_south, dtw_southwest, dtw_west)

        self._matrix_dtw[(base, compare)] = self.distance(base, compare) + \
            dtw_min

        return self._matrix_dtw[(base, compare)]

    def run(self):
        return self.dtw(
            len(self._base_serie) - 1,
            len(self._compare_serie) - 1)
