import base64
import io
import os

from django.conf import settings
from django.http import JsonResponse
from PIL import Image
from rest_framework import status

from .models import ImageFrame
from .utils import apply_color_map_with_name, process_csv_and_store_images


def upload_csv(request):
    """
    Endpoint to process and upload a CSV file.
    """
    try:
        # Assuming the CSV file is located in the root directory for simplicity
        csv_file_path = os.path.join(settings.BASE_DIR, 'img.csv')

        if not os.path.isfile(csv_file_path):
            return JsonResponse({'error': f'File not found at {csv_file_path}'}, status=status.HTTP_404_NOT_FOUND)

        process_csv_and_store_images(csv_file_path)
        return JsonResponse({'message': 'CSV processed successfully and images saved.'})

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def get_images_by_depth_range(request, depth_min, depth_max):
    """
    Fetch and return all grayscale images within the specified depth range (inclusive),
    applying a color map dynamically before returning them as Base64-encoded strings.
    Supports dynamic color map selection through query parameters.
    """
    colormap_name = request.GET.get('colormap', 'viridis')  # Default to 'viridis'

    try:
        frames = ImageFrame.objects.filter(depth__gte=depth_min, depth__lte=depth_max)

        if not frames.exists():
            return JsonResponse({'error': 'No images found in this depth range.'}, status=status.HTTP_404_NOT_FOUND)

        response_images = []
        for frame in frames:
            # Load grayscale image from binary data
            grayscale_image = Image.open(io.BytesIO(frame.image_data))

            # Apply the selected color map dynamically
            color_mapped_image = apply_color_map_with_name(grayscale_image, colormap_name)

            # Save the color-mapped image to a buffer
            buffer = io.BytesIO()
            color_mapped_image.save(buffer, format="PNG")
            buffer.seek(0)

            # Convert binary to Base64 string
            base64_image = base64.b64encode(buffer.getvalue()).decode('utf-8')

            response_images.append({
                'depth': frame.depth,
                'image': base64_image  # Base64-encoded image
            })

        return JsonResponse({'images': response_images}, safe=False)

    except Exception as e:
        return JsonResponse({'error': f'An error occurred: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)