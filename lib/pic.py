import random


class Picture:
    @staticmethod
    def horizontal_dust(pixels, size, factor):
        w, h = size
        for y in range(h):
            for x in range(w):
                r, g, b = pixels[x, y]
                pos = random.randint(0, factor)
                if x + pos < w:
                    pixels[x, y] = pixels[x + pos, y]
                    pixels[x + pos, y] = r, g, b
        return pixels

    @staticmethod
    def vertical_dust(pixels, size, factor):
        w, h = size
        for x in range(w):
            for y in range(h):
                r, g, b = pixels[x, y]
                pos = random.randint(0, factor)
                if y + pos < h:
                    pixels[x, y] = pixels[x, y + pos]
                    pixels[x, y + pos] = r, g, b
        return pixels

    @staticmethod
    def bound(pixels, size):
        w, h = size
        for x in range(w):
            for y in range(h):
                if 0 < x < w - 1 and 0 < y < h - 1:
                    r, g, b = pixels[x, y]
                    rb, gb, bb = pixels[x, y - 1]
                    xrb, xgb, xbb = pixels[x - 1, y]
                    if abs(rb - r) > 40 or abs(gb - g) > 40 or abs(bb - b) > 40:
                        pixels[x, y - 1] = r + 16, g + 16, b + 16
                        pixels[x, y] = r + 39, g + 39, b + 39
                        pixels[x, y + 1] = r + 16, g + 16, b + 16
                    if abs(xrb - r) > 40 or abs(xgb - g) > 40 or abs(xbb - b) > 40:
                        pixels[x - 1, y] = r + 16, g + 16, b + 16
                        pixels[x, y] = r + 39, g + 39, b + 39
                        pixels[x + 1, y] = r + 16, g + 16, b + 16
        return pixels

    @staticmethod
    def curve(pixels, size):
        w, h = size
        for x in range(w):
            for y in range(h):
                r, g, b = pixels[x, y]
                brightness = r + g + b if r + g + b > 0 else 1
                if brightness < 100:
                    k = 100 / brightness
                    pixels[x, y] = \
                        min(255, int(r * k ** 2)), \
                        min(255, int(g * k ** 2)), \
                        min(255, int(b * k ** 2))
        return pixels

    @staticmethod
    def negative(pixels, size):
        w, h = size
        for x in range(w):
            for y in range(h):
                r, g, b = pixels[x, y]
                pixels[x, y] = 255 - r, 255 - g, 255 - b
        return pixels

    @staticmethod
    def change_colors(pixels, size):
        w, h = size
        for x in range(w):
            for y in range(h):
                r, g, b = pixels[x, y]
                pixels[x, y] = g, r, b
        return pixels

    @staticmethod
    def black_and_gray(pixels, size):
        w, h = size
        for x in range(w):
            for y in range(h):
                r, g, b = pixels[x, y]
                bw = (r + g + b) // 3
                pixels[x, y] = bw, bw, bw
        return pixels

    @staticmethod
    def glitch(pixels, size):
        w, h = size
        for x in range(w):
            for y in range(h):
                if 0 < x < w - 1 and 0 < y < h - 1:
                    xr, xg, xb = pixels[x, y]
                    xrn, xgn, xbn = pixels[x + 1, y]
                    yr, yg, yb = pixels[x, y + 1]
                    xyrn, xygn, xybn = pixels[x + 1, y + 1]
                    if abs(xr - xrn) > 5 or abs(xg - xgn) > 5 or abs(xb - xbn) > 5:
                        xr -= 20
                        xg -= xr
                        xb += xg
                        pixels[x, y] = xr, xb, xg
                    if abs(yr - xyrn) > 5 or abs(yg - xygn) > 5 or abs(yb - xybn) > 5:
                        yr -= 20
                        yg -= yr
                        yb += yg
                        pixels[x, y] = yr, yb, yg
                    if abs(yr - xr) > 5 or abs(yg - xg) > 5 or abs(yb - xb) > 5:
                        yr -= xb
                        yg -= xg
                        yb += yg
                        pixels[x, y] = yr, yb, yg
                    if abs(xr - xyrn) > 5 or abs(xg - xygn) > 5 or abs(xb - xybn) > 5:
                        xr += xg
                        xg -= xb
                        xb *= xygn
                        pixels[x, y] = xb, xg, xr
        return pixels

    @staticmethod
    def pixelize(pixels, size, factor):
        ri = 0
        w, h = size
        for x in range(w):
            for y in range(h):
                if 0 < x + factor < w - 1 and 0 < y + factor < h - 1:
                    if y % factor:
                        if not y % 2:
                            ri = -random.randint(0, w - 2 - x)
                        else:
                            ri = random.randint(0, w - 2 - x)
                    if x % factor:
                        if x % 2:
                            pixels[x, y] = pixels[x + factor, y + factor]
                        elif x % 3:
                            pixels[x + ri, y] = pixels[x + factor, y]
                        elif x % 5:
                            pixels[x + ri, y] = pixels[x, y + factor]
                        elif x % 7:
                            pixels[x, y] = pixels[x, y - factor]
                        elif x % 11:
                            pixels[x + ri, y] = pixels[x - factor, y]
                        elif x % 13:
                            pixels[x, y] = pixels[x - factor, y - factor]
                        elif x % 17:
                            pixels[x, y] = pixels[x - factor, y + factor]
                        elif x % 19:
                            pixels[x + ri, y] = pixels[x + factor, y - factor]
        return pixels