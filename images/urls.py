from django.urls import path, register_converter
from images import views
from .converters import FloatConverter

# Register custom float converter
register_converter(FloatConverter, 'float')

urlpatterns = [
    path('upload-csv/', views.upload_csv, name='upload_csv'),
    path('get-images/<float:depth_min>/<float:depth_max>/', 
         views.get_images_by_depth_range, name='get_images_by_depth_range'),
]
