import typing

from PyQt5.QtChart import QChart, QValueAxis, QBoxPlotSeries, QBoxSet
from PyQt5.QtWidgets import QGroupBox, QLineEdit, QFormLayout, QLabel

from FinChart.SeriesAbstract import SeriesAbstract


class BoxSeries(SeriesAbstract):
    def __init__(
        self,
        _name: str,
        _x_list: typing.Sequence,
        _y_list: typing.Sequence,
        _color: typing.Any = None,
        _show_value: bool = True,
    ):
        y_list = [sorted(d) for d in _y_list]
        super().__init__(_name, _x_list, y_list, _color, _show_value)

        self.show_le_edit: QLineEdit = None
        self.show_lq_edit: QLineEdit = None
        self.show_m_edit: QLineEdit = None
        self.show_uq_edit: QLineEdit = None
        self.show_ue_edit: QLineEdit = None

        self.type = SeriesAbstract.BOX

    def calcRangeY(self, _begin_x=None, _end_x=None) -> typing.Tuple:
        tmp_y = self.y_list[self._find_begin_idx(_begin_x) : self._find_end_idx(_end_x)]
        min_value = min([min(d) for d in tmp_y])
        max_value = max([max(d) for d in tmp_y])
        return min_value, max_value

    def addSeries(
        self,
        _x2idx: typing.Dict,
        _idx2x: list,
        _chart: QChart,
        _axis_x: QValueAxis,
        _axis_y: QValueAxis,
    ):
        series = QBoxPlotSeries()
        series.setName(self.name)
        if self.color is not None:
            series.setBrush(self.color)

        tmp_dict = dict(zip(self.x_list, self.y_list))
        for k in _idx2x:
            try:
                series.append(QBoxSet(*tmp_dict[k]))
            except KeyError:
                series.append(QBoxSet())

        _chart.addSeries(series)
        _chart.setAxisX(_axis_x, series)
        _chart.setAxisY(_axis_y, series)

        if self.show_value:
            self.createShow()

    def createShow(self):
        self.show_group = QGroupBox()
        self.show_group.setTitle(self.name)

        self.show_le_edit = QLineEdit()
        self.show_le_edit.setDisabled(True)
        self.show_lq_edit = QLineEdit()
        self.show_lq_edit.setDisabled(True)
        self.show_m_edit = QLineEdit()
        self.show_m_edit.setDisabled(True)
        self.show_uq_edit = QLineEdit()
        self.show_uq_edit.setDisabled(True)
        self.show_ue_edit = QLineEdit()
        self.show_ue_edit.setDisabled(True)
        layout = QFormLayout()
        layout.addWidget(QLabel("le"))
        layout.addWidget(self.show_le_edit)
        layout.addWidget(QLabel("lq"))
        layout.addWidget(self.show_lq_edit)
        layout.addWidget(QLabel("m"))
        layout.addWidget(self.show_m_edit)
        layout.addWidget(QLabel("uq"))
        layout.addWidget(self.show_uq_edit)
        layout.addWidget(QLabel("ue"))
        layout.addWidget(self.show_ue_edit)
        self.show_group.setLayout(layout)

    def updateValue(self, _x):
        idx = self._find_idx(_x)
        if idx is None:
            self.show_le_edit.setText("")
            self.show_lq_edit.setText("")
            self.show_m_edit.setText("")
            self.show_uq_edit.setText("")
            self.show_ue_edit.setText("")
        else:
            value = self.y_list[idx]
            self.show_le_edit.setText("{:.5f}".format(value[0]))
            self.show_lq_edit.setText("{:.5f}".format(value[1]))
            self.show_m_edit.setText("{:.5f}".format(value[2]))
            self.show_uq_edit.setText("{:.5f}".format(value[3]))
            self.show_ue_edit.setText("{:.5f}".format(value[4]))
