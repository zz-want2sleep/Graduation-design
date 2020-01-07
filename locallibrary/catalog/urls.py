from django.urls import re_path
from django.urls import path
from catalog import views
app_name = 'catalog'
urlpatterns = [
    path('', views.index, name='index'),
    path('books/', views.BookListView.as_view(), name='books'),
    path('book/<int:pk>', views.BookDetailView.as_view(), name='book-detail'),
    path('authors/', views.AuthorListView.as_view(), name="authors"),
    path('author/<int:pk>', views.AuthorDetailView.as_view(), name="author-detail"),
    path('authors/s/<str:name>',
         views.AuthorListView1.as_view(), name="author_filter"),
    path('books/s/<str:name>', views.BookListView1.as_view(), name="book_filter"),
    # bulk create user
    path('addusers/', views.addusers, name='addusers'),
    # bulk delete user
    path('deleteusers/', views.deleteusers, name='deleteusers'),

    # path('addusers1/', views.addusers1, name='addusers1'),
    path('group/', views.group, name="group"),

]
# Borrower URLConfig
urlpatterns += [
    path('mybooks/', views.LoanedBooksByUserListView.as_view(), name='my-borrowed'),
    path('mybooks/s/<str:name>',
         views.LoanedBooksByUserListView1.as_view(), name="mybook_filter"),
    path(r'borrowed/', views.LoanedBooksAllListView.as_view(), name='all-borrowed'),
    path(r'borrowed/s/<str:name>',
         views.LoanedBooksAllListView1.as_view(), name="mybook_filter"),
]

# renewal url setting

urlpatterns += [
    path('book/<uuid:pk>/renew/', views.renew_book_librarian,
         name='renew-book-librarian'),
]

# sending return back books email
urlpatterns += [
    path('send_email/<str:names>/', views.sendEmail, name='send_email'),
]

# setting author edit
urlpatterns += [
    path('author/create/', views.AuthorCreate.as_view(), name='author_create'),
    path('author/<int:pk>/update/',
         views.AuthorUpdate.as_view(), name='author_update'),
    path('author/<int:pk>/delete/',
         views.AuthorDelete.as_view(), name='author_delete'),
]
# setting book edit
urlpatterns += [
    path('book/create/', views.BookCreate.as_view(), name='book_create'),
    path('book/<int:pk>/update/', views.BookUpdate.as_view(), name='book_update'),
    path('book/<int:pk>/delete/', views.BookDelete.as_view(), name="book_delete")
]


# setting popup to add author
urlpatterns += [
    path(r'p1/', views.p1, name="popup"),
]

# setting update user password
urlpatterns += [
    re_path(r'password-change/$', views.PasswordChangeView.as_view(), {
        'template_name': "catalog/password_change_form.html",
        'post_change_redirect': 'registration/password-change-done'}, name='password_change'),
    re_path(r'password-change-done/$', views.PasswordChangeDoneView.as_view(), {
        'template_name': "catalog/password_change_done.html"}, name='password_change_done'),
]
# setting user profile
urlpatterns += [
    path('user_profile/<int:pk>/',
         views.UserDetailView.as_view(), name="user_profile"),
    path('user_form/<int:pk>/', views.UserUpdate.as_view(), name="user_update")
]

# update  borrower in bookinstance and appointment
urlpatterns += [
    path('rent_out/<uuid:id>/<int:pk>/',
         views.rent_out, name="rent_out"),
    path('appoint_ment/<int:pk>/<uuid:id>/<int:pk1>/',
         views.appointmentBook, name="appointment"),
    path('my_appointment/', views.AppointmentByUserListView.as_view(),
         name='my-appointment'),
    path('my_appointment/s/<str:name>',
         views.AppointmentByUserListView1.as_view(), name="myappointment_filter"),
    path('appointment/', views.AppointmentAllListView.as_view(),
         name='all-appointment'),
    path('appointment/s/<str:name>',
         views.AppointmentAllListView1.as_view(), name="appointment_filter"),
]
# History recoder
urlpatterns += [
    path('my_history/', views.HistoryListView.as_view(), name="my_history"),
    path('delete_history', views.deleteHistory, name="deletehistory")
]
# Genre search
urlpatterns += [
    path('genre/<str:name>', views.genre_books, name="genre-books"),
    path('genre/<str:name>/s/<str:name1>',
         views.genre_books1, name="genre-books1"),
]
# bulk create bookinstace
urlpatterns += [
    path('create/bookinstance/<int:pk>',
         views.BulkCreateBookinstance, name="bulkcreatebookinstance"),
]
# one user login
urlpatterns += [
    path('isthatone/',
         views.is_thatone, name="isthatone"),
]
# statistical state统计
urlpatterns += [
    path('statistical/', views.statistical, name="statistical")
]

# returned book
urlpatterns += [
    path(r'returned/<uuid:id>/<path:next>/',
         views.returned, name="returnedbook")
]

# captcha image change
urlpatterns += [
    path(r'loginCaptcha/', views.loginCaptcha, name="captcha")
]
# jquery user query
urlpatterns += [
    path(r'userQuery/', views.userQuery, name="userQuery")
]
