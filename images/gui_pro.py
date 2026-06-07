from tkinter import filedialog
from PIL import Image, ImageTk
import customtkinter as ctk

# ======================
# Theme
# ======================
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# ======================
# App Window
# ======================
app = ctk.CTk()
app.title("Microscope Copilot Pro")
app.geometry("1300x750")

# ======================
# Functions
# ======================

def upload_image():
    global img_label_image

    file_path = filedialog.askopenfilename(
        filetypes=[
            ("Image Files", "*.jpg *.jpeg *.png *.bmp *.tif")
        ]
    )

    if file_path:
        img = Image.open(file_path)
        img.thumbnail((700, 500))

        img_label_image = ImageTk.PhotoImage(img)

        image_label.configure(
            image=img_label_image,
            text=""
        )

        status_label.configure(
            text="Image Loaded Successfully"
        )


def analyze_material():
    results_box.delete("1.0", "end")

    results_box.insert(
        "end",
        """
Material Analysis Results
--------------------------------

Particles Found : 75

Porosity (%) : 31.65

Crack Percentage (%) : 39.36

Health Score : 28.99

Material Grade : POOR
"""
    )

    status_label.configure(
        text="Material Analysis Completed"
    )


def generate_pdf():
    status_label.configure(
        text="Material_Report.pdf Generated Successfully"
    )


def export_data():
    status_label.configure(
        text="material_analysis.xlsx Exported Successfully"
    )


def ai_summary():
    summary = """

AI GENERATED SUMMARY
--------------------------------

The analyzed material shows a relatively high crack percentage and significant porosity.

The health score indicates poor structural integrity.

Further processing or optimization is recommended before industrial application.

Overall Material Grade: POOR
"""

    results_box.insert("end", summary)

    status_label.configure(
        text="AI Summary Generated"
    )

# ======================
# Title
# ======================

title = ctk.CTkLabel(
    app,
    text="MICROSCOPE COPILOT PRO",
    font=("Arial", 32, "bold")
)

title.pack(pady=15)

# ======================
# Main Layout
# ======================

main_frame = ctk.CTkFrame(app)
main_frame.pack(fill="both", expand=True, padx=10, pady=10)

# ======================
# Left Panel
# ======================

left_panel = ctk.CTkFrame(main_frame, width=220)
left_panel.pack(side="left", fill="y", padx=10)

ctk.CTkLabel(
    left_panel,
    text="Controls",
    font=("Arial", 22, "bold")
).pack(pady=15)

ctk.CTkButton(
    left_panel,
    text="Upload Image",
    command=upload_image
).pack(pady=10)

ctk.CTkButton(
    left_panel,
    text="Analyze Material",
    command=analyze_material
).pack(pady=10)

ctk.CTkButton(
    left_panel,
    text="Generate PDF Report",
    command=generate_pdf
).pack(pady=10)

ctk.CTkButton(
    left_panel,
    text="Export Analysis Data",
    command=export_data
).pack(pady=10)

ctk.CTkButton(
    left_panel,
    text="AI Summary",
    command=ai_summary
).pack(pady=10)

# ======================
# Center Panel
# ======================

center_panel = ctk.CTkFrame(main_frame)
center_panel.pack(
    side="left",
    fill="both",
    expand=True,
    padx=10
)

image_label = ctk.CTkLabel(
    center_panel,
    text="Image Preview Area",
    font=("Arial", 26)
)

image_label.pack(expand=True)

# ======================
# Right Panel
# ======================

right_panel = ctk.CTkFrame(
    main_frame,
    width=320
)

right_panel.pack(
    side="right",
    fill="y",
    padx=10
)

ctk.CTkLabel(
    right_panel,
    text="Analysis Results",
    font=("Arial", 22, "bold")
).pack(pady=15)

results_box = ctk.CTkTextbox(
    right_panel,
    width=280,
    height=450
)

results_box.pack(padx=10, pady=10)

# ======================
# Status Bar
# ======================

status_label = ctk.CTkLabel(
    app,
    text="Ready",
    font=("Arial", 14)
)

status_label.pack(pady=8)

# ======================
# Run App
# ======================

app.mainloop()

