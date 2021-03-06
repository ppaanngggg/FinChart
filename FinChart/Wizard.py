import sys
import typing
from collections import OrderedDict

from PyQt5.QtWidgets import QApplication, QVBoxLayout

from FinChart.View import View
from FinChart.Window import Window


class Wizard:
    ZOOM_STEP = 10.0
    SCROLL_STEP = 10.0

    def __init__(self, _width: int = 1440, _height: int = 720):
        self.view_dict: typing.Dict[str, View] = OrderedDict()

        # map x to axis idx
        self.x2idx: typing.Dict[typing.Any, int] = None
        # map axis idx to x
        self.idx2x: typing.List[typing.Any] = None

        self.begin_idx: int = 0
        self.end_idx: int = 0

        self.app: QApplication = None
        self.window: Window = None
        self.width = _width
        self.height = _height

    def addView(
        self,
        _name: str,
        _view_stretch: int = 1,
        _adaptive=True,
        _chart_stretch: int = 15,
    ) -> View:
        """
        Add a new view. If there are multi-views, they will be
        sorted as you add.

        :param _name: the name of this view
        :param _view_stretch: the stretch compared with other views
        :param _adaptive: adapt y or not
        :param _chart_stretch: the stretch of chart compared with text in this view
        """
        assert _name not in self.view_dict
        assert _view_stretch > 0
        assert _chart_stretch > 0
        self.view_dict[_name] = View(
            _name, self, _adaptive, _view_stretch, _chart_stretch
        )
        return self.view_dict[_name]

    def _calcSetX(self) -> typing.Tuple[dict, list]:
        """
        :return: x2idx and idx2x, because idx is int, then idx2x is list
        """
        # join all x
        tmp = set()
        for d in self.view_dict.values():
            tmp |= d.calcSetX()
        tmp = sorted(tmp)
        # reset x range
        self.begin_idx = 0
        self.end_idx = len(tmp) - 1

        return dict(zip(tmp, range(len(tmp)))), tmp

    def _setAxisX(self, _begin: int, _end: int):
        tmp_begin = _begin - 1
        tmp_end = _end + 1

        for d in self.view_dict.values():
            d.setAxisX(tmp_begin, tmp_end)

    def _setAxisY(self, _begin: int, _end: int):
        for d in self.view_dict.values():
            if d.adaptive:
                d.calcRangeY(self.idx2x[_begin], self.idx2x[_end])
                d.setAxisY(d.begin_y, d.end_y)

    def drawWindow(self):
        if not self.view_dict:
            return

        self.app = QApplication(sys.argv)

        # get the axis info, and reset it
        self.x2idx, self.idx2x = self._calcSetX()
        self._setAxisX(self.begin_idx, self.end_idx)

        layout = QVBoxLayout()
        # keep the sort when inserted
        for d in self.view_dict.values():
            layout.addLayout(d.createChartView(self.x2idx, self.idx2x), d.view_stretch)

        self.window = Window(self)
        self.window.resize(self.width, self.height)
        self.window.setLayout(layout)

    def show(self):
        """
        show the whole chart you draw
        """
        self.drawWindow()
        self.window.show()

        return self.app.exec()

    def save(self, _filename: str):
        """
        save the whole chart as pic

        :param _filename: path to save the pic
        """
        self.drawWindow()
        self.window.grab().save(_filename)

    def zoomIn(self):
        diff = max(int((self.end_idx - self.begin_idx) / 2.0 / self.ZOOM_STEP), 1)
        if self.end_idx - self.begin_idx > 2 * diff:
            self.begin_idx += diff
            self.end_idx -= diff

        self._setAxisX(self.begin_idx, self.end_idx)
        self._setAxisY(self.begin_idx, self.end_idx)

    def zoomOut(self):
        diff = max(int((self.end_idx - self.begin_idx) / 2.0 / self.ZOOM_STEP), 1)
        self.begin_idx = max(self.begin_idx - diff, 0)
        self.end_idx = min(self.end_idx + diff, len(self.idx2x) - 1)

        self._setAxisX(self.begin_idx, self.end_idx)
        self._setAxisY(self.begin_idx, self.end_idx)

    def scrollLeft(self):
        diff = max(int((self.end_idx - self.begin_idx) / self.SCROLL_STEP), 1)
        self.begin_idx -= diff
        self.begin_idx = max(self.begin_idx, 0)
        self.end_idx -= diff
        self.end_idx = max(self.end_idx, 0)

        self._setAxisX(self.begin_idx, self.end_idx)
        self._setAxisY(self.begin_idx, self.end_idx)

    def scrollRight(self):
        diff = max(int((self.end_idx - self.begin_idx) / self.SCROLL_STEP), 1)
        self.begin_idx += diff
        self.begin_idx = min(self.begin_idx, len(self.idx2x) - 1)
        self.end_idx += diff
        self.end_idx = min(self.end_idx, len(self.idx2x) - 1)

        self._setAxisX(self.begin_idx, self.end_idx)
        self._setAxisY(self.begin_idx, self.end_idx)

    def mouseMove(self, _index):
        _index = max(0, _index)
        _index = min(len(self.idx2x) - 1, _index)
        x = self.idx2x[_index]
        self.window.setWindowTitle(str(x))
        for d in self.view_dict.values():
            d.updateValue(x)
