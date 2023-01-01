import svgwrite
import math


class Sheet:
    def __init__(self, w, h):
        self.w = w
        self.h = h
        self.circles = []


class Circle:
    def __init__(self, r, cx=None, cy=None):
        self.cx = cx
        self.cy = cy
        self.r = r

    @staticmethod
    def two_circle_intersections(c1, c2):
        x0, y0, r0 = c1.cx, c1.cy, c1.r
        x1, y1, r1 = c2.cx, c2.cy, c2.r
        d = math.sqrt((x1 - x0) ** 2 + (y1 - y0) ** 2)
        if d > r0 + r1:
            return False
        if d < abs(r0 - r1):
            return False
        if d == 0 and r0 == r1:
            return False
        else:
            return True


class CirclePacking:
    def __init__(self, sheet_w, sheet_h, user_circles, welding_w):
        self.sheet_w = sheet_w
        self.sheet_h = sheet_h
        self.user_circles = user_circles
        self.circles = []
        self.sheets = []
        self.circles_excluded = {}
        self.welding_w = welding_w

    def create_circles_sorted(self):
        self.circles = []
        for i in reversed(sorted(self.user_circles.keys())):
            for k in range(self.user_circles[i]):
                self.circles.append(Circle(i))

    # Убираем круги, которые уже размещены
    def clean_circles(self):
        circles_cleaned = []
        for i in self.user_circles.keys():
            for k in range(self.user_circles[i]):
                circles_cleaned.append(Circle(i))
        self.circles = circles_cleaned

    def packing_v2(self):
        self.create_circles_sorted()
        while sum(self.user_circles.values()) > 0:
            # print(self.user_circles, self.circles)
            self.sheets.append(Sheet(self.sheet_w, self.sheet_h))
            current_sheet = self.sheets[-1]
            for i in self.circles:
                i.cx, i.cy = self.find_best_packing_start_point(current_sheet, i)
                if i.cx is None and i.cy is None:
                    if i.r not in self.circles_excluded:
                        self.circles_excluded[i.r] = 1
                    else:
                        self.circles_excluded[i.r] += 1
                    self.user_circles[i.r] -= 1
                else:
                    # Проверка что мы не вышли за длину листа
                    if i.cx > current_sheet.w - i.r - self.welding_w:
                        pass
                    else:
                        self.user_circles[i.r] -= 1
                        current_sheet.circles.append(i)
            self.clean_circles()

    def packing(self):
        self.create_circles_sorted()

        self.sheets.append(Sheet(self.sheet_w, self.sheet_h))
        current_sheet = self.sheets[0]

        for i in self.circles:

            i.cx, i.cy = self.find_best_packing_start_point(current_sheet, i)

            if i.cx is None and i.cy is None:
                if i.r not in self.circles_excluded:
                    self.circles_excluded[i.r] = 1
                else:
                    self.circles_excluded[i.r] += 1
            else:
                # Проверка что мы не вышли за длину листа
                if i.cx > current_sheet.w - i.r - self.welding_w:
                    print("Добавляем следющий лист")
                    self.sheets.append(Sheet(self.sheet_w, self.sheet_h))
                    current_sheet = self.sheets[-1]
                    i.cx, i.cy = self.find_best_packing_start_point(current_sheet, i)
                self.user_circles[i.r] -= 1
                current_sheet.circles.append(i)

    # Ищем наилучшую позицию по вертикали для размещения круга
    def find_best_packing_start_point(self, s, c):
        try_results = {}
        N = 10  # На сколько частей делим высоту для поиска наилучшей позиции по вертикали для текущего круга
        step = int((s.h - c.r) / N)
        # Формируем массив координат по вертикали для попыток
        try_y = [c.r, s.h - c.r, s.h / 2]
        for i in range(int((s.h - c.r) / step)):
            try_y.append(c.r + step * i)
        # Пробуем все координаты из массива попыток
        for i in try_y:
            c.cx = s.w + c.r
            c.cy = i
            self.move_circle(s, c)
            # Проверяем что мы вошли на лист
            if c.cy >= c.r + self.welding_w and c.cy <= s.h - c.r - self.welding_w:
                try_results[c.cx] = c.cy
        if try_results == {}:
            cx = cy = None
        else:
            cx = sorted(try_results.keys())[0]
            cy = try_results[cx]
        return cx, cy

    def move_circle(self, s, c):
        while c.cx > c.r + self.welding_w:
            if self.check_intersections(s, c):
                return
            c.cx -= 1

    def check_intersections(self, s, c):
        for i in s.circles:
            i.r += self.welding_w
            if Circle.two_circle_intersections(i, c):
                i.r -= self.welding_w
                return True
            i.r -= self.welding_w
        return False

    def draw_sheet_with_circles(self, sheet_idx, scale, filename):
        sheet = self.sheets[sheet_idx]
        w = sheet.w * scale
        h = sheet.h * scale
        border_x = 150 * scale
        border_y = 150 * scale
        svg = svgwrite.Drawing(
            filename=filename,
            size=(str(w + border_x * 2) + "px", str(h + border_y * 2) + "px"),
        )
        svg.add(
            svg.line(
                stroke="red",
                start=(str(0 + border_x) + "px", str(0 + border_y) + "px"),
                end=(str(w + border_x) + "px", str(0 + border_y) + "px"),
            )
        )
        svg.add(
            svg.line(
                stroke="red",
                start=(str(0 + border_x) + "px", str(0 + border_y) + "px"),
                end=(str(0 + border_x) + "px", str(h + border_y) + "px"),
            )
        )
        svg.add(
            svg.line(
                stroke="red",
                start=(str(0 + border_x) + "px", str(h + border_y) + "px"),
                end=(str(w + border_x) + "px", str(h + border_y) + "px"),
            )
        )
        line1 = svg.add(
            svg.line(
                stroke="red",
                start=(str(w + border_x) + "px", str(0 + border_y) + "px"),
                end=(str(w + border_x) + "px", str(h + border_y) + "px"),
            )
        )
        line1.dasharray([5, 10])
        for i in sheet.circles:
            cx = i.cx * scale
            cy = i.cy * scale
            r = i.r * scale
            svg.add(
                svg.circle(
                    center=(str(cx + border_x) + "px", str(cy + border_x) + "px"),
                    r=str(r) + "px",
                    stroke="black",
                    fill="white",
                    stroke_width=1,
                )
            )
        svg.save()
