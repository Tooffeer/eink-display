from PIL import Image

# Try to import the Waveshare driver
try:
    from waveshare_epd import epd2in13_V4
    EINK_AVAILABLE = True
except (ImportError, RuntimeError):
    EINK_AVAILABLE = False
    print("E-Ink hardware not available — running in PC mode.")

def update_eink(image_path):
    if not EINK_AVAILABLE:
        print(f"Skipping E-Ink update for {image_path}")
        return

    try:
        from waveshare_epd import epd2in13_V4
        # --- Initialize display ---
        epd = epd2in13_V4.EPD()
        epd.init()
        epd.Clear()

        # --- Open image ---
        img = Image.open(image_path)
        img = img.convert('1')  # ensure 1-bit B/W

        # --- Display image ---
        epd.display(epd.getbuffer(img))

        # --- Put display to sleep ---
        epd.sleep()
        print("E-Ink display updated successfully.")

    except Exception as e:
        print("Error updating E-Ink display:", e)
