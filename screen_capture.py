import mss
from PIL import Image

def capture_screen(region=None):
    with mss.mss() as sct:
        monitor = sct.monitors[1] if region is None else region
        screenshot = sct.grab(monitor)
        img = Image.frombytes('RGB', (screenshot.width, screenshot.height), screenshot.rgb)
        return img
