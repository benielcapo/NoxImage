import tkinter as tk
from tkinter import filedialog, messagebox
import os
import numpy
from PIL import Image

ext_to_format = Image.registered_extensions()
formats = sorted(set(ext_to_format.values()))

def is_path_valid_image(path: str):
    return path.split(".")[-1].lower() in [f.lower() for f in formats]

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

def decrypt_img(path, token):
    img = Image.open(path).convert("RGB")
    img_arr = numpy.array(img)
    first, second, third, fourth = map(int, token.split("."))
    top_left, top_right, bottom_left, bottom_right = divide_img(img_arr)
    rng = numpy.random.default_rng(first)
    top_left_dec = numpy.bitwise_xor(top_left, rng.integers(0, 256, top_left.shape, dtype=numpy.uint8))
    rng = numpy.random.default_rng(second)
    top_right_dec = numpy.bitwise_xor(top_right, rng.integers(0, 256, top_right.shape, dtype=numpy.uint8))
    rng = numpy.random.default_rng(third)
    bottom_left_dec = numpy.bitwise_xor(bottom_left, rng.integers(0, 256, bottom_left.shape, dtype=numpy.uint8))
    rng = numpy.random.default_rng(fourth)
    bottom_right_dec = numpy.bitwise_xor(bottom_right, rng.integers(0, 256, bottom_right.shape, dtype=numpy.uint8))
    return reassemble_img(top_left_dec, top_right_dec, bottom_left_dec, bottom_right_dec)

def on_decrypt():
    file_path = filedialog.askopenfilename(
        title="Select encrypted image",
        filetypes=[("All files", "*.*")]
    )
    if not file_path:
        messagebox.showerror("Error", "No file selected!")
        return
    token_path = filedialog.askopenfilename(
        title="Select token file",
        filetypes=[("Token files", "*.tkn")]
    )
    if not token_path:
        messagebox.showerror("Error", "No token file selected!")
        return
    with open(token_path, "r") as f:
        token = f.read().strip()
    if is_path_valid_image(file_path):
        decrypted_img = decrypt_img(file_path, token)
        save_path = os.path.splitext(file_path)[0] + "_decrypted.png"
        decrypted_img.save(save_path)
        messagebox.showinfo("Success", f"Decrypted image saved as {save_path}")
    else:
        messagebox.showerror("Error", "Invalid image file!")

root = tk.Tk()
root.title("Image Decrypter")
root.geometry("300x150")
label = tk.Label(root, text="Click below to choose an encrypted file and token:")
label.pack(pady=10)
decrypt_button = tk.Button(root, text="Choose image and token to decrypt", command=on_decrypt)
decrypt_button.pack(pady=20)
root.mainloop()
