import random

from FinChart import Wizard

wizard = Wizard()
view = wizard.addView("line", _view_stretch=3)
view.addLine(
    "line",
    [i for i in range(100)],
    [random.random() for _ in range(100)],
    _color="red",
    _show_value=True,
)
view.addLine(
    "line_2",
    [i for i in range(50)],
    [random.random() * 2 for _ in range(50)],
    _show_value=True,
)

view_2 = wizard.addView("line_2", _view_stretch=1, _adaptive=False)
view_2.addLine("line_3", [i for i in range(100)], [i for i in range(100)])

wizard.show()
