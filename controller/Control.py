from matplotlib.backend_bases import MouseButton

from model import *

# line list
LineList = []
# default degree
k = 3
type = 1


# if degree has changed so we need redraw line
def change_degree(degree):

    try:
        degree = int(degree)
    except ValueError:
        print("Input Value must can be Integer")
        return

    if degree < 2:
        print("Input Valuse must greate than 2")
        return
    global k
    if degree == k:
        print("Wish input valuse be different as before")
        return
    # change the degree setting
    k = degree
    # if have line
    if len(LineList):
        for line in LineList:
            # update the degree of old line
            line.k = degree
            line.updateline()


def change_type(label):

    global type
    if label == "Uniform":
        type = 0
    else:
        type = 1

    if len(LineList):
        for line in LineList:
            # update the type of old line
            line.type = type
            line.updateline()


class CreatLine(object):

    def __init__(self, axes):
        self.axes = axes

    def createnewline(self, event):
        self.cline, = self.axes.plot([], [])
        self.line = Line(self.cline, k=k, type=type)
        self.line.connect()
        LineList.append(self.line)


class Line(object):

    # only one can be animated at a time
    lock = None

    def __init__(self, line, k=k, type=type):
        self.line = line
        self.axes = line.axes
        # Default settings
        self.k = k
        self.type = type
        # set point and line
        self.cx, self.cy = [], []
        self.bx, self.by = [], []
        self.bspline, = self.axes.plot(self.bx, self.by)
        self.line.set(linestyle=":", marker='p', mfc='r', ms=7, label='Control Point Line')
        self.bspline.set(linestyle="-", color="k", label='B Spline Line')

        # index of the pick point
        self._index = None
        # Controlline hide
        self.pointHide = False
        # blit background
        self.background = None

    def connect(self):
        canvas = self.line.figure.canvas
        self.cidpress = canvas.mpl_connect('button_press_event', self.mouse_press)
        self.cidrelease = canvas.mpl_connect('button_release_event', self.mouse_release)
        self.cidkey = canvas.mpl_connect('key_press_event', self.key_press)
        self.cidmotion = canvas.mpl_connect('motion_notify_event', self.mouse_moves)
        self.canvas = canvas

    def get_point_index(self, event, threshold=0.2):
        if len(self.cx) == 0:
            return
        distance = dict()
        for i in range(len(self.cx)):
            distance[i] = pow((self.cx[i] - event.xdata) ** 2 + (self.cy[i] - event.ydata) ** 2, 0.5)
        # find the index of the min value
        index = min(distance, key=lambda key: distance[key])
        # if this min distance >= threshold:
        if distance[index] >= threshold:
            index = None
        return index

    def mouse_press(self, event):
        if event.inaxes is not self.axes:
            return
        if Line.lock is not None:
            return
        if self.pointHide is True:
            return
        # left button press
        if event.button == MouseButton.LEFT:
            self._index = self.get_point_index(event, threshold=0.25)
            if self._index is None:
                return
            # get the lock of the Line
            Line.lock = self
        elif event.button == MouseButton.RIGHT:
            # add point on the newest line
            if LineList[len(LineList)-1] is not self:
                return
            self._index = self.get_point_index(event, threshold=0.1)
            if self._index is not None:
                return
            Line.lock = self
            # update the control point and line
            self.cx.append(event.xdata)
            self.cy.append(event.ydata)
            self.line.set_data(self.cx, self.cy)

        self.line.set_animated(True)
        self.bspline.set_animated(True)
        self.canvas.draw()
        self.background = self.canvas.copy_from_bbox(self.axes.bbox)
        self.updateline()

    def mouse_moves(self, event):
        if Line.lock is not self:
            return
        if event.inaxes is not self.axes:
            return
        if event.button is not MouseButton.LEFT:
            return
        if self._index is None:
            return
        # update the control point
        self.cx[self._index] = event.xdata
        self.cy[self._index] = event.ydata
        # redraw line
        self.line.set_data(self.cx, self.cy)
        self.updateline()

    def mouse_release(self, event):
        if Line.lock is not self:
            return
        Line.lock = None
        self.background = None
        self.line.set_animated(False)
        self.bspline.set_animated(False)

        # redraw the full figure
        self.canvas.draw()

    def updateline(self):
        bspline = BSpline(self.k)
        self.bx, self.by = bspline.getpoint(self.cx, self.cy, ktype=self.type)

        self.bspline.set_data(self.bx, self.by)
        # redraw the line and bspline
        if self.background:
            self.canvas.restore_region(self.background)
            self.axes.draw_artist(self.line)
            self.axes.draw_artist(self.bspline)
            # blit just the background
            self.canvas.blit(self.axes.bbox)
        # when change k or type:
        else:
            self.bspline.set_data(self.bx, self.by)
            self.axes.figure.canvas.draw()

    def key_press(self, event):
        if event.inaxes is not self.axes:
            return
        if event.key == 'h' or event.key == 'H':
            self.line.set_visible(self.pointHide)
            self.pointHide = not self.pointHide
            self.canvas.draw()

    # disconnect
    def disconnect(self):
        self.canvas.mpl_disconnect(self.cidpress)
        self.canvas.mpl_disconnect(self.cidmotion)
        self.canvas.mpl_disconnect(self.cidrelease)
        self.canvas.mpl_disconnect(self.cidkey)
