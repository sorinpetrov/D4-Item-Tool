import time
import keyboard
import queue
from capture_process import capture_and_process
from utils import toggle_capture_state
from stats_loader import load_best_stats, update_best_stats
from mouse_listener import start_mouse_listener
from overlay import create_overlay, update_overlay, update_state_circle

def main():
    state = {'capturing': False}
    overlay_queue = queue.Queue()

    # Ask user if they want to update the priority list
    update_list = input("Do you want to update the priority list? (yes/no): ").strip().lower()
    if update_list == 'yes':
        update_best_stats()
    
    best_stats = load_best_stats()

    root, canvas, state_circle = create_overlay()

    def capture_and_process_with_overlay(best_stats):
        print("Capturing and processing with overlay...")
        stats_with_priority = capture_and_process(best_stats)
        print(f"Stats with priority: {stats_with_priority}")
        overlay_queue.put(stats_with_priority)

    def toggle_capture_state(state):
        state['capturing'] = not state['capturing']
        update_state_circle(canvas, state_circle, state['capturing'])

    print("Press Caps Lock to start/stop capturing. Press any key to clear overlay when capturing is on. Press Esc to exit.")
    keyboard.on_press_key('caps lock', lambda _: toggle_capture_state(state))

    listener = start_mouse_listener(state, best_stats, capture_and_process_with_overlay)
    listener.start()

    def process_queue():
        try:
            while True:
                stats_with_priority = overlay_queue.get_nowait()
                update_overlay(canvas, stats_with_priority)
        except queue.Empty:
            pass
        root.after(100, process_queue)  # Check the queue every 100ms

    def clear_overlay(canvas):
        items = canvas.find_withtag('stat_circle')
        for item in items:
            canvas.delete(item)
        update_state_circle(canvas, state_circle, state['capturing'])

    def clear_on_key_press(event):
        if state['capturing']:
            clear_overlay(canvas)

    keyboard.on_press(clear_on_key_press)

    root.after(100, process_queue)  # Start processing the queue
    update_state_circle(canvas, state_circle, state['capturing'])  # Initialize the state circle
    root.mainloop()

    listener.stop()  # Ensure the listener stops when the main loop ends

if __name__ == "__main__":
    main()
