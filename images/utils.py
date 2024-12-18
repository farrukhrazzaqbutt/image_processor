import io

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from PIL import Image

from .models import ImageFrame


def apply_color_map_with_name(image, colormap_name):
    """
    Apply a specified color map to a grayscale image.
    """
    grayscale_array = np.array(image)
    colormap = plt.get_cmap(colormap_name)  # Dynamically select colormap
    colored_array = colormap(grayscale_array / 255.0)[:, :, :3]  # Normalize and remove alpha

    return Image.fromarray((colored_array * 255).astype(np.uint8))


def process_csv_and_store_images(csv_path):
    """
    Reads the CSV file, generates images, resizes them to 150-pixel width,
    applies color mapping, and saves them in the database as binary data.
    """
    data = pd.read_csv(csv_path)
    data = data.dropna(subset=['depth'])  # Remove rows with missing depth
    data['depth'] = pd.to_numeric(data['depth'], errors='coerce').dropna()

    expected_width = 200  # Original width of the image

    for _, row in data.iterrows():
        depth = float(row['depth'])

        try:
            # Extract pixel data
            pixels = row.drop('depth').fillna(0).clip(0, 255).astype(np.uint8).values

            # Validate pixel data
            if len(pixels) != expected_width:
                print(f'Invalid pixel data for depth {depth}: {len(pixels)} pixels found')
                continue

            height = 1  # Single row of pixels
            image = Image.fromarray(pixels.reshape((height, expected_width)), mode='L')  # Grayscale

            # Resize width to 150 while keeping aspect ratio
            # new_height = int((150 / expected_width) * height) or 1  # Ensure new height is at least 1
            new_height = 150
            image_resized = image.resize((150, new_height))

            # # Apply color mapping
            # image_colored = apply_color_map(image_resized)

            # Save the image as binary data
            buffer = io.BytesIO()
            image_resized.save(buffer, format='PNG')
            buffer.seek(0)
            binary_image_data = buffer.getvalue()

            # Save the binary data in the database
            ImageFrame.objects.create(depth=depth, image_data=binary_image_data)

        except Exception as e:
            print(f'Error processing depth {depth}: {e}')

    print('All images have been saved successfully.')
