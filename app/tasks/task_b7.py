from PIL import Image

def execute_task_b7(image_path, output_path, size, quality=85):
    """
    Compresses or resizes an image and saves it to a new file.
    Args:
        image_path (str): Path to the input image file.
        output_path (str): Path to save the resized/compressed image.
        size (tuple): New size for the image (width, height).
        quality (int): Compression quality for JPEG images (default is 85).
    Returns:
        str: Success or error message.
    """
    try:
        img = Image.open(image_path)
        
        img_resized = img.resize(size)
        
        img_resized.save(output_path, quality=quality)

        return f"Task B7 completed successfully. Image saved to {output_path}."
    except Exception as e:
        return f"Error executing Task B7: {str(e)}"