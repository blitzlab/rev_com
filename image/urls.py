from django.urls import path
from .views import (image_list_view, ImageCreateView, ImageDeleteView, image_detail,
                    get_countdown, image_view_proccess)

app_name = "image"
urlpatterns=[
    path("", image_list_view, name="images"),
    path("add-image", ImageCreateView.as_view(), name="add_image"),
    path("image-detail/<pk>", image_detail, name="image_detail"),
    path("delete-image/<pk>", ImageDeleteView.as_view(), name="image_delete"),
    path("countdown/", get_countdown, name="countdown"),
    path("image-proccess/", image_view_proccess, name="image_proccess"),

]
