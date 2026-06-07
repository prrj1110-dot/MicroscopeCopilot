import cv2

# Load image
img = cv2.imread(r"C:\Users\LC_18\Desktop\MicroscopeCopilot\microscope.jpg")

if img is None:
    print("Image not found!")
    exit()

# Resize for display
img = cv2.resize(img, (900, 700))

# Layer 1 - Original
cv2.imshow("Layer 1 - Original Structure", img)

# Layer 2 - Grayscale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
cv2.imshow("Layer 2 - Microstructure", gray)

# Layer 3 - Porosity
_, porosity = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY_INV)
cv2.imshow("Layer 3 - Porosity Map", porosity)

# Layer 4 - Crack Detection
cracks = cv2.Canny(gray, 50, 150)
cv2.imshow("Layer 4 - Crack Network", cracks)

print("\n===== SEEING MATTER IN LAYERS =====")
print("Layer 1 : Original Structure")
print("Layer 2 : Microstructure")
print("Layer 3 : Porosity Analysis")
print("Layer 4 : Crack Analysis")
print("\nAnalysis Completed Successfully")

cv2.waitKey(0)
cv2.destroyAllWindows()