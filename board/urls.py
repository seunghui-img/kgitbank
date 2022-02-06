from django.urls import path
from . import views

app_name="board"

urlpatterns = [
    path('index/', views.index, name="index"),
    path('detail/<pk>', views.detail, name="detail"),
    path('create/', views.create, name="create"),
    path('modify/<pk>', views.modify, name="modify"),
    path('delete/<pk>', views.delete, name="delete"),

    path('creReply/<b_pk>/', views.creReply, name="creReply"),
    path('modReply/<b_pk>/', views.modReply, name="modReply"),
    path('delReply/<b_pk>/<pk>', views.delReply, name="delReply"),

    path('likey/<b_pk>', views.likey, name="likey"),
    path('unlikey/<b_pk>', views.unlikey, name="unlikey"),
]