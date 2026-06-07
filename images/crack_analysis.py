import cv2

def calculate_crack_percentage(image_path):

    img = cv2.imread(image_path)

    if img is None:
        return 0

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    edges = cv2.Canny(gray, 100, 200)

    crack_pixels = cv2.countNonZero(edges)

    total_pixels = gray.shape[0] * gray.shape[1]

    crack_percentage = (crack_pixels / total_pixels) * 100

    return round(crack_percentage, 2)