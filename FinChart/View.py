import typing

from PyQt5.Qt import QMouseEvent, QPainter
from PyQt5.QtChart import QChart, QChartView, QValueAxis
from PyQt5.QtWidgets import QHBoxLayout, QFormLayout

from FinChart.BarSeries import BarSeries
from FinChart.CandleSeries import CandleSeries
from FinChart.LineSeries import LineSeries
from FinChart.ScatterSeries import ScatterSeries
from FinChart.SeriesAbstract import SeriesAbstract


class ChartView(QChartView):
    def __init__(self, _chart: QChart, _wizard):
        super().__init__(_chart)
        self.wizard = _wizard

    def mouseMoveEvent(self, _event: QMouseEvent):
        point = self.chart().mapToValue(_event.pos())
        index = round(point.x())
        self.wizard.mouseMove(index)


class View:
    def __init__(
        self,
        _name: str,
        _wizard,
        _adaptive: bool,
        _view_stretch: int,
        _chart_stretch: int,
    ):
        self.name = _name
        self.wizard = _wizard
        self.adaptive = _adaptive
        self.view_stretch = _view_stretch
        self.chart_stretch = _chart_stretch

        self.series_table: typing.Dict[str, SeriesAbstract] = {}

        # show x will slow down chart
        self.axis_x = QValueAxis()
        self.axis_x.setVisible(False)

        # set name to axis_y, price for price, volume for volume, etc
        self.axis_y = QValueAxis()
        self.axis_y.setTitleText(self.name)

        # for adaptive
        self.begin_y: float = None
        self.end_y: float = None

    def addBar(
        self,
        _name: str,
        _x_list: typing.Sequence,
        _y_list: typing.Sequence,
        _color: typing.Any = None,
        _show_value: bool = False,
    ):
        assert _name not in self.series_table
        self.series_table[_name] = BarSeries(
            _name, _x_list, _y_list, _color, _show_value
        )

    def addLine(
        self,
        _name: str,
        _x_list: typing.Sequence,
        _y_list: typing.Sequence,
        _color: typing.Any = None,
        _show_value: bool = False,
    ):
        """
        add line to view

        :param _name: str
        :param _x_list: List or any sequence
        :param _y_list: List or any sequence
        :param _color: 'red' or (255, 255, 255)
        :param _show_value: show value or not
        :return:
        """
        assert _name not in self.series_table
        self.series_table[_name] = LineSeries(
            _name, _x_list, _y_list, _color, _show_value
        )

    def addScatter(
        self,
        _name: str,
        _x_list: typing.Sequence,
        _y_list: typing.Sequence,
        _color: typing.Any = None,
        _show_value: bool = False,
    ):
        assert _name not in self.series_table
        self.series_table[_name] = ScatterSeries(
            _name, _x_list, _y_list, _color, _show_value
        )

    def addCandle(
        self,
        _name: str,
        _x_list: typing.Sequence,
        _y_list: typing.Sequence[typing.Sequence],
        _inc_color: typing.Any = None,
        _dec_color: typing.Any = None,
        _show_value: bool = False,
    ):
        assert _name not in self.series_table
        self.series_table[_name] = CandleSeries(
            _name, _x_list, _y_list, _inc_color, _dec_color, _show_value
        )

    def calcSetX(self) -> typing.Set:
        """
        get the set of x, to get x range for wizard

        :return: the set of all x value
        """
        tmp = set()
        for v in self.series_table.values():
            tmp |= set(v.calcSetX())
        return tmp

    def calcRangeY(self, _begin_x=None, _end_x=None):
        """
        get range of y for this view

        :return: (min, max)
        """
        tmp_min_list = []
        tmp_max_list = []
        for v in self.series_table.values():
            min_y, max_y = v.calcRangeY(_begin_x, _end_x)
            if min_y is not None and max_y is not None:
                tmp_min_list.append(min_y)
                tmp_max_list.append(max_y)

        if tmp_min_list:
            self.begin_y = min(tmp_min_list)
        if tmp_max_list:
            self.end_y = max(tmp_max_list)

    def setAxisX(self, _begin: float, _end: float):
        self.axis_x.setRange(_begin, _end)

    def setAxisY(self, _begin: float, _end: float):
        self.axis_y.setRange(_begin, _end)

    def createChartView(self, _x2idx: dict, _idx2x: list) -> QHBoxLayout:
        chart = QChart()

        # assign y range
        self.calcRangeY()
        self.setAxisY(self.begin_y, self.end_y)

        value_layout = QFormLayout()
        # add each series
        for v in self.series_table.values():
            v.addSeries(_x2idx, _idx2x, chart, self.axis_x, self.axis_y)
            if v.show_value:
                value_layout.addWidget(v.show_group)

        # create chartview and layout for view and value
        chartview = ChartView(chart, self.wizard)
        chartview.setRenderHint(QPainter.Antialiasing)

        global_layout = QHBoxLayout()
        global_layout.addWidget(chartview, self.chart_stretch)
        global_layout.addLayout(value_layout)

        return global_layout

    def updateValue(self, _x):
        for v in self.series_table.values():
            if v.show_value:
                v.updateValue(_x)
