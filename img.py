from PIL import Image  # Import the Image module from PIL (Pillow) library
import face_recognition  # Import the face_recognition library
import os  # Import the os module for file and directory operations
import shutil  # Import the shutil module for file operations
import numpy as np  # Import the numpy library for numerical operations
import tkinter as tk  # Import the tkinter library for GUI
# Import specific modules from tkinter
from tkinter import filedialog, messagebox, ttk
from tkinter import font as tkfont  # Import the font module from tkinter
import threading  # Import the threading module for multi-threading

# Global variables
KNOWN_FACES_DIR = ""  # Directory for known faces
SORTED_DIR = ""  # Directory for sorted images
image_directory = ""  # Directory for images to process
processed_images = 0  # Counter for processed images
total_images = 0  # Total number of images to process

# Tkinter window setup
root = tk.Tk()  # Create the main window
root.title("Image Sorter")  # Set the window title
root.geometry("800x800")  # Set the window size
root.config(bg="#1e1e1e")  # Set the background color

# Set a custom font for the app
font_style = tkfont.Font(family="Helvetica", size=12, weight="bold")

# Frame for buttons and info display
frame = tk.Frame(root, bg="#2c2f3e", relief="solid", bd=2, padx=20, pady=20)
frame.pack(pady=20, padx=40, fill="x")

# Function to browse and select directory for known faces


def select_known_faces_dir():
    global KNOWN_FACES_DIR
    KNOWN_FACES_DIR = filedialog.askdirectory(
        title="Select Known Faces Directory")
    known_faces_dir_label.config(
        text=f"Known Faces Directory: {KNOWN_FACES_DIR}")
    check_button_state()  # Check if both directories are selected

# Function to browse and select directory for image sorting


def select_sorted_dir():
    global SORTED_DIR
    SORTED_DIR = filedialog.askdirectory(title="Select Sorted Directory")
    sorted_dir_label.config(text=f"Sorted Directory: {SORTED_DIR}")
    check_button_state()  # Check if both directories are selected

# Function to browse and select directory for images to process


def select_image_directory():
    global image_directory
    image_directory = filedialog.askdirectory(title="Select Image Directory")
    image_dir_label.config(text=f"Image Directory: {image_directory}")
    check_button_state()  # Check if both directories are selected

# Function to enable or disable the start sorting button based on directory selection


def check_button_state():
    if KNOWN_FACES_DIR and SORTED_DIR and image_directory:
        # Enable button if all directories are selected
        start_sorting_btn.config(state=tk.NORMAL)
    else:
        # Disable button if any directory is not selected
        start_sorting_btn.config(state=tk.DISABLED)

# Function to encode known faces


def encode_known_faces():
    known_face_encodings = []  # List to store face encodings
    known_face_names = []  # List to store face names

    if not KNOWN_FACES_DIR:
        messagebox.showerror("Error", "Please select a known faces directory.")
        return known_face_encodings, known_face_names

    for person_name in os.listdir(KNOWN_FACES_DIR):
        person_dir = os.path.join(KNOWN_FACES_DIR, person_name)

        if not os.path.isdir(person_dir):
            continue

        for image_name in os.listdir(person_dir):
            image_path = os.path.join(person_dir, image_name)

            try:
                img = Image.open(image_path).convert(
                    "RGB")  # Open and convert image to RGB
                img = np.array(img)  # Convert image to numpy array

                encodings = face_recognition.face_encodings(
                    img)  # Get face encodings

                if encodings:
                    known_face_encodings.append(
                        encodings[0])  # Add encoding to list
                    known_face_names.append(person_name)  # Add name to list

            except Exception as e:
                print(f"Error processing {image_name}: {e}")

    return known_face_encodings, known_face_names

# Function to process images and sort them


