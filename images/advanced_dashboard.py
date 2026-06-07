import cv2
import numpy as np
import pandas as pd
from tkinter import Tk
from tkinter.filedialog import askopenfilename

# Select image
Tk().withdraw()

image_path = askopenfilename(
    title="Select Microscope Image",
    filetypes=[("Image Files", "*.jpg *.jpeg *.png *.bmp")]
)

if not image_path:
    print("No image selected!")
    exit()

img = cv2.imread(image_path)

if img is None:
    print("Image not found!")
    exit()

# Resize
img = cv2.resize(img, (600, 400))

# Grayscale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Porosity Detection
_, porosity = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY_INV)
# Particle Analysis
num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(
    porosity, connectivity=8
)

particle_data = []

for i in range(1, num_labels):
    area = stats[i, cv2.CC_STAT_AREA]

    if area > 10:
        diameter = np.sqrt((4 * area) / np.pi)

        particle_data.append([
            i,
            area,
            round(diameter, 2)
        ])
# Crack Detection
# Improved Crack Detection

gray_blur = cv2.GaussianBlur(gray, (5,5), 0)

thresh = cv2.adaptiveThreshold(
    gray_blur,
    255,
    cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
    cv2.THRESH_BINARY_INV,
    11,
    2
)

kernel = np.ones((3,3), np.uint8)

cracks = cv2.morphologyEx(
    thresh,
    cv2.MORPH_OPEN,
    kernel
)
# Remove noise
kernel = np.ones((3,3), np.uint8)
cracks = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)

# Keep only long thin objects
num_labels, labels, stats, _ = cv2.connectedComponentsWithStats(cracks)

filtered = np.zeros_like(cracks)

for i in range(1, num_labels):
    area = stats[i, cv2.CC_STAT_AREA]

    if area > 500:
        filtered[labels == i] = 255

cracks = filtered
# Particle Count
particle_data = []
contours, _ = cv2.findContours(
    porosity,
    cv2.RETR_EXTERNAL,
    cv2.CHAIN_APPROX_SIMPLE
)
particle_count = 0

for cnt in contours:

    area = cv2.contourArea(cnt)

    if area > 20:

        particle_count += 1

        diameter = np.sqrt(4 * area / np.pi)

        particle_data.append([
            particle_count,
            round(area, 2),
            round(diameter, 2)
        ])
# Porosity %
porosity_percent = (
    np.count_nonzero(porosity) /
    porosity.size
) * 100

# Crack %
crack_pixels = cv2.countNonZero(cracks)

crack_percent = (
    crack_pixels /
    cracks.size
) * 100

# Health Score
health_score = max(
    0,
    100 - (porosity_percent + crack_percent)
)

# Grade
if health_score >= 80:
    grade = "EXCELLENT"
elif health_score >= 60:
    grade = "GOOD"
elif health_score >= 40:
    grade = "MODERATE"
else:
    grade = "POOR"
# Save Report

with open("analysis_report.txt", "w") as report:
    report.write("Material Analysis Report\n")
    report.write("========================\n\n")

    report.write(f"Particles      : {particle_count}\n")
    report.write(f"Porosity (%)   : {porosity_percent:.2f}\n")
    report.write(f"Cracks (%)     : {crack_percent:.2f}\n")
    report.write(f"Health Score   : {health_score:.2f}\n")
    report.write(f"Grade          : {grade}\n")

print("Report saved: analysis_report.txt")
# Convert to BGR
gray_bgr = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
porosity_bgr = cv2.cvtColor(porosity, cv2.COLOR_GRAY2BGR)
cracks_bgr = cv2.cvtColor(cracks, cv2.COLOR_GRAY2BGR)

# Dashboard Layout
top = np.hstack((img, gray_bgr))
bottom = np.hstack((porosity_bgr, cracks_bgr))
dashboard = np.vstack((top, bottom))

# Title
cv2.putText(
    dashboard,
    "SEEING MATTER IN LAYERS",
    (20, 40),
    cv2.FONT_HERSHEY_SIMPLEX,
    1.2,
    (0, 255, 0),
    3
)

# Labels
cv2.putText(
    dashboard,
    "Original Structure",
    (20, 80),
    cv2.FONT_HERSHEY_SIMPLEX,
    0.8,
    (255, 255, 255),
    2
)

cv2.putText(
    dashboard,
    "Microstructure",
    (620, 80),
    cv2.FONT_HERSHEY_SIMPLEX,
    0.8,
    (255, 255, 255),
    2
)

cv2.putText(
    dashboard,
    "Porosity Analysis",
    (20, 440),
    cv2.FONT_HERSHEY_SIMPLEX,
    0.8,
    (255, 255, 255),
    2
)

cv2.putText(
    dashboard,
    "Crack Analysis",
    (620, 440),
    cv2.FONT_HERSHEY_SIMPLEX,
    0.8,
    (255, 255, 255),
    2
)

