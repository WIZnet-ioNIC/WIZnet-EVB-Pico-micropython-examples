# ssd1306_test.py
from machine import Pin, I2C
import ssd1306
import math
import time


class OLED_Display:
    def __init__(self):
        # I²C 설정 (SCL = Pin 17, SDA = Pin 16)
        # self.i2c = I2C(0, scl=Pin(17), sda=Pin(16), freq=400000)
        self.i2c = I2C(0, scl=Pin(9), sda=Pin(8), freq=400000)
        devices = self.i2c.scan()

        if devices:
            for device in devices:
                print("I2C device found at address:", hex(device))
        else:
            print("No I2C device found")

        # SSD1306 OLED 디스플레이 초기화
        self.oled = ssd1306.SSD1306_I2C(128, 64, self.i2c)
        self.x = 0
        self.y = 0

    # 텍스트 출력 및 위치 업데이트 함수
    def print_oled(self, text):
        max_width = 128
        line_height = 10

        self.oled.text(text, self.x, self.y)
        self.oled.show()

        # 다음 줄 좌표 계산
        self.y += line_height
        if self.y >= 64:
            self.y = 0  # 화면 아래로 벗어나면 다시 위로

    # 사각형 그리기 함수
    def draw_rectangle(self, show_delay=0):
        pixel_count = 0
        for x in range(10, 60):
            self.oled.pixel(x, 10, 1)
            self.oled.pixel(x, 40, 1)
            pixel_count += 1
            if show_delay > 0 and pixel_count >= 5:
                self.oled.show()
                time.sleep_us(show_delay)
                pixel_count = 0
        for y in range(10, 41):
            self.oled.pixel(10, y, 1)
            self.oled.pixel(59, y, 1)
            pixel_count += 1
            if show_delay > 0 and pixel_count >= 5:
                self.oled.show()
                time.sleep_us(show_delay)
                pixel_count = 0

    # 채워진 사각형 그리기 함수
    def draw_filled_rectangle(self, show_delay=0):
        pixel_count = 0
        for x in range(70, 110):
            for y in range(10, 30):
                self.oled.pixel(x, y, 1)
                pixel_count += 1
            if show_delay > 0 and pixel_count >= 5:
                self.oled.show()
                time.sleep_us(show_delay)
                pixel_count = 0

    # 수평선 그리기 함수
    def draw_horizontal_line(self, show_delay=0):
        pixel_count = 0
        for x in range(0, 128):
            self.oled.pixel(x, 50, 1)
            pixel_count += 1
            if show_delay > 0 and pixel_count >= 5:
                self.oled.show()
                time.sleep_us(show_delay)
                pixel_count = 0

    # 수직선 그리기 함수
    def draw_vertical_line(self, show_delay=0):
        pixel_count = 0
        for y in range(0, 64):
            self.oled.pixel(64, y, 1)
            pixel_count += 1
            if show_delay > 0 and pixel_count >= 5:
                self.oled.show()
                time.sleep_us(show_delay)
                pixel_count = 0

    # 원 그리기 함수
    def draw_circle(self, show_delay=0):
        pixel_count = 0
        center_x, center_y, radius = 96, 48, 10
        for angle in range(0, 360, 5):  # 5도씩 증가하며 점을 찍음
            rad = math.radians(angle)
            x = int(center_x + radius * math.cos(rad))
            y = int(center_y + radius * math.sin(rad))
            self.oled.pixel(x, y, 1)
            pixel_count += 1
            if show_delay > 0 and pixel_count >= 5:
                self.oled.show()
                time.sleep_us(show_delay)
                pixel_count = 0

    # 삼각형 그리기 함수
    def draw_triangle(self, show_delay=0):
        pixel_count = 0
        for x in range(10, 61):
            self.oled.pixel(x, 40, 1)
            pixel_count += 1
            if show_delay > 0 and pixel_count >= 5:
                self.oled.show()
                time.sleep_us(show_delay)
                pixel_count = 0  # 밑변
        for i in range(0, 26):
            self.oled.pixel(10 + i, 40 - i, 1)
            pixel_count += 1
            if show_delay > 0 and pixel_count >= 5:
                self.oled.show()
                time.sleep_us(show_delay)
                pixel_count = 0  # 왼쪽 변
            self.oled.pixel(60 - i, 40 - i, 1)
            pixel_count += 1
            if show_delay > 0 and pixel_count >= 5:
                self.oled.show()
                time.sleep_us(show_delay)
                pixel_count = 0  # 오른쪽 변

    # 육각형 그리기 함수
    def draw_hexagon(self, show_delay=0):
        pixel_count = 0
        hex_center_x, hex_center_y, hex_radius = 80, 50, 10
        hex_points = []
        for angle in range(0, 360, 60):  # 60도마다 점을 찍어 육각형 꼭짓점 계산
            rad = math.radians(angle)
            x = int(hex_center_x + hex_radius * math.cos(rad))
            y = int(hex_center_y + hex_radius * math.sin(rad))
            hex_points.append((x, y))

        # 육각형의 선을 잇기
        for i in range(len(hex_points)):
            x1, y1 = hex_points[i]
            x2, y2 = hex_points[(i + 1) % len(hex_points)]
            for t in range(0, 101):
                xt = x1 + (x2 - x1) * t // 100
                yt = y1 + (y2 - y1) * t // 100
                self.oled.pixel(xt, yt, 1)
                pixel_count += 1
            if show_delay > 0 and pixel_count >= 5:
                self.oled.show()
                time.sleep_us(show_delay)
                pixel_count = 0

    # 도형 그리기 호출 함수
    def draw_shape(self, shape, show_delay=0):
        draw_functions = {
            "rectangle": self.draw_rectangle,
            "filled_rectangle": self.draw_filled_rectangle,
            "horizontal_line": self.draw_horizontal_line,
            "vertical_line": self.draw_vertical_line,
            "circle": self.draw_circle,
            "triangle": self.draw_triangle,
            "hexagon": self.draw_hexagon,
        }

        if shape in draw_functions:
            draw_functions[shape](show_delay)
        else:
            print(f"Unknown shape: {shape}")

    # 기존의 draw_shapes 함수 업데이트
    def draw_shapes(self, show_delay=0):
        self.oled.fill(0)
        shapes = [
            "rectangle",
            "filled_rectangle",
            "horizontal_line",
            "vertical_line",
            "circle",
            "triangle",
            "hexagon",
        ]
        for shape in shapes:
            self.draw_shape(shape, show_delay)
        self.oled.show()


def main():
    # SSD1306 OLED 디스플레이 인스턴스 생성
    display = OLED_Display()

    # 텍스트 출력
    display.print_oled("Hello, World!")
    time.sleep(1)
    display.print_oled("Hi, guys")
    time.sleep(1)

    # 그림 그리기 함수 호출
    # display.draw_shapes(show_delay=1000000)
    display.draw_shapes()


if __name__ == "__main__":
    main()
