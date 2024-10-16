import threading
import time
import pyautogui
import numpy as np
import sys
from pydub import AudioSegment
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
import pythoncom
from pycaw.pycaw import AudioUtilities, IAudioMeterInformation

time.sleep(6)

def farm(action_duration=72, cycles=6, repeat=4):
    try:
        for j in range(repeat):
            for i in range(cycles):
                pyautogui.keyDown('w')
                pyautogui.keyDown('a')
                pyautogui.mouseDown()

                time.sleep(action_duration)

                pyautogui.keyUp('a')
                pyautogui.keyDown('d')

                time.sleep(action_duration)

                pyautogui.keyUp('w')
                pyautogui.keyUp('d')
                pyautogui.mouseUp()

                print(f"Cycle {i+1} of set {j+1} completed")

            print(f"All cycles of set {j+1} completed")
            time.sleep(4)  #delay between repetitions
        print("All cycles completed")

    except KeyboardInterrupt:
        print("script interrupted.")

#compare target sound with desktop audio
def match_sound(target_sound, input_segment, threshold=0.5, noise_floor=500):
    target_data = np.array(target_sound.get_array_of_samples())
    input_data = np.array(input_segment.get_array_of_samples())

    min_len = min(len(target_data), len(input_data))
    target_data = target_data[:min_len]
    input_data = input_data[:min_len]

    input_energy = np.sum(input_data**2)
    if input_energy < noise_floor:
        return False

    target_energy = np.sum(target_data**2)
    if target_energy == 0:
        return False

    correlation = np.correlate(input_data, target_data, mode='valid')
    similarity = np.max(correlation) / target_energy

    return similarity >= threshold

def get_system_audio_levels():
    pythoncom.CoInitialize() 
    try:
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(
            IAudioMeterInformation._iid_, CLSCTX_ALL, None)
        meter = cast(interface, POINTER(IAudioMeterInformation))
        return meter.GetPeakValue()
    finally:
        pythoncom.CoUninitialize()  

#monitor desktop audio
def monitor_system_audio(threshold=0.02, max_mismatch_duration=6):
    mismatch_start_time = None

    while True:
        level = get_system_audio_levels()
        print(f"System Audio Level: {level}")

        if level > threshold:
            mismatch_start_time = None
        else:
            if mismatch_start_time is None:
                mismatch_start_time = time.time()
            else:
                current_time = time.time()
                if current_time - mismatch_start_time >= max_mismatch_duration:
                    print("No audio detected for the specified duration. Performing action.")
                    pyautogui.mouseUp()
                    pyautogui.keyUp("a")
                    pyautogui.keyUp("w")
                    pyautogui.keyUp("d")

                    pyautogui.moveRel(20,200, duration=.7)

                    time.sleep(.3)
                    pyautogui.press('enter')
                    pyautogui.typewrite('what', interval=.9)
                    pyautogui.press('enter')
                    time.sleep(3)
                    pyautogui.press("esc")
                    time.sleep(.5)
                    pyautogui.locateOnScreen("Disconnec.png", confidence=.6)
                    pyautogui.center("Disconnect.png")
                    # pyautogui.moveTo(960,680, duration=.6)
                    time.sleep(1)
                    pyautogui.click()
                    sys.exit()

        time.sleep(3)  #polling interval

#threads for both functions
movement_thread = threading.Thread(target=farm)
audio_thread = threading.Thread(target=monitor_system_audio)

#start both threads
movement_thread.start()
audio_thread.start()

try:
    # Join the threads to keep the main script running
    movement_thread.join()
    audio_thread.join()
except KeyboardInterrupt:
    print("Main script interrupted. Exiting gracefully.")
    quit()


