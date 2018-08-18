from FinChart import Wizard

# create a chart wizard
wizard = Wizard()
# add a view to draw
view = wizard.addView("demo")
# add a line into this view
view.addLine("demo line", [1, 2], [1, 2])
# show all
wizard.show()
