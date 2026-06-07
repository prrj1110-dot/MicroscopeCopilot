import cv2

img = cv2.imread("microscope.jpg")
img = cv2.imread(r"C:\Users\LC_18\Desktop\MicroscopeCopilot\microscope.jpg")
if img is None:
    print("Image not found!")
    exit()

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

_, thresh = cv2.threshold(gray, 120, 255, cv2.THRESH_BINARY)

contours, _ = cv2.findContours(
    thresh,
    cv2.RETR_EXTERNAL,
    cv2.CHAIN_APPROX_SIMPLE
)

particle_count = 0

for cnt in contours:
    area = cv2.contourArea(cnt)

    if area > 100:
        particle_count += 1
        cv2.drawContours(img, [cnt], -1, (0, 255, 0), 2)

print("Particles Found =", particle_count)

cv2.imshow("Detected Particles", img)
cv2.waitKey(0)
cv2.destroyAllWindows()