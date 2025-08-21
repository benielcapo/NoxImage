# NoxImage

NoxImage is a Python GUI application that allows users to **encrypt and decrypt images** using a simple XOR-based algorithm with a 4-part token. The project is designed to be user-friendly and uses `tkinter` for the interface.

---

## Table of Contents

1. [Overview](#overview)  
2. [Features](#features)  
3. [Requirements](#requirements)  
4. [Installation](#installation)  
5. [Usage](#usage)  
   - [Encrypting an Image](#encrypting-an-image)  
   - [Decrypting an Image](#decrypting-an-image)  
6. [How It Works](#how-it-works)  
7. [File Structure](#file-structure)  
8. [License](#license)

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

---
