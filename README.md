# Алгоритм упаковки произвольного количества гругов на листы (прямоугольники) заданного габарита

Пример использования:
```python
from IPython.display import SVG, display
import circle_packing

circles = {
    730 : 1,
    490 : 2,
    360 : 3,
    280 : 5,
    150 : 7,
    100 : 12,
    50 : 24,
}

cp = circle_packing.CirclePacking(sheet_w=6000, sheet_h=1500, circles=circles, cut_border=20)
cp.packing()
```

Результат работы алгоритма:

![Пример работы алгоритка упаковки кругов на лист](https://github.com/tau15/python_circle_packing_in_rectangle/blob/main/python_circle_packing_in_rectangle.png "Пример работы алгоритка упаковки кругов на лист")

Ссыдка на ноутбук:
https://colab.research.google.com/drive/1e-RoNHStyqdyROZNPHga_vvrIKyRy3ZR?usp=sharing
