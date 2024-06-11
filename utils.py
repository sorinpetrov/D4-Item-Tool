import re
import pytesseract

def toggle_capture_state(state):
    state['capturing'] = not state['capturing']
    print(f"Capturing state toggled: {state['capturing']}")

def clean_text(text):
    return re.sub(r'\d+', '', text).strip().lower()

def extract_text_with_boxes(image):
    custom_oem_psm_config = r'--oem 3 --psm 6'
    data = pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT, config=custom_oem_psm_config)
    
    bounding_boxes = [(data['text'][i], (data['left'][i], data['top'][i], data['width'][i], data['height'][i])) 
                      for i in range(len(data['text'])) if data['text'][i].strip() != ""]

    return "\n".join([t for t in data['text'] if t.strip() != ""]), bounding_boxes
