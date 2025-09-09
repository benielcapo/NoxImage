# NoxImage

NoxImage is a Python GUI application that allows users to **encrypt and decrypt images** using a simple XOR-based algorithm with a 4-part token. The project is designed to be user-friendly and uses `tkinter` for the interface.

---

## Overview

NoxImage provides a simple way to secure images by splitting them into four quadrants and applying XOR encryption using a randomly generated 4-part token. Each quadrant is encrypted independently to increase security.  

The same token is required to decrypt the image back to its original form.

---

## Features

- Encrypt any valid image format supported by Pillow (e.g., PNG, JPEG, BMP).  
- Decrypt encrypted images using the corresponding token.  
- Graphical user interface for easy interaction.  
- Automatically saves encrypted and decrypted images.  
- Generates and stores a token file for each encrypted image.
- Choose the token to encrypt the image, or leave blank to generate randomly.

---