def process_images(known_face_encodings, known_face_names):
    global processed_images, total_images

    if not SORTED_DIR or not image_directory:
        messagebox.showerror(
            "Error", "Please select both image and sorted directories.")
        return

    if not os.path.exists(SORTED_DIR):
        # Create the sorted directory if it does not exist
        os.makedirs(SORTED_DIR)
        update_log_output(f"Created sorted directory: {SORTED_DIR}")

    image_filenames = os.listdir(image_directory)
    total_images = len(image_filenames)  # Get total number of images

    if not known_face_encodings:
        messagebox.showinfo(
            "Info", "No known faces found. Skipping image processing.")
        return

    processed_images = 0  # Reset processed images counter

    for filename in image_filenames:
        image_path = os.path.join(image_directory, filename)

        try:
            img = Image.open(image_path).convert(
                "RGB")  # Open and convert image to RGB
            img = np.array(img)  # Convert image to numpy array

            face_locations = face_recognition.face_locations(
                img)  # Get face locations
            face_encodings = face_recognition.face_encodings(
                img, face_locations)  # Get face encodings

            matched_names = []
            for face_encoding in face_encodings:
                matches = face_recognition.compare_faces(
                    known_face_encodings, face_encoding)  # Compare faces
                face_distance = face_recognition.face_distance(
                    known_face_encodings, face_encoding)  # Get face distance
                best_match_index = np.argmin(
                    face_distance)  # Get best match index

                if matches[best_match_index]:
                    # Get matched name
                    name = known_face_names[best_match_index]
                    matched_names.append(name)

            if not matched_names:
                no_known_faces_dir = os.path.join(SORTED_DIR, "NoKnownFaces")
                os.makedirs(no_known_faces_dir, exist_ok=True)
                destination_path = os.path.join(no_known_faces_dir, filename)
                # Move image to "NoKnownFaces" directory
                shutil.move(image_path, destination_path)
                continue

            for name in matched_names:
                destination_dir = os.path.join(SORTED_DIR, name)
                os.makedirs(destination_dir, exist_ok=True)

                destination_path = os.path.join(destination_dir, filename)
                # Copy image to matched name directory
                shutil.copy(image_path, destination_path)

        except Exception as e:
            print(f"Error processing image {filename}: {e}")

        processed_images += 1  # Update the processed image count
        processed_images_label.config(text=f"Processed Images: {
                                      processed_images}/{total_images}")

        update_log_output(f"Processed: {filename}")
        root.after(0, root.update_idletasks)  # Update GUI

    messagebox.showinfo("Sorting Completed", "Image sorting is completed!")
    start_sorting_btn.config(state=tk.NORMAL)

# Function to handle the "Start Sorting" button click


def start_sorting():
    known_face_encodings, known_face_names = encode_known_faces()
    if known_face_encodings:
        threading.Thread(target=process_images, args=(
            known_face_encodings, known_face_names), daemon=True).start()
        # Disable the button to prevent multiple clicks
        start_sorting_btn.config(state=tk.DISABLED)

# Update the log output in the text widget


def update_log_output(message):
    log_output.config(state=tk.NORMAL)  # Enable text widget for editing
    log_output.insert(tk.END, f"{message}\n")  # Insert the message at the end
    log_output.yview(tk.END)  # Scroll to the bottom
    log_output.config(state=tk.DISABLED)  # Disable editing again


# UI elements with advanced styling
select_known_faces_btn = tk.Button(frame, text="Select Known Faces Directory",
                                   command=select_known_faces_dir, font=font_style, bg="#4CAF50", fg="white", padx=10, pady=5)
select_known_faces_btn.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

select_sorted_btn = tk.Button(frame, text="Select Saving Directory", command=select_sorted_dir,
                              font=font_style, bg="#4CAF50", fg="white", padx=10, pady=5)
select_sorted_btn.grid(row=1, column=0, padx=5, pady=5, sticky="ew")

select_image_btn = tk.Button(frame, text="Select Image Directory", command=select_image_directory,
                             font=font_style, bg="#4CAF50", fg="white", padx=10, pady=5)
select_image_btn.grid(row=2, column=0, padx=5, pady=5, sticky="ew")

# Labels to display selected directories
known_faces_dir_label = tk.Label(frame, text="Known Faces Directory: Not Selected",
                                 font=font_style, bg="#2c2f3e", fg="white", anchor="w")
known_faces_dir_label.grid(row=0, column=1, padx=5, pady=5, sticky="w")

sorted_dir_label = tk.Label(frame, text="Saving Directory: Not Selected",
                            font=font_style, bg="#2c2f3e", fg="white", anchor="w")
sorted_dir_label.grid(row=1, column=1, padx=5, pady=5, sticky="w")

image_dir_label = tk.Label(frame, text="Images Directory: Not Selected",
                           font=font_style, bg="#2c2f3e", fg="white", anchor="w")
image_dir_label.grid(row=2, column=1, padx=5, pady=5, sticky="w")

# Processed Images label
processed_images_label = tk.Label(
    root, text="Processed Images: 0/0", font=font_style, bg="#1e1e1e", fg="white")
processed_images_label.pack(pady=10)

# Log Output (Terminal) area
log_output_label = tk.Label(
    root, text="Processing Log", font=font_style, bg="#1e1e1e", fg="white")
log_output_label.pack(pady=10)

log_output = tk.Text(root, height=15, width=90, font=font_style, wrap=tk.WORD,
                     bg="#2c2f3e", fg="white", bd=2, padx=10, pady=10, state=tk.DISABLED)
log_output.pack(pady=10)

# Start Sorting Button
start_sorting_btn = tk.Button(root, text="Start Sorting", command=start_sorting,
                              font=font_style, bg="#ff9800", fg="white", padx=10, pady=10, state=tk.DISABLED)
start_sorting_btn.pack(pady=20)

# Start the Tkinter main loop
root.mainloop()  # Run the main loop
