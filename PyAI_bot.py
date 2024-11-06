import cv2
import numpy as np
import pyautogui
import time
import mss

# Convert hex to BGR color format
def hex_to_bgr(hex_color):
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))[::-1]  # Convert hex to BGR

# Constants
wheat_color = hex_to_bgr("#e3dc7b")  # Wheat color (adjust if needed)
wheat_color_hsv = cv2.cvtColor(np.uint8([[wheat_color]]), cv2.COLOR_BGR2HSV)[0][0]

# Tighter HSV range for wheat color detection
tolerance_hue = 5
tolerance_saturation = 50
tolerance_value = 50

WHEAT_COLOR_LOWER = np.array([
    max(0, wheat_color_hsv[0] - tolerance_hue), 
    max(0, wheat_color_hsv[1] - tolerance_saturation), 
    max(0, wheat_color_hsv[2] - tolerance_value)
])
WHEAT_COLOR_UPPER = np.array([
    min(179, wheat_color_hsv[0] + tolerance_hue), 
    min(255, wheat_color_hsv[1] + tolerance_saturation), 
    min(255, wheat_color_hsv[2] + tolerance_value)
])

MONITOR_REGION = {"top": 0, "left": 0, "width": 1920, "height": 1080}
BREAK_KEY = 'left'
MOVE_KEYS = ['w', 'a', 's', 'd']

def capture_screen(monitor):
    with mss.mss() as sct:
        screen = np.array(sct.grab(monitor))
        screen = cv2.cvtColor(screen, cv2.COLOR_BGRA2BGR)
    return screen

def find_wheat(screenshot):
    hsv_img = cv2.cvtColor(screenshot, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv_img, WHEAT_COLOR_LOWER, WHEAT_COLOR_UPPER)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    wheat_locations = []
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > 800:  # Increased threshold to avoid detecting small objects
            x, y, w, h = cv2.boundingRect(contour)
            wheat_locations.append((x + w // 2, y + h // 2))
            # Debug: Draw rectangles around detected areas for verification
            cv2.rectangle(screenshot, (x, y), (x + w, y + h), (0, 255, 0), 2)

    cv2.imshow("Detected Wheat", screenshot)  # Display for debugging
    cv2.waitKey(1)
    return wheat_locations

def break_wheat(location):
    pyautogui.moveTo(location[0], location[1], duration=0.1)
    pyautogui.click(button=BREAK_KEY)

def move_forward(duration):
    pyautogui.keyDown('w')
    time.sleep(duration)
    pyautogui.keyUp('w')

def turn_right(duration):
    pyautogui.moveRel(100, 0, duration=duration)

def turn_left(duration):
    pyautogui.moveRel(-100, 0, duration=duration)

def search_area():
    move_forward(1)
    turn_right(0.5)

def run_bot():
    print("Starting in 5 seconds. Please switch to Minecraft.")
    time.sleep(5)
    print("Bot started. Press Ctrl+C to stop.")

    try:
        while True:
            screenshot = capture_screen(MONITOR_REGION)
            wheat_locations = find_wheat(screenshot)

            if wheat_locations:
                print(f"Wheat found at: {wheat_locations}")
                for location in wheat_locations:
                    break_wheat(location)
                    time.sleep(0.2)
            else:
                search_area()

            time.sleep(0.1)
    except KeyboardInterrupt:
        print("Bot stopped by user.")
    finally:
        for key in MOVE_KEYS:
            pyautogui.keyUp(key)
        cv2.destroyAllWindows()  # Close any OpenCV windows

if __name__ == "__main__":
    run_bot()
