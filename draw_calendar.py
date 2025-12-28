from PIL import Image, ImageDraw, ImageFont
import calendar
from datetime import datetime
import os

WIDTH = 250
HEIGHT = 122

def draw_calendar(current_date, events, save_path):
    print("Drawing calendar image")

    # --- Create image ---
    img = Image.new("1", (WIDTH, HEIGHT), 1)  # 1-bit B/W, white background
    draw = ImageDraw.Draw(img)
    font = ImageFont.load_default()

    # --- Date helpers ---
    today_real = datetime.now()
    today = today_real.day
    current_year = current_date.year
    current_month = current_date.month

    # --- Collect event days for this month ---
    event_days = set()
    for event in events:
        try:
            event_date = datetime.strptime(event['date'], "%Y-%m-%d")
            if event_date.year == current_year and event_date.month == current_month:
                event_days.add(event_date.day)
        except Exception:
            pass

    # --- Define layout ---
    cal_width = int(WIDTH * 2 / 3)
    events_width = WIDTH - cal_width
    left_margin = 2
    top_margin = 2

    # --- Draw Month and Year ---
    month_name = current_date.strftime("%B %Y")
    bbox = draw.textbbox((0, 0), month_name, font=font)
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]
    draw.text(
        ((cal_width - text_w) // 2, top_margin),
        month_name,
        fill=0,
        font=font
    )

    # --- Draw Weekday Headers ---
    weekdays = ["Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"]
    square_width = cal_width // 7
    header_y = top_margin + text_h + 2

    for i, day_name in enumerate(weekdays):
        draw.text((i * square_width + 2, header_y), day_name, fill=0, font=font)

    # --- Draw Day Grid ---
    cal = calendar.monthcalendar(current_year, current_month)
    start_y = header_y + 10
    square_height = (HEIGHT - start_y - 2) // len(cal)

    for y, week in enumerate(cal):
        for x, day in enumerate(week):
            if day == 0:
                continue

            x0 = x * square_width
            y0 = start_y + y * square_height
            x1 = x0 + square_width
            y1 = y0 + square_height

            is_today = (
                day == today and
                current_year == today_real.year and
                current_month == today_real.month
            )

            # Background
            if is_today:
                draw.rectangle([x0, y0, x1, y1], fill=0)
                text_color = 1
            else:
                draw.rectangle([x0, y0, x1, y1], outline=0)
                text_color = 0

            # Day number
            draw.text((x0 + 2, y0 + 2), str(day), fill=text_color, font=font)

            # Event dot
            if day in event_days:
                dot_radius = 2
                dot_x = x1 - 6
                dot_y = y0 + 6
                draw.ellipse(
                    [
                        dot_x - dot_radius,
                        dot_y - dot_radius,
                        dot_x + dot_radius,
                        dot_y + dot_radius
                    ],
                    fill=text_color if is_today else 0
                )

    # --- Draw Events List ---
    events_x = cal_width + 2
    events_y = top_margin
    draw.text((events_x, events_y), "Events:", fill=0, font=font)
    events_y += 10

    for event in events[:10]:
        title = event.get('title', '')
        date = event.get('date', '')
        draw.text((events_x, events_y), title, fill=0, font=font)
        events_y += 12
        draw.text((events_x, events_y), date, fill=0, font=font)
        events_y += 12

    # --- Save image ---
    img.save(save_path)
