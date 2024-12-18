from django.db import models


class ImageFrame(models.Model):
    """
    Model to store image frames along with their depth values.
    """
    depth = models.FloatField(unique=True, null=False, blank=False)
    image_data = models.BinaryField(null=False)  # Binary field to store image data

    def __str__(self):
        return f'ImageFrame(depth={self.depth})'