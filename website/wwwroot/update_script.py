import os
import json
from PIL import Image
from PIL.ExifTags import TAGS
from datetime import datetime
import sys

# This helper function remains unchanged.
def get_image_date(image_path):
    """Extracts the creation date from image EXIF data."""
    try:
        image = Image.open(image_path)
        exif_data = image.getexif()
        if exif_data:
            for tag_id in exif_data:
                tag = TAGS.get(tag_id, tag_id)
                data = exif_data.get(tag_id)
                # The 'DateTimeOriginal' tag is often more accurate than 'DateTime'
                if tag in ("DateTime", "DateTimeOriginal"):
                    date_str = data
                    try:
                        return datetime.strptime(date_str, '%Y:%m:%d %H:%M:%S')
                    except (ValueError, TypeError):
                        pass  # Handle different date formats or data types if needed
    except (FileNotFoundError, OSError, AttributeError) as e:
        # It's good practice to know why it failed.
        # print(f"Warning: Could not read EXIF data from {image_path}. Reason: {e}", file=sys.stderr)
        pass
    # Default to a very old date if no EXIF data is found to ensure it sorts last.
    return datetime.min

# --- NEW CORE FUNCTION ---
def process_folder(folder_path):
    """
    Scans a folder, pairs original images with their 'resized_' counterparts,
    extracts metadata, and returns a list of data dictionaries.
    This function is case-insensitive when matching but preserves original capitalization.
    """
    try:
        all_files = os.listdir(folder_path)
    except FileNotFoundError:
        print(f"Error: Folder not found at '{folder_path}'", file=sys.stderr)
        return []

    image_extensions = ('.png', '.jpg', '.jpeg', '.gif', '.bmp')
    originals = {}
    resized_map = {}

    # 1. First, categorize all files into originals and a resized map
    for filename in all_files:
        lower_filename = filename.lower()
        if not lower_filename.endswith(image_extensions):
            continue  # Skip non-image files

        if lower_filename.startswith('resized_'):
            # Create a map from the original's expected lower-case name to the
            # actual, case-preserved resized filename.
            # e.g., 'image.jpg' -> 'resized_Image.JPG'
            base_name = lower_filename[len('resized_'):]
            resized_map[base_name] = filename
        else:
            # Store the original's actual, case-preserved filename.
            # e.g., 'image.jpg' -> 'Image.JPG'
            originals[lower_filename] = filename

    # 2. Now, build the final data structure by pairing them up
    processed_images = []
    for lower_name, original_filename in originals.items():
        
        # Find the matching resized file from our map
        resized_filename = resized_map.get(lower_name)

        if not resized_filename:
            print(
                f"Warning: No corresponding 'resized_' file found for '{original_filename}' in '{folder_path}'. Skipping.",
                file=sys.stderr
            )
            continue
            
        # Use os.path.join to create the system path, then format for the web
        full_image_path = os.path.join(folder_path, original_filename).replace(os.sep, '/')
        thumb_path = os.path.join(folder_path, resized_filename).replace(os.sep, '/')
        
        # Get the date from the original full-size image
        # We need the local system path for PIL to open the file
        date = get_image_date(os.path.join(folder_path, original_filename))

        processed_images.append({
            'thumb': thumb_path,
            'image': thumb_path,  # 'image' and 'thumb' point to the same resized file
            'big': full_image_path,
            'date': date # Store date for sorting
        })
        
    return processed_images


def output_javascript_literal(data_list):
    """Combines data and prints it as a JavaScript object literal string."""
    print("var data = [")

    # The data_list is already sorted and contains all the correct path strings
    object_strings = [
        f"    {{thumb: '{item['thumb']}', image: '{item['image']}', big: '{item['big']}'}}"
        for item in data_list
    ]

    print(",\n".join(object_strings))

    print("];")


if __name__ == "__main__":
    irl_folder = 'pics/irl'
    vrc_folder = 'pics/vrc'

    # Process each folder to get a list of dictionaries
    irl_data = process_folder(irl_folder)
    vrc_data = process_folder(vrc_folder)

    # Combine the data from both folders
    combined_data = irl_data + vrc_data

    # Sort the combined list by the 'date' key we stored in each dictionary
    combined_data.sort(key=lambda x: x['date'], reverse=True) # Sort newest first

    # Generate the final JavaScript output
    output_javascript_literal(combined_data)