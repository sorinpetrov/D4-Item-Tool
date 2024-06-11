import re
import pytesseract
from PIL import Image, ImageEnhance, ImageFilter

def find_equip_position(image):
    data = pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT)
    for i in range(len(data['text'])):
        if "Equip" in data['text'][i]:
            x, y, w, h = data['left'][i], data['top'][i], data['width'][i], data['height'][i]
            return (x, y, w, h)
    return None

def preprocess_image(image):
    image = image.convert('L')  # Convert to grayscale
    image = image.filter(ImageFilter.SHARPEN)  # Sharpen the image
    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(2)  # Increase contrast
    return image

def extract_text_from_image(image):
    custom_oem_psm_config = r'--oem 3 --psm 6'
    data = pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT, config=custom_oem_psm_config)
    text = "\n".join([t for t in data['text'] if t.strip() != ""])
    bounding_boxes = [(data['text'][i], (data['left'][i], data['top'][i], data['width'][i], data['height'][i])) for i in range(len(data['text'])) if data['text'][i].strip() != ""]
    
    # Group text lines by their proximity
    grouped_bboxes = []
    current_phrase = []
    current_bbox = [float('inf'), float('inf'), 0, 0]

    for i in range(len(data['text'])):
        if int(data['conf'][i]) > 0 and data['text'][i].strip() != "":
            text = data['text'][i].strip()
            x, y, w, h = data['left'][i], data['top'][i], data['width'][i], data['height'][i]

            if current_phrase and (abs(current_bbox[1] - y) > h or abs(current_bbox[0] + current_bbox[2] - x) > w):
                # Append current phrase and reset
                grouped_bboxes.append((" ".join(current_phrase), tuple(current_bbox)))
                current_phrase = []
                current_bbox = [float('inf'), float('inf'), 0, 0]

            # Update current bounding box
            current_bbox[0] = min(current_bbox[0], x)
            current_bbox[1] = min(current_bbox[1], y)
            current_bbox[2] = max(current_bbox[2], x + w - current_bbox[0])
            current_bbox[3] = max(current_bbox[3], y + h - current_bbox[1])

            # Append to current phrase
            current_phrase.append(text)

    if current_phrase:
        grouped_bboxes.append((" ".join(current_phrase), tuple(current_bbox)))

    return text, grouped_bboxes

def compare_stats(extracted_text, best_stats):
    priority_match = {1: [], 2: [], 3: []}
    # Remove numeric values from the extracted text for comparison
    extracted_text_clean = re.sub(r'\d+', '', extracted_text)

    for priority, stats in best_stats.items():
        for stat in stats:
            # Remove numeric values from the stat for comparison
            stat_clean = re.sub(r'\d+', '', stat)
            if re.search(r'\b' + re.escape(stat_clean) + r'\b', extracted_text_clean, re.IGNORECASE):
                priority_match[int(priority)].append(stat)
    return priority_match
