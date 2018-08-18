# FinChart

This module is a chart tool to show time series data based on PyQt5

## Current support series

1.  line
2.  bar
3.  scatter
4.  candle

## Requirements

-   Python >= 3.6
-   PyQt5 >= 5.10
-   PyQtChart >= 5.10

## Install

`clone` and `pip install -e .`

## Quick start

```python
from FinChart import Wizard

# create a chart wizard
wizard = Wizard()
# add a view to draw
view = wizard.addView('demo')
# add a line into this view
view.addLine('demo line', [1, 2], [1, 2])
# show all
wizard.show()
```

> use `arrow` key to adjust view
