from django.urls import path
from . import views

urlpatterns = [
    path('messageRoom/<str:room_id>', views.messageRoom, name="messageRoom"),
    path('createMessager/<int:receiver_id>/<int:ser_req_id>', views.createMessager, name="createMessager"),
    
    path('AddFavorite/<int:receiver_id>', views.AddFavorite, name="AddFavorite"),
    path('AddDeleteFavorite/<int:receiver_id>', views.AddDeleteFavorite, name="AddDeleteFavorite"),
    path('BlockUserMessenger/<int:receiver_id>', views.BlockUserMessenger, name="BlockUserMessenger"),
    
    path('DeleteFavorite/<int:fav_id>', views.DeleteFavorite, name="DeleteFavorite"),
    path('DeleteBlockUser/<int:block_id>', views.DeleteBlockUser, name="DeleteBlockUser"),

    path('SendFiles/<str:room_id>', views.SendFiles, name='MessagerSendFiles'),
    path('DirectionMap/', views.DirectionMap, name='DirectionMap'),
]