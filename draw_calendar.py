from PIL import Image, ImageDraw, ImageFont
import textwrap
import calendar
import datetime

WIDTH = 250
HEIGHT = 122

from PIL import Image, ImageDraw, ImageFont
import calendar
from datetime import datetime
import os

WIDTH = 250
HEIGHT = 122

from PIL import Image, ImageDraw, ImageFont
import calendar
from datetime import datetime
import os

WIDTH = 250
HEIGHT = 122

def draw_calendar(current_date, events, save_path):
    # --- Create image ---
    img = Image.new("1", (WIDTH, HEIGHT), 1)  # 1-bit B/W, white background
    draw = ImageDraw.Draw(img)
    font = ImageFont.load_default()

    # --- Define layout ---
    cal_width = int(WIDTH * 2 / 3)
    events_width = WIDTH - cal_width
    left_margin = 2
    top_margin = 2

    # --- Draw Month and Year at top of calendar ---
    month_name = current_date.strftime("%B %Y")
    bbox = draw.textbbox((0, 0), month_name, font=font)
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]
    draw.text(((cal_width - text_w)//2, top_margin), month_name, fill=0, font=font)

    # --- Draw Weekday Headers ---
    weekdays = ["Mo","Tu","We","Th","Fr","Sa","Su"]
    square_width = cal_width // 7
    header_y = top_margin + text_h + 2
    for i, day_name in enumerate(weekdays):
        draw.text((i*square_width + 2, header_y), day_name, fill=0, font=font)

    # --- Draw Day Grid ---
    cal = calendar.monthcalendar(current_date.year, current_date.month)
    start_y = header_y + 10
    square_height = (HEIGHT - start_y - 2) // len(cal)  # full height minus top

    for y, week in enumerate(cal):
        for x, day in enumerate(week):
            if day != 0:
                x0 = x * square_width
                y0 = start_y + y * square_height
                x1 = x0 + square_width
                y1 = y0 + square_height
                draw.rectangle([x0, y0, x1, y1], outline=0)
                draw.text((x0 + 2, y0 + 2), str(day), fill=0, font=font)

    # --- Draw Upcoming Events on the right ---
    events_x = cal_width + 2
    events_y = top_margin
    draw.text((events_x, events_y), "Events:", fill=0, font=font)
    events_y += 10
    for event in events[:10]:  # show top 10 events
        # wrap text if too long
        title = event['title']
        date = event['date']
        draw.text((events_x, events_y), f"{title}", fill=0, font=font)
        events_y += 12
        draw.text((events_x, events_y), f"{date}", fill=0, font=font)
        events_y += 12

    # --- Save Image ---
    img.save(save_path)


