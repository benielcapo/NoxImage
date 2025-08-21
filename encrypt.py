import tkinter as tk
import random
import os
import numpy
from tkinter import filedialog, messagebox
from PIL import Image

ext_to_format = Image.registered_extensions()
formats = sorted(set(ext_to_format.values()))

def is_path_valid_image(path: str):
    return path.split(".")[-1].lower() in [f.lower() for f in formats]

def get_token_sequence():
    seq = ""
    for i in range(4):
        seq += str(random.randint(1, 10000)) + "."
    seq = seq[0:-1]
    print("returned " + seq)
    return seq

def divide_img(img):
    h, w = img.shape[:2]
    h_mid, w_mid = h // 2, w // 2
    top_left = img[0:h_mid, 0:w_mid]
    top_right = img[0:h_mid, w_mid:w]
    bottom_left = img[h_mid:h, 0:w_mid]
    bottom_right = img[h_mid:h, w_mid:w]
    return top_left, top_right, bottom_left, bottom_right

def reassemble_img(top_left, top_right, bottom_left, bottom_right):
    top = numpy.hstack((top_left, top_right))
    bottom = numpy.hstack((bottom_left, bottom_right))
    new_img_array = numpy.vstack((top, bottom))
    new_img_pil = Image.fromarray(new_img_array.astype(numpy.uint8))
    return new_img_pil

def encrypt_img(path, token):
    img = Image.open(path).convert("RGB")
    img_arr = numpy.array(img)
    first, second, third, fourth = map(int, token.split("."))
    top_left, top_right, bottom_left, bottom_right = divide_img(img_arr)
    rng = numpy.random.default_rng(first)
    top_left_xor = numpy.bitwise_xor(top_left, rng.integers(0, 256, top_left.shape, dtype=numpy.uint8))
    rng = numpy.random.default_rng(second)
    top_right_xor = numpy.bitwise_xor(top_right, rng.integers(0, 256, top_right.shape, dtype=numpy.uint8))
    rng = numpy.random.default_rng(third)
    bottom_left_xor = numpy.bitwise_xor(bottom_left, rng.integers(0, 256, bottom_left.shape, dtype=numpy.uint8))
    rng = numpy.random.default_rng(fourth)
    bottom_right_xor = numpy.bitwise_xor(bottom_right, rng.integers(0, 256, bottom_right.shape, dtype=numpy.uint8))
    return reassemble_img(top_left_xor, top_right_xor, bottom_left_xor, bottom_right_xor)

def create_project_dir(name):
    os.makedirs(name, exist_ok=True)

def save_token(token, dir_name):
    with open(dir_name + "\\token.tkn", "w+") as file:
        file.write(token)

def on_submit():
    file_path = filedialog.askopenfilename(
        title="Select a file",
        filetypes=[("All files", "*.*")]
    )
    if file_path:
        if is_path_valid_image(file_path):
            file_name = os.path.splitext(os.path.basename(file_path))[0]
            save_image_path = file_name + "\\" + os.path.basename(file_path)
            token = get_token_sequence()
            create_project_dir(file_name)
            save_token(token, file_name)
            encrypted_img = encrypt_img(file_path, token)
            encrypted_img.save(save_image_path)
            messagebox.showinfo("Success", f"Encrypted image saved as {save_image_path}")
        else:
            messagebox.showerror("Error", f"{file_path.split(".")[-1].lower()} is not a valid image extension!")
    else:
        messagebox.showerror("Error", f"{file_path} doesnt exist!")

root = tk.Tk()
root.title("Image encrypter")
root.geometry("300x150")

label = tk.Label(root, text="Click below to choose a file:")
label.pack(pady=10)

submit_button = tk.Button(root, text="Choose image and encrypt", command=on_submit)
submit_button.pack(pady=20)

root.mainloop()
