import base64
import math
import struct
import zlib

LOGO_SIZE = 256
SMALL_SIZE = 48

GOLD = (255, 215, 0)
DARK_GOLD = (184, 134, 11)
RED = (255, 68, 68)
DARK_RED = (139, 0, 0)
BLUE = (51, 204, 255)
DARK_BLUE = (0, 51, 102)
WHITE = (255, 255, 255)


def make_buffer(width, height):
    return bytearray(width * height * 4)


def set_pixel(buf, width, height, x, y, color, alpha=255):
    if 0 <= x < width and 0 <= y < height:
        index = (y * width + x) * 4
        buf[index] = color[0]
        buf[index + 1] = color[1]
        buf[index + 2] = color[2]
        buf[index + 3] = alpha


def fill_polygon(buf, width, height, points, color):
    y_coords = [p[1] for p in points]
    y_start = int(math.floor(min(y_coords)))
    y_end = int(math.ceil(max(y_coords)))
    point_count = len(points)
    for y in range(y_start, y_end + 1):
        scan_y = y + 0.5
        intersections = []
        for i in range(point_count):
            x1, y1 = points[i]
            x2, y2 = points[(i + 1) % point_count]
            if (y1 <= scan_y < y2) or (y2 <= scan_y < y1):
                t = (scan_y - y1) / (y2 - y1)
                intersections.append(x1 + t * (x2 - x1))
        intersections.sort()
        for k in range(0, len(intersections) - 1, 2):
            x_start = int(math.ceil(intersections[k]))
            x_end = int(math.floor(intersections[k + 1]))
            for x in range(x_start, x_end + 1):
                set_pixel(buf, width, height, x, y, color)


def draw_line(buf, width, height, x1, y1, x2, y2, thickness, color):
    length = math.hypot(x2 - x1, y2 - y1)
    steps = int(length) + 1
    for i in range(steps + 1):
        t = i / steps if steps else 0
        cx = x1 + t * (x2 - x1)
        cy = y1 + t * (y2 - y1)
        for dx in range(-thickness, thickness + 1):
            for dy in range(-thickness, thickness + 1):
                if dx * dx + dy * dy <= thickness * thickness:
                    set_pixel(buf, width, height, int(round(cx + dx)), int(round(cy + dy)), color)


def draw_polyline(buf, width, height, points, thickness, color, closed=False):
    segment_count = len(points) if closed else len(points) - 1
    for i in range(segment_count):
        x1, y1 = points[i]
        x2, y2 = points[(i + 1) % len(points)]
        draw_line(buf, width, height, x1, y1, x2, y2, thickness, color)


def fill_circle(buf, width, height, center_x, center_y, radius, color):
    for y in range(int(center_y - radius) - 1, int(center_y + radius) + 2):
        for x in range(int(center_x - radius) - 1, int(center_x + radius) + 2):
            if (x - center_x) ** 2 + (y - center_y) ** 2 <= radius * radius:
                set_pixel(buf, width, height, x, y, color)


def draw_crown(buf, width, height):
    scale = width / LOGO_SIZE
    cx, cy = width / 2, height / 2

    band = [
        (cx - 60 * scale, cy + 50 * scale),
        (cx + 60 * scale, cy + 50 * scale),
        (cx + 48 * scale, cy + 70 * scale),
        (cx - 48 * scale, cy + 70 * scale),
    ]
    body = [
        (cx - 60 * scale, cy + 50 * scale),
        (cx - 50 * scale, cy - 30 * scale),
        (cx - 25 * scale, cy - 5 * scale),
        (cx, cy - 65 * scale),
        (cx + 25 * scale, cy - 5 * scale),
        (cx + 50 * scale, cy - 30 * scale),
        (cx + 60 * scale, cy + 50 * scale),
    ]
    fill_polygon(buf, width, height, body, GOLD)
    fill_polygon(buf, width, height, band, GOLD)
    outline_thickness = max(1, int(3 * scale))
    draw_polyline(buf, width, height, body, outline_thickness, DARK_GOLD, closed=True)
    draw_polyline(buf, width, height, band, outline_thickness, DARK_GOLD, closed=True)

    jewel_radius = 10 * scale
    jewel_positions = [
        (cx - 50 * scale, cy - 30 * scale),
        (cx, cy - 65 * scale),
        (cx + 50 * scale, cy - 30 * scale),
    ]
    for jx, jy in jewel_positions:
        fill_circle(buf, width, height, jx, jy, jewel_radius, RED)
        draw_circle_outline(buf, width, height, jx, jy, jewel_radius, max(1, int(2 * scale)), DARK_RED)

    cross_x = cx
    cross_y = cy - 65 * scale - 25 * scale
    cross_thick = max(2, int(4 * scale))
    draw_line(buf, width, height, cross_x - 10 * scale, cross_y, cross_x + 10 * scale, cross_y, cross_thick, WHITE)
    draw_line(buf, width, height, cross_x, cross_y - 10 * scale, cross_x, cross_y + 10 * scale, cross_thick, WHITE)

    gem_radius = 7 * scale
    gem_positions = [
        (cx - 32 * scale, cy + 58 * scale),
        (cx, cy + 58 * scale),
        (cx + 32 * scale, cy + 58 * scale),
    ]
    for gx, gy in gem_positions:
        fill_circle(buf, width, height, gx, gy, gem_radius, BLUE)
        draw_circle_outline(buf, width, height, gx, gy, gem_radius, max(1, int(2 * scale)), DARK_BLUE)


