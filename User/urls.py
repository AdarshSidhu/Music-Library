from django.conf import settings
from django.contrib.staticfiles.urls import static
from django.urls import path
from django.contrib.auth import views as auth_views
from .views import signup, login_view, home, AddMusic, add_music_to_folder, CreateFolder, folder_detail, \
    FolderListView, add_to_favorites, remove_from_favorites, Musicupdate, MusicDelete, Musiclist, Folderdelete,\
favorites

urlpatterns = [

                  path('home/', home, name='home'),
                  path('signup/', signup, name='signup'),
                  path('login/', login_view, name='login'),
                  path(r'logout/', auth_views.LogoutView.as_view(), name='logout'),
                  path('addtrack/', AddMusic.as_view(), name='addtrack'),
                  path('create_folder/', CreateFolder.as_view(), name='create_folder'),
                  path('add_music_to_folder/<int:folder_id>/', add_music_to_folder,
                       name='add_music_to_folder'),
                  path('folders/<int:folder_id>/', folder_detail, name='folder_detail'),
                  path('folder_list/', FolderListView.as_view(), name='folder_list'),
                  path('add-to-favorites/<int:track_id>/', add_to_favorites, name='add_to_favorites'),
                  path('remove-from-favorites/<int:track_id>/', remove_from_favorites, name='remove_from_favorites'),
                  path('musicdelete/(?p<pk>[0-9]+)', MusicDelete.as_view(), name='musicdelete'),
                  path('musicupdate/(?p<pk>[0-9]+)', Musicupdate.as_view(), name='musicupdate'),

                  path('musiclist/', Musiclist.as_view(), name='musiclist'),
                  path('folderdelete/(?p<pk>[0-9]+)', Folderdelete.as_view(), name='folderdelete'),
                  path('favorites/', favorites, name='favorites'),

              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
