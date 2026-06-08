from flask import Flask, render_template, request
import os
import cv2

app = Flask(__name__)

UPLOAD_FOLDER = os.path.join("static", "uploads")
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


@app.route("/", methods=["GET", "POST"])
def home():

    image_path = None
    particle_count = None
    porosity = None
    crack_percentage = None
    health_score = None
    material_grade = None

    if request.method == "POST":

        file = request.files["image"]

        if file and file.filename != "":

            filepath = os.path.join(
                app.config["UPLOAD_FOLDER"],
                file.filename
            )

            file.save(filepath)

            img = cv2.imread(filepath)

            if img is not None:

                gray = cv2.cvtColor(
                    img,
                    cv2.COLOR_BGR2GRAY
                )

                # -------------------------
                # POROSITY
                # -------------------------
                _, pore_mask = cv2.threshold(
                    gray,
                    100,
                    255,
                    cv2.THRESH_BINARY_INV
                )

                total_pixels = gray.shape[0] * gray.shape[1]
                pore_pixels = cv2.countNonZero(pore_mask)

                porosity = round(
                    (pore_pixels / total_pixels) * 100,
                    2
                )

                # -------------------------
                # PARTICLE COUNT
                # -------------------------
                _, thresh = cv2.threshold(
                    gray,
                    120,
                    255,
                    cv2.THRESH_BINARY
                )

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

                # -------------------------
                # CRACK %
                # -------------------------
                crack_percentage = round(
                    porosity * 0.30,
                    2
                )

                # -------------------------
                # HEALTH SCORE
                # -------------------------
                health_score = round(
                    max(
                        0,
                        100 - porosity - crack_percentage
                    ),
                    2
                )

                # -------------------------
                # MATERIAL GRADE
                # -------------------------
                if health_score >= 90:
                    material_grade = "A"

                elif health_score >= 75:
                    material_grade = "B"

                elif health_score >= 60:
                    material_grade = "C"

                else:
                    material_grade = "D"

            image_path = file.filename

    return render_template(
        "index.html",
        image_path=image_path,
        particle_count=particle_count,
        porosity=porosity,
        crack_percentage=crack_percentage,
        health_score=health_score,
        material_grade=material_grade,
        dashboard_image="dashboard_result.png"
    )

import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
    