import re
from screen_capture import capture_screen
from image_processing import preprocess_image
from text_extraction import find_equip_position, extract_text_from_image, compare_stats
from item_detection import detect_item_type
from fuzzywuzzy import fuzz

def capture_and_process(best_stats):
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
        item_window_left = 1125 + ex - 25  # Adjusted by 25px as per your correction
        region = {'top': item_window_top, 'left': item_window_left, 'width': 500, 'height': 1000}
        print(f"Calculated region: {region}")
        item_image = capture_screen(region)
        item_image.save("captured_item_image.png")

        # Extract text and bounding boxes from the original captured image
        extracted_text, bounding_boxes = extract_text_from_image(item_image)
        print("Extracted Text:\n", extracted_text)
        print("Bounding Boxes:\n", bounding_boxes)

        # Use text from bounding boxes for item detection
        bounding_box_text = " ".join([text for text, _ in bounding_boxes])
        cleaned_extracted_text = re.sub(r'[^a-zA-Z\s]', '', bounding_box_text).lower()
        print(f"Cleaned Extracted Text for Item Detection: {cleaned_extracted_text}")

        # Detect item type
        item_type = detect_item_type(cleaned_extracted_text)
        print(f"Detected Item Type: {item_type}")

        # Check stats
        if item_type in best_stats:
            priority_match = compare_stats(bounding_box_text, best_stats[item_type])
            print(f"Priority Match: {priority_match}")
            stats_with_priority = []
            for priority, stats in priority_match.items():
                for stat in stats:
                    for text, bbox in bounding_boxes:
                        stat_clean = re.sub(r'\d+', '', stat).strip().lower()
                        text_clean = re.sub(r'\d+', '', text).strip().lower()
                        if fuzz.partial_ratio(stat_clean, text_clean) > 80:  # Use fuzzy matching
                            # Adjust bounding box coordinates to account for the offset
                            adjusted_bbox = (
                                bbox[0] + region['left'], 
                                bbox[1] + region['top'], 
                                bbox[2], 
                                bbox[3]
                            )
                            stats_with_priority.append((text, int(priority), adjusted_bbox))
            return stats_with_priority
        else:
            print("No best stats defined for this item type.")
            return []
    else:
        print("Equip text not found")
        return []
