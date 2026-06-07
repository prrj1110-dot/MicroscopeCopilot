import cv2

def calculate_porosity(image_path):

```
img = cv2.imread(image_path)

if img is None:
    return 0

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

_, thresh = cv2.threshold(
    gray,
    100,
    255,
    cv2.THRESH_BINARY_INV
)

total_pixels = gray.shape[0] * gray.shape[1]

pore_pixels = cv2.countNonZero(thresh)

porosity = (pore_pixels / total_pixels) * 100

return round(porosity, 2)
```
