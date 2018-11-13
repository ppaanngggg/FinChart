from datetime import date

from FinChart import Wizard

wizard = Wizard()
view = wizard.addView("candel", _view_stretch=3)
view.addBox(
    "box",
    [date(2018, 1, 1), date(2018, 1, 2), date(2018, 1, 3)],
    [(1, 2, 3, 4, 5), (2, 3, 4, 5, 6), (3, 4, 5, 6, 7)],
)

wizard.show()
