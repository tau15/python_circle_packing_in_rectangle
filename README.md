# Алгоритм упаковки произвольного количества гругов на листы (прямоугольники) заданного габарита

Пример использования:
```python
from IPython.display import SVG, display
import circle_packing

# Задаём диаметру кругов для размщения в формате: { Диаметр : Количество }
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
После заверешения работы алгоритма в объекте CirclePacking создаётся массив из прямоугольников, заданного размера с размещенными на них кругами:
```python
cp.sheets
# [<__main__.Sheet at 0x7f172b67d8e0>,
# <__main__.Sheet at 0x7f172b67d820>,
# <__main__.Sheet at 0x7f172b66cca0>]
```
Круги, не вошедшие на лист (не вошли по габаритам) находятся в атрибуте cp.circles_excluded:
```python
cp.circles_excluded
# {830: 1}
```

Результат работы алгоритма:

![Пример работы алгоритка упаковки кругов на лист](https://github.com/tau15/python_circle_packing_in_rectangle/blob/main/python_circle_packing_in_rectangle_sample.png "Пример работы алгоритка упаковки кругов на лист")

Ссыдка на ноутбук:
https://colab.research.google.com/drive/1e-RoNHStyqdyROZNPHga_vvrIKyRy3ZR?usp=sharing
