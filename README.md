# Image Editor

A desktop image editing application developed with Python, Tkinter, and OpenCV.

## Features

- Load local image files
- Interactive image cropping with mouse
- Real-time preview of cropped image
- Image scaling functionality
- Save modified images
- Undo/Redo functionality
- Keyboard shortcuts support

## Requirements

- Python 3.7+
- OpenCV
- NumPy
- Pillow

## Installation

1. Clone or download this repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Run the application:
   ```bash
   python image_editor.py
   ```

2. Instructions:
   - Click "Open Image" to load an image
   - Use mouse drag on the left canvas to select crop area
   - Use the slider to adjust the scale of the cropped image
   - Click "Save" or use Ctrl+S to save the modified image
   - Use "Undo" and "Redo" buttons or Ctrl+Z/Ctrl+Y for edit history

## Keyboard Shortcuts

- Ctrl+S: Save image
- Ctrl+Z: Undo
- Ctrl+Y: Redo 