def draw_circle_outline(buf, width, height, center_x, center_y, radius, thickness, color):
    for y in range(int(center_y - radius - thickness) - 1, int(center_y + radius + thickness) + 2):
        for x in range(int(center_x - radius - thickness) - 1, int(center_x + radius + thickness) + 2):
            dist = math.hypot(x - center_x, y - center_y)
            if abs(dist - radius) <= thickness:
                set_pixel(buf, width, height, x, y, color)


def encode_png(width, height, rgba_bytes):
    def chunk(chunk_type, data):
        chunk_body = chunk_type + data
        return struct.pack(">I", len(data)) + chunk_body + struct.pack(">I", zlib.crc32(chunk_body) & 0xffffffff)

    signature = b"\x89PNG\r\n\x1a\n"
    ihdr = struct.pack(">IIBBBBB", width, height, 8, 6, 0, 0, 0)
    raw = bytearray()
    for y in range(height):
        raw.append(0)
        raw += rgba_bytes[y * width * 4:(y + 1) * width * 4]
    idat = zlib.compress(bytes(raw), 9)
    return signature + chunk(b"IHDR", ihdr) + chunk(b"IDAT", idat) + chunk(b"IEND", b"")


def encode_ico(png_bytes, width, height):
    header = struct.pack("<HHH", 0, 1, 1)
    entry = struct.pack("<BBBBHHII", width % 256, height % 256, 0, 0, 1, 32, len(png_bytes), 22)
    return header + entry + png_bytes


def downsample(src_buf, src_width, src_height, dest_width, dest_height):
    dest = make_buffer(dest_width, dest_height)
    for y in range(dest_height):
        for x in range(dest_width):
            src_x = int(x * src_width / dest_width)
            src_y = int(y * src_height / dest_height)
            src_index = (src_y * src_width + src_x) * 4
            dest_index = (y * dest_width + x) * 4
            dest[dest_index:dest_index + 4] = src_buf[src_index:src_index + 4]
    return dest


def main():
    big_buf = make_buffer(LOGO_SIZE, LOGO_SIZE)
    draw_crown(big_buf, LOGO_SIZE, LOGO_SIZE)
    big_png = encode_png(LOGO_SIZE, LOGO_SIZE, big_buf)

    small_buf = downsample(big_buf, LOGO_SIZE, LOGO_SIZE, SMALL_SIZE, SMALL_SIZE)
    small_png = encode_png(SMALL_SIZE, SMALL_SIZE, small_buf)

    with open("chess_logo.png", "wb") as f:
        f.write(big_png)
    with open("chess_icon.ico", "wb") as f:
        f.write(encode_ico(big_png, LOGO_SIZE, LOGO_SIZE))

    big_b64 = base64.b64encode(big_png).decode("ascii")
    small_b64 = base64.b64encode(small_png).decode("ascii")

    with open("logo_data.py", "w") as f:
        f.write("LOGO_PNG_BASE64 = \"" + big_b64 + "\"\n")
        f.write("LOGO_SMALL_PNG_BASE64 = \"" + small_b64 + "\"\n")

    print("Generated chess_logo.png, chess_icon.ico, logo_data.py")
    print("logo_data.py size:", len(big_b64) + len(small_b64), "chars")


if __name__ == "__main__":
    main()