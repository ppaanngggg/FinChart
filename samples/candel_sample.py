from datetime import date

from FinChart import Wizard

wizard = Wizard()
view = wizard.addView("candel", _view_stretch=3)
view.addCandle(
    "bar",
    [date(2018, 1, 1), date(2018, 1, 2), date(2018, 1, 3), date(2018, 1, 4)],
    [(1, 2, 0.5, 1.8), (2, 3, 1, 2), (1, 1, 0.5, 0.8), (0.8, 1, 0.8, 0.9)],
)

wizard.show()
