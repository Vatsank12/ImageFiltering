import cv2
import numpy as np

def apply_filter(filter_type, image, intensity=1.0):
    """
    Apply the specified filter to the image.
    intensity: float between 0 and 1 to control filter strength where applicable.
    """
    if filter_type == "grayscale":
        grayscale_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        return cv2.cvtColor(grayscale_image, cv2.COLOR_GRAY2BGR)
    elif filter_type == "sepia":
        kernel = np.array([[0.272, 0.534, 0.131],
                           [0.349, 0.686, 0.168],
                           [0.393, 0.769, 0.189]])
        sepia_image = cv2.transform(image, kernel)
        sepia_image = np.clip(sepia_image, 0, 255).astype(np.uint8)
        if intensity < 1.0:
            return cv2.addWeighted(image, 1 - intensity, sepia_image, intensity, 0)
        return sepia_image
    elif filter_type == "blur":
        ksize = int(15 * intensity)
        if ksize % 2 == 0:
            ksize += 1
        return cv2.GaussianBlur(image, (ksize, ksize), 0)
    elif filter_type == "invert":
        return cv2.bitwise_not(image)
    elif filter_type == "edges":
        edges = cv2.Canny(image, 100, 200)
        return cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
    elif filter_type == "sketch":
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        inverted_image = cv2.bitwise_not(gray_image)
        sketch = cv2.divide(gray_image, 255 - inverted_image, scale=256)
        return cv2.cvtColor(sketch, cv2.COLOR_GRAY2BGR)
    elif filter_type == "posterize":
        shift = int(64 * (1 - intensity))
        image = (image // (shift + 1)) * (shift + 1)
        return image
    elif filter_type == "emboss":
        kernel = np.array([[-2, -1, 0],
                           [-1,  1, 1],
                           [ 0,  1, 2]])
        return cv2.filter2D(image, -1, kernel)
    elif filter_type == "sharpen":
        kernel = np.array([[0, -1, 0],
                           [-1, 5, -1],
                           [0, -1, 0]])
        sharpened = cv2.filter2D(image, -1, kernel)
        if intensity < 1.0:
            return cv2.addWeighted(image, 1 - intensity, sharpened, intensity, 0)
        return sharpened
    elif filter_type == "flip_horizontal":
        return cv2.flip(image, 1)
    elif filter_type == "flip_vertical":
        return cv2.flip(image, 0)
    elif filter_type == "rotate":
        height, width = image.shape[:2]
        center = (width // 2, height // 2)
        matrix = cv2.getRotationMatrix2D(center, 90, 1.0)
        return cv2.warpAffine(image, matrix, (width, height))
    elif filter_type == "saturation":
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV).astype(np.float32)
        hsv[...,1] = np.clip(hsv[...,1] * intensity, 0, 255)
        hsv = hsv.astype(np.uint8)
        return cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
    else:
        return image

def adjust_brightness_contrast(image, brightness=0, contrast=1.0):
    """
    Adjust brightness and contrast of the image.
    brightness: int from -100 to 100
    contrast: float from 0.1 to 3.0
    """
    return cv2.convertScaleAbs(image, alpha=contrast, beta=brightness)

def resize_image(image, width=600):
    """
    Resize image maintaining aspect ratio.
    """
    aspect_ratio = image.shape[1] / image.shape[0]
    new_height = int(width / aspect_ratio)
    return cv2.resize(image, (width, new_height))

def get_int_input(prompt, min_val, max_val):
    """
    Get validated integer input from user within min and max.
    """
    while True:
        try:
            val = int(input(prompt))
            if val < min_val or val > max_val:
                print(f"Please enter a value between {min_val} and {max_val}.")
                continue
            return val
        except ValueError:
            print("Invalid input. Please enter an integer.")

def get_float_input(prompt, min_val, max_val):
    """
    Get validated float input from user within min and max.
    """
    while True:
        try:
            val = float(input(prompt))
            if val < min_val or val > max_val:
                print(f"Please enter a value between {min_val} and {max_val}.")
                continue
            return val
        except ValueError:
            print("Invalid input. Please enter a number.")

def image_editor():
    """
    Main image editor function with undo/redo and enhanced features.
    """
    print("Welcome to the Advanced Image Filter & Editing Application!")
    image_path = input("Enter the path to the image: ")
    image = cv2.imread(image_path)

    if image is None:
        print("Error: Could not load the image. Check the file path.")
        return

    original_image = image.copy()
    edited_image = image.copy()

    undo_stack = []
    redo_stack = []

    cv2.namedWindow("Image Editor (Original | Edited)", cv2.WINDOW_NORMAL)

    while True:
        resized_original = resize_image(original_image)
        resized_edited = resize_image(edited_image)

        combined = np.hstack((resized_original, resized_edited))
        cv2.imshow("Image Editor (Original | Edited)", combined)

        print("\nOptions:")
        print("1. Apply Grayscale Filter")
        print("2. Apply Sepia Filter")
        print("3. Apply Blur Filter")
        print("4. Invert Colors")
        print("5. Apply Edge Detection")
        print("6. Apply Sketch Effect")
        print("7. Apply Posterize Effect")
        print("8. Apply Emboss Effect")
        print("9. Apply Sharpen Effect")
        print("10. Flip Horizontally")
        print("11. Flip Vertically")
        print("12. Rotate 90°")
        print("13. Adjust Brightness and Contrast")
        print("14. Adjust Saturation")
        print("15. Undo Last Change")
        print("16. Redo Last Change")
        print("17. Reset to Original")
        print("18. Save and Exit")
        print("19. Exit without Saving")
        choice = input("Enter your choice: ")

        if choice in [str(i) for i in range(1, 14)] + ['14']:
            undo_stack.append(edited_image.copy())
            redo_stack.clear()

        if choice == '1':
            edited_image = apply_filter("grayscale", edited_image)
        elif choice == '2':
            edited_image = apply_filter("sepia", edited_image)
        elif choice == '3':
            intensity = get_float_input("Enter blur intensity (0.1 to 1.0): ", 0.1, 1.0)
            edited_image = apply_filter("blur", edited_image, intensity)
        elif choice == '4':
            edited_image = apply_filter("invert", edited_image)
        elif choice == '5':
            edited_image = apply_filter("edges", edited_image)
        elif choice == '6':
            edited_image = apply_filter("sketch", edited_image)
        elif choice == '7':
            intensity = get_float_input("Enter posterize intensity (0.1 to 1.0): ", 0.1, 1.0)
            edited_image = apply_filter("posterize", edited_image, intensity)
        elif choice == '8':
            edited_image = apply_filter("emboss", edited_image)
        elif choice == '9':
            intensity = get_float_input("Enter sharpen intensity (0.1 to 1.0): ", 0.1, 1.0)
            edited_image = apply_filter("sharpen", edited_image, intensity)
        elif choice == '10':
            edited_image = apply_filter("flip_horizontal", edited_image)
        elif choice == '11':
            edited_image = apply_filter("flip_vertical", edited_image)
        elif choice == '12':
            edited_image = apply_filter("rotate", edited_image)
        elif choice == '13':
            brightness = get_int_input("Enter brightness (-100 to 100): ", -100, 100)
            contrast = get_float_input("Enter contrast (0.1 to 3.0): ", 0.1, 3.0)
            edited_image = adjust_brightness_contrast(edited_image, brightness, contrast)
        elif choice == '14':
            saturation = get_float_input("Enter saturation intensity (0.0 to 3.0): ", 0.0, 3.0)
            edited_image = apply_filter("saturation", edited_image, saturation)
        elif choice == '15':
            if undo_stack:
                redo_stack.append(edited_image.copy())
                edited_image = undo_stack.pop()
            else:
                print("Nothing to undo.")
        elif choice == '16':
            if redo_stack:
                undo_stack.append(edited_image.copy())
                edited_image = redo_stack.pop()
            else:
                print("Nothing to redo.")
        elif choice == '17':
            undo_stack.append(edited_image.copy())
            redo_stack.clear()
            edited_image = original_image.copy()
        elif choice == '18':
            save_path = input("Enter the path to save the edited image: ")
            cv2.imwrite(save_path, edited_image)
            print("Image saved successfully!")
            break
        elif choice == '19':
            print("Exiting without saving.")
            break
        else:
            print("Invalid choice! Please try again.")

        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("Exiting...")
            break

    cv2.destroyAllWindows()

if __name__ == "__main__":
    image_editor()