# Metrics
cv2.putText(
    dashboard,
    f"Particles: {particle_count}",
    (20, 730),
    cv2.FONT_HERSHEY_SIMPLEX,
    0.8,
    (0, 255, 0),
    2
)

cv2.putText(
    dashboard,
    f"Porosity: {porosity_percent:.2f}%",
    (20, 760),
    cv2.FONT_HERSHEY_SIMPLEX,
    0.8,
    (0, 255, 0),
    2
)

cv2.putText(
    dashboard,
    f"Cracks: {crack_percent:.2f}%",
    (350, 730),
    cv2.FONT_HERSHEY_SIMPLEX,
    0.8,
    (0, 255, 0),
    2
)

cv2.putText(
    dashboard,
    f"Health Score: {health_score:.2f}",
    (350, 760),
    cv2.FONT_HERSHEY_SIMPLEX,
    0.8,
    (0, 255, 0),
    2
)

cv2.putText(
    dashboard,
    f"Grade: {grade}",
    (700, 760),
    cv2.FONT_HERSHEY_SIMPLEX,
    0.8,
    (0, 255, 255),
    2
)

# Save Image
cv2.imwrite("dashboard_result.png", dashboard)

# Save Report
with open("analysis_report.txt", "w") as report:
    report.write("===== SEEING MATTER IN LAYERS REPORT =====\n")
    report.write(f"Particles Found: {particle_count}\n")
    report.write(f"Porosity (%): {porosity_percent:.2f}\n")
    report.write(f"Crack Percentage (%): {crack_percent:.2f}\n")
    report.write(f"Health Score: {health_score:.2f}\n")
    report.write(f"Material Grade: {grade}\n")

# Display
cv2.imshow("Material Layer Explorer", dashboard)
key = cv2.waitKey(0)
print("Window closed")
cv2.destroyAllWindows()
print("Dashboard closed")
# Excel Export
df = pd.DataFrame(
    particle_data,
    columns=[
        "Particle ID",
        "Area (px²)",
        "Equivalent Diameter"
    ]
)

df.to_excel(
    "particle_distribution.xlsx",
    index=False
)

print("Particle table saved!")
# =========================
# SAVE RESULTS TO EXCEL
# =========================

import pandas as pd

data = {
    "Parameter": [
        "Particles",
        "Porosity (%)",
        "Crack Percentage (%)",
        "Health Score",
        "Material Grade"
    ],
    "Value": [
        particle_count,
        round(porosity_percent, 2),
        round(crack_percent, 2),
        round(health_score, 2),
        grade
    ]
}

df = pd.DataFrame(data)

df.to_excel("material_analysis.xlsx", index=False)
print("Reached graph section")

print("Excel file saved: material_analysis.xlsx")

print("Starting graph generation")
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt

diameters = [row[2] for row in particle_data]

plt.figure(figsize=(8,5))
plt.hist(diameters, bins=20)

plt.title("Particle Size Distribution")
plt.xlabel("Equivalent Diameter")
plt.ylabel("Frequency")

plt.savefig("particle_size_distribution.png")
plt.close()

print("Graph saved!")
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image

from reportlab.lib.styles import getSampleStyleSheet

pdf = SimpleDocTemplate("Material_Report.pdf")

styles = getSampleStyleSheet()

content = []

content.append(Paragraph("SEEING MATTER IN LAYERS REPORT", styles['Title']))
content.append(Spacer(1, 12))

content.append(Paragraph(f"Particles Found: {particle_count}", styles['Normal']))
content.append(Paragraph(f"Porosity (%): {porosity_percent:.2f}", styles['Normal']))
content.append(Paragraph(f"Crack Percentage (%): {crack_percent:.2f}", styles['Normal']))
content.append(Paragraph(f"Health Score: {health_score:.2f}", styles['Normal']))
content.append(Paragraph(f"Material Grade: {grade}", styles['Normal']))

content.append(Spacer(1, 20))

content.append(Image("dashboard_result.png", width=400, height=300))

pdf.build(content)

print("PDF Report Saved!")# AI-style Summary Generation

if porosity_percent < 10:
    porosity_comment = "low porosity"
elif porosity_percent < 30:
    porosity_comment = "moderate porosity"
else:
    porosity_comment = "high porosity"

if crack_percent < 5:
    crack_comment = "low crack density"
elif crack_percent < 15:
    crack_comment = "moderate crack density"
else:
    crack_comment = "high crack density"

if health_score > 80:
    recommendation = "excellent structural quality"
elif health_score > 60:
    recommendation = "good structural quality"
else:
    recommendation = "requires further inspection"

summary = f"""
AI MATERIAL ANALYSIS SUMMARY

The image analysis detected {particle_count} particles.

The material shows {porosity_comment} ({porosity_percent:.2f}%)
and {crack_comment} ({crack_percent:.2f}%).

The calculated health score is {health_score:.2f},
resulting in a material grade of {grade}.

Overall, the sample demonstrates {recommendation}.
"""

print(summary)
with open("ai_summary.txt", "w") as f:
    f.write(summary)