# Advanced Image Filter & Editing Application

## Description
This is a Python-based advanced image filter and editing application built using OpenCV and NumPy. It allows users to apply a variety of filters and effects to images, adjust brightness, contrast, and saturation, and perform basic image transformations such as flipping and rotating. The application supports undo and redo functionality, enabling users to experiment with different edits easily.

## Features
- Apply multiple filters including grayscale, sepia, blur, invert colors, edge detection, sketch, posterize, emboss, and sharpen.
- Adjust brightness, contrast, and saturation of images.
- Flip images horizontally or vertically.
- Rotate images by 90 degrees.
- Undo and redo changes.
- Reset image to original.
- Save edited images to a specified path.
- Side-by-side display of original and edited images for easy comparison.

## Installation

### Prerequisites
- Python 3.x
- OpenCV (`opencv-python`)
- NumPy

### Install dependencies
```bash
pip install opencv-python numpy
```

## Usage

1. Run the script:
```bash
python "import cv2.py"
```

2. When prompted, enter the path to the image you want to edit.

3. Use the menu options to apply filters, adjust image properties, undo/redo changes, reset, save, or exit.

4. The original and edited images will be displayed side-by-side in a window.

5. Press 'q' or choose the exit options to close the application.

## Supported Filters and Effects
- Grayscale
- Sepia
- Blur (adjustable intensity)
- Invert Colors
- Edge Detection
- Sketch Effect
- Posterize (adjustable intensity)
- Emboss
- Sharpen (adjustable intensity)
- Flip Horizontal
- Flip Vertical
- Rotate 90°
- Brightness and Contrast Adjustment
- Saturation Adjustment

## Notes
- Intensity values for some filters can be adjusted between 0.1 and 1.0.
- Brightness ranges from -100 to 100.
- Contrast ranges from 0.1 to 3.0.
- Saturation ranges from 0.0 to 3.0.

## License
This project is provided as-is without any warranty. Feel free to use and modify it for your own purposes.
