"""App notes urls"""
from django.urls import path

from notes import api_views

urlpatterns = [
    path(
        'notes/', 
        api_views.NotesApiView.as_view(),
        name='notes-notes',
    ),
    path(
        'notes/<int:id>', 
        api_views.NotesApiView.as_view(),
        name='notes-note',
    ),
    path(
        'notes/<int:id>/share', 
        api_views.ShareNoteApiView.as_view(),
        name='notes-share',
    ),
    path(
        'search/<str:query>', 
        api_views.SearchNoteApiView.as_view(),
        name='notes-search',
    ),
]
