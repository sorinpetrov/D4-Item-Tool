import time
import keyboard
from screen_capture import capture_screen
from image_processing import preprocess_image
from text_extraction import find_equip_position, extract_text_from_image, compare_stats
from utils import toggle_capture_state
from item_detection import detect_item_type
from stats_loader import load_best_stats, update_best_stats
from pynput import mouse

def main():
    state = {'capturing': False}

    # Ask user if they want to update the priority list
    update_list = input("Do you want to update the priority list? (yes/no): ").strip().lower()
    if update_list == 'yes':
        update_best_stats()
    
    best_stats = load_best_stats()

    def on_click(x, y, button, pressed):
        if button == mouse.Button.middle and pressed and state['capturing']:
            capture_and_process()

    def capture_and_process():
        print("Capturing...")
        scan_region = {'top': 1015, 'left': 1150, 'width': 950, 'height': 250}
        equip_image = capture_screen(scan_region)
        preprocessed_image = preprocess_image(equip_image)
        preprocessed_image.save("preprocessed_equip_image.png")
        equip_position = find_equip_position(preprocessed_image)

        if equip_position:
            print(f"Equip text found at position: {equip_position}")
            ex, ey, ew, eh = equip_position
            item_window_top = 1015 + ey - 15 - 1000
            item_window_left = 1150 + ex - 25
            region = {'top': item_window_top, 'left': item_window_left, 'width': 500, 'height': 1000}
            print(f"Calculated region: {region}")
            item_image = capture_screen(region)
            item_image.save("captured_item_image.png")
            extracted_text = extract_text_from_image(item_image)
            print("Extracted Text:\n", extracted_text)

            # Detect item type
            item_type = detect_item_type(extracted_text)
            print(f"Detected Item Type: {item_type}")

            # Check stats
            if item_type in best_stats:
                priority_match = compare_stats(extracted_text, best_stats[item_type])
                print(f"Priority Match: {priority_match}")
                for priority, stats in priority_match.items():
                    if stats:
                        print(f"Priority {priority} stats: {', '.join(stats)}")
                    else:
                        print(f"Priority {priority} stats: None")
            else:
                print("No best stats defined for this item type.")
        else:
            print("Equip text not found")

    print("Press Caps Lock to start/stop capturing. Press Esc to exit.")
    keyboard.on_press_key('caps lock', lambda _: toggle_capture_state(state))

    listener = mouse.Listener(on_click=on_click)
    listener.start()

    while True:
        if keyboard.is_pressed('esc'):
            print("Exiting...")
            listener.stop()
            break

        time.sleep(0.1)  # Small delay to reduce CPU usage

if __name__ == "__main__":
    main()
