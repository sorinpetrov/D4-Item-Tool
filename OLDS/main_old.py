import time
import keyboard
from capture_process import capture_and_process
from utils import toggle_capture_state
from stats_loader import load_best_stats, update_best_stats
from mouse_listener import start_mouse_listener
from overlay import create_overlay, update_overlay

def main():
    state = {'capturing': False}

    # Ask user if they want to update the priority list
    update_list = input("Do you want to update the priority list? (yes/no): ").strip().lower()
    if update_list == 'yes':
        update_best_stats()
    
    best_stats = load_best_stats()

    screen = create_overlay()

    def capture_and_process_with_overlay(best_stats):
        stats_with_priority = capture_and_process(best_stats)
        update_overlay(screen, stats_with_priority)

    print("Press Caps Lock to start/stop capturing. Press Esc to exit.")
    keyboard.on_press_key('caps lock', lambda _: toggle_capture_state(state))

    listener = start_mouse_listener(state, best_stats, capture_and_process_with_overlay)
    listener.start()

    while True:
        if keyboard.is_pressed('esc'):
            print("Exiting...")
            listener.stop()
            break

        time.sleep(0.1)  # Small delay to reduce CPU usage

if __name__ == "__main__":
    main()
