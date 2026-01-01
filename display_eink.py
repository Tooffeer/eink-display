from PIL import Image

def update_eink(image_path):
    try:
        from waveshare_epd import epd2in13_V4

        epd = epd2in13_V4.EPD()
        epd.init()
        epd.Clear()

        img = Image.open(image_path).convert("1")
        epd.display(epd.getbuffer(img))

        epd.sleep()
        print("E-Ink display updated")

    except Exception as e:
        # Safe on PC, safe if hardware not ready
        print("Skipping E-Ink update:", e)
