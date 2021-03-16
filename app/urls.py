from django.urls import path
from .views import CreateAPIView,UpdateAPIView,GetAPIView,DeleteAPIView

urlpatterns = [
    path("audiofile/create-api",CreateAPIView.as_view()),
    path('update/<str:audioFileType>/<int:audioFileID>',UpdateAPIView.as_view()),
    path('get/<str:audioFileType>/<int:audioFileID>',GetAPIView.as_view()),
    path('get/<str:audioFileType>',GetAPIView.as_view()),
    path('delete/<str:audioFileType>/<int:audioFileID>',DeleteAPIView.as_view()),
]