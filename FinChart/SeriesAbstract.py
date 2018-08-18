import typing
from bisect import bisect_right, bisect_left
from collections import namedtuple

from PyQt5.Qt import QColor
from PyQt5.QtChart import QChart, QValueAxis
from PyQt5.QtWidgets import QGroupBox, QLineEdit, QFormLayout

DataTuple = namedtuple("DataTuple", ["x", "y"])


class SeriesAbstract:
    BAR = "bar"
    LINE = "line"
    SCATTER = "scatter"
    CANDLE = "candle"

    def __init__(
        self,
        _name: str,
        _x_list: typing.Sequence,
        _y_list: typing.Sequence,
        _color: typing.Any = None,
        _show_value: bool = True,
    ):
        assert len(_x_list) == len(_y_list)
        assert len(_x_list) > 0

        self.name = _name
        self.x_list = _x_list
        self.y_list = _y_list
        self.show_value = _show_value
        self.show_group: QGroupBox = None
        self.show_edit: QLineEdit = None

        self.color = None if _color is None else QColor(_color)

    def _find_begin_idx(self, _x):
        if _x is None:
            return _x

        i = bisect_left(self.x_list, _x)
        if i != len(self.x_list):
            return i
        else:
            return i - 1

    def _find_end_idx(self, _x):
        if _x is None:
            return _x

        return bisect_right(self.x_list, _x)

    def _find_idx(self, _x):
        i = bisect_left(self.x_list, _x)
        if i != len(self.x_list) and self.x_list[i] == _x:
            return i
        else:
            return None

    def calcSetX(self) -> typing.Set:
        return set(self.x_list)

    def calcRangeY(self, _begin_x=None, _end_x=None) -> typing.Tuple:
        tmp_y = self.y_list[self._find_begin_idx(_begin_x) : self._find_end_idx(_end_x)]
        if len(tmp_y) == 0:
            return None, None
        return min(tmp_y), max(tmp_y)

    def addSeries(
        self,
        _x2idx: typing.Dict,
        _idx2x: typing.List,
        _chart: QChart,
        _axis_x: QValueAxis,
        _axis_y: QValueAxis,
    ):
        raise NotImplementedError("implement addSeries plz")

    def createShow(self):
        self.show_group = QGroupBox()
        self.show_group.setTitle(self.name)
        self.show_edit = QLineEdit()
        self.show_edit.setDisabled(True)
        layout = QFormLayout()
        layout.addWidget(self.show_edit)
        self.show_group.setLayout(layout)

    def updateValue(self, _x):
        idx = self._find_idx(_x)
        if idx is None:
            self.show_edit.setText("")
        else:
            self.show_edit.setText("{:.5f}".format(self.y_list[idx]))
