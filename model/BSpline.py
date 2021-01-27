import numpy as np


class BSpline(object):

    def __init__(self, k=3):
        # k is curves order
        self.k = k

    def getpoint(self, cx, cy, ktype=1):
        self.cx = cx
        self.cy = cy
        self.n = len(cx)
        if self.n < self.k:
            return [], []
        # knots.length = n + k
        self.knots = list(range(self.n + self.k))
        # Uniform type
        if ktype:
            self.knots = np.linspace(0, 1, num=len(self.knots)).tolist()
        # Clamped type
        else:
            self.knots[:self.k - 1] = [0] * (self.k - 1)
            self.knots[len(self.knots) - self.k + 1:] = [1] * (self.k - 1)
            self.knots[self.k - 1:len(self.knots) - self.k + 1] = np.linspace(0, 1, num=self.n - self.k + 2).tolist()
        # de Boor
        return self.bspline_point()

    def bspline_point(self):
        k = self.k
        knot = self.knots
        cx = self.cx
        cy = self.cy

        def deboor_x(r, j, u):
            if r == 0:
                return cx[j]
            if abs(knot[j + k - r] -knot[j]) < 1e-5:
                alpha = 0
            else:
                alpha = (u - knot[j]) / (knot[j + k - r] - knot[j])
            return alpha * deboor_x(r-1, j, u) + (1 - alpha) * deboor_x(r-1, j-1, u)

        def deboor_y(r, j, u):
            if r == 0:
                return cy[j]
            if abs(knot[j + k - r] - knot[j]) < 1e-5:
                alpha = 0
            else:
                alpha = (u - knot[j]) / (knot[j + k - r] - knot[j])
            return alpha * deboor_y(r-1, j, u) + (1 - alpha) * deboor_y(r-1, j-1, u)

        bx, by = [], []
        for j in range(self.k - 1, self.n):
            for u in np.linspace(self.knots[j], self.knots[j+1], num=50):
                bx.append(deboor_x(self.k-1, j, u))
                by.append(deboor_y(self.k-1, j, u))

        return bx, by
