from PIL import Image, ImageEnhance, ImageFilter

def preprocess_image(image):
    # Convert to grayscale
    gray = image.convert('L')
    # Enhance contrast
    enhancer = ImageEnhance.Contrast(gray)
    enhanced = enhancer.enhance(1.0)  # Adjusted to 1.0 as per your successful attempt
    # Apply a binary threshold to get a clean black-and-white image
    bw = enhanced.point(lambda x: 0 if x < 128 else 255, '1')
    return bw
