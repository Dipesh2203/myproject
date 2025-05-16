from django.urls import path
from . import views
from .views import *

urlpatterns = [
    # Home
    path('', views.home, name="home"),

    # Notes
    path('notes', views.notes, name="notes"),
    path('notes/edit/<int:pk>/', views.edit_note, name='edit_note'),
    path('delete_note/<int:pk>', views.delete_note, name="delete-note"),
    path('notes_detail/<int:pk>', views.NotesDetailView.as_view(), name="notes-detail"),

    # Homework
    path('homework', views.homework, name="homework"),
    path('homework/edit/<int:pk>/', views.edit_homework, name='edit_homework'),
    path('update_homework/<int:pk>', views.update_homework, name="update-homework"),
    path('delete_homework/<int:pk>', views.delete_homework, name="delete-homework"),

    # Todo
    path('todo', views.todo, name="todo"),
    path('todo/edit/<int:pk>/', views.edit_todo, name='edit_todo'),
    path('update_todo/<int:pk>', views.update_todo, name="update-todo"),
    path('delete_todo/<int:pk>', views.delete_todo, name="delete-todo"),

    # Group Homework
    path('group/<int:pk>/grouphomework/', views.group_homework, name='group_homework'),
    path('group/<int:group_pk>/delete_homework/<int:homework_pk>/', views.delete_group_homework, name="delete-group-homework"),
    path('group/<int:group_pk>/edit/<int:homework_pk>/', views.edit_group_homework, name='edit_group_homework'),

    # Ebooks
    path('ebooks', views.ebooks, name="ebook"),
    path('ebooks/edit/<int:pk>/', views.edit_ebook, name='edit_ebook'),
    path('delete_ebook/<int:pk>', views.delete_ebook, name="delete-ebook"),

    # Groups
    path('groups/create/', create_group, name='create_group'),
    path('groups/<int:pk>/', group_detail, name='group_detail'),
    
    # Youtube
    path('youtube', views.youtube, name="youtube"),

    # Dictionary
    path('dictionary', views.dictionary, name="dictionary"),

    # Wikipedia
    path('wiki', views.wiki, name="wiki"),

    # Conversion
    path('conversion', views.conversion, name="conversion"),

    
]



# from django.urls import path
# from . import views
# # from .views import group_study_list,create_group,group_detail
# from .views import *


# urlpatterns = [
#     path('', views.home,name="home"),
#     #path('context in views',views.function,name to use in templates)  

#     path('notes', views.notes,name="notes"),
#     path('notes/edit/<int:pk>/', views.edit_note, name='edit_note'),
#     path('delete_note/<int:pk>', views.delete_note,name="delete-note"),
#     path('notes_detail/<int:pk>', views.NotesDetailView.as_view(),name="notes-detail"),

#     path('homework', views.homework,name="homework"),
#     path('homework/edit/<int:pk>/', views.edit_homework, name='edit_homework'),
#     path('update_homework/<int:pk>', views.update_homework,name="update-homework"),
#     path('delete_homework/<int:pk>', views.delete_homework,name="delete-homework"),
    
#     path('todo', views.todo,name="todo"),
#     path('todo/edit/<int:pk>/', views.edit_todo, name='edit_todo'),
#     path('update_todo/<int:pk>', views.update_todo,name="update-todo"), 
#     path('delete_todo/<int:pk>', views.delete_todo,name="delete-todo"),

#     path('youtube', views.youtube,name="youtube"),
#     # path('books', views.books,name="books"),
#     path('dictionary', views.dictionary,name="dictionary"),
#     path('wiki', views.wiki,name="wiki"),
#     path('conversion', views.conversion,name="conversion"),

#     path('ebooks', views.ebooks,name="ebook"),
#     path('ebooks/edit/<int:pk>/', views.edit_ebook, name='edit_ebook'),
#     path('delete_ebook/<int:pk>', views.delete_ebook,name="delete-ebook"),

#     path('groups/create/',create_group,name='create_group'),
#     path('groups/<int:pk>/',group_detail,name='group_detail'),

#     path('group/<int:pk>/grouphomework/', views.group_homework, name='group_homework'),
#     path('group/<int:group_pk>/delete_homework/<int:homework_pk>/', views.delete_group_homework, name="delete-group-homework"),
#     path('group/<int:group_pk>/edit/<int:homework_pk>/', views.edit_group_homework, name='edit_group_homework'),
    
# ]
# # group/13/delete_group_homework