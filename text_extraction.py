import re
import pytesseract
from fuzzywuzzy import fuzz

def find_equip_position(image):
    data = pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT)
    for i in range(len(data['text'])):
        if "Equip" in data['text'][i]:
            x, y, w, h = data['left'][i], data['top'][i], data['width'][i], data['height'][i]
            return (x, y, w, h)
    return None

def extract_text_from_image(image):
    custom_oem_psm_config = r'--oem 3 --psm 6'
    data = pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT, config=custom_oem_psm_config)
    
    lines = []
    bounding_boxes = []
    current_line = ""
    current_bbox = None

    for i in range(len(data['text'])):
        if data['text'][i].strip() == "":
            if current_line.strip():
                lines.append(current_line.strip())
                bounding_boxes.append(tuple(current_bbox))
            current_line = ""
            current_bbox = None
        else:
            if current_bbox is None:
                current_bbox = [data['left'][i], data['top'][i], data['width'][i], data['height'][i]]
            else:
                current_bbox[2] = max(current_bbox[2], data['left'][i] + data['width'][i] - current_bbox[0])
                current_bbox[3] = max(current_bbox[3], data['top'][i] + data['height'][i] - current_bbox[1])
            current_line += " " + data['text'][i]

    if current_line.strip():
        lines.append(current_line.strip())
        bounding_boxes.append(tuple(current_bbox))

    # Ensure bounding_boxes is a list of tuples (text, bounding box)
    bounding_boxes = [(line, bbox) for line, bbox in zip(lines, bounding_boxes)]
    
    return "\n".join(lines), bounding_boxes

def compare_stats(extracted_text, best_stats):
    priority_match = {1: [], 2: [], 3: []}
    extracted_text_lines = extracted_text.split('\n')

    for priority, stats in best_stats.items():
        for stat in stats:
            stat_clean = re.sub(r'[^a-zA-Z\s]', '', stat).strip().lower()
            for line in extracted_text_lines:
                line_clean = re.sub(r'[^a-zA-Z\s]', '', line).strip().lower()
                if fuzz.ratio(line_clean, stat_clean) > 80:
                    priority_match[int(priority)].append(stat)
    return priority_match
