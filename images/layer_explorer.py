import cv2

# Load image
img = cv2.imread(r"C:\Users\LC_18\Desktop\MicroscopeCopilot\microscope.jpg")

if img is None:
    print("Image not found!")
    exit()

# Layer 1: Original
original = img.copy()

# Layer 2: Structure Layer
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
structure = cv2.Canny(gray, 100, 200)

# Layer 3: Defect Layer
_, defects = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY_INV)

# Layer 4: Particle Layer
particle_img = img.copy()

contours, _ = cv2.findContours(
    defects,
    cv2.RETR_EXTERNAL,
    cv2.CHAIN_APPROX_SIMPLE
)

particle_count = 0

for cnt in contours:
    area = cv2.contourArea(cnt)

    if area > 100:
        particle_count += 1
        cv2.drawContours(
            particle_img,
            [cnt],
            -1,
            (0, 255, 0),
            2
        )

# Metrics
total_pixels = gray.shape[0] * gray.shape[1]
pore_pixels = cv2.countNonZero(defects)

porosity = (pore_pixels / total_pixels) * 100

crack_pixels = cv2.countNonZero(structure)
crack_percent = (crack_pixels / total_pixels) * 100

print("\n===== LAYER EXPLORER REPORT =====")
print("Particles Found =", particle_count)
print("Porosity (%) =", round(porosity, 2))
print("Crack Percentage (%) =", round(crack_percent, 2))
# Material Health Score

health_score = 100 - (porosity * 0.8) - (crack_percent * 1.2)

if health_score > 80:
    status = "Excellent"
elif health_score > 60:
    status = "Good"
elif health_score > 40:
    status = "Moderate"
else:
    status = "Poor"

print("Material Health Score =", round(health_score, 2))
print("Material Condition =", status)

print("\nProject: Seeing Matter in Layers")
print("Analysis Complete Successfully")
# Display Layers
cv2.imshow("Layer 1 - Observation", original)
cv2.imshow("Layer 2 - Structure", structure)
cv2.imshow("Layer 3 - Defects", defects)
cv2.imshow("Layer 4 - Nanoscale Features", particle_img)

cv2.waitKey(0)
cv2.destroyAllWindows()