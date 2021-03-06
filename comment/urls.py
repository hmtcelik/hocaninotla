from django.urls import path
from . import views
from . import models

#django auth views for password things
from django.contrib.auth import views as auth_views


app_name = 'comment'

urlpatterns = [
    path('', views.HomeView.as_view(), name = 'home'),
    path('university/faculty/depart/doctor/<int:pk>/', views.CommentView.as_view(), name='comment'),
    path("search/", views.searchbar, name="searchbar"),
    path("register/", views.register_request, name="register"),
    path("login/", views.login_request, name="login"),
    path("logout", views.logout_request, name= "logout"),
    
    #comment urls
    path("createcomment/<int:doctor_id>/", views.CommentCreate.as_view(), name = 'createcomment'),
    path("editcomment/<int:doctor_id>/<int:comment_id>/", views.commenteditview, name = 'editcomment'),
    path("deletecomment/<int:doctor_id>/<int:comment_id>/", views.commentdeleteview, name = 'deletecomment'),
    path("answercomment/<int:doctor_id>/<int:comment_id>/", views.CommentAnswerView.as_view(), name = 'commentanswer'),
    path("likecomment/<int:doctor_id>/<int:comment_id>/", views.likeview, name="likecomment"),
    path("dislikecomment/<int:doctor_id>/<int:comment_id>/", views.dislikeview, name="dislikecomment"),
    path("reportcomment/<int:doctor_id>/<int:comment_id>/", views.ReportCommentView.as_view(), name='reportcomment'),
    
    #my account
    path("myaccount/", views.AccountView.as_view(), name="account"),
    path("myaccount/mycomments", views.MyCommentsView.as_view(), name="mycomments"),
    
    #password change (in account page)
    path("changepassword/", views.PasswordsChangeView.as_view(), name='changepassword'),
    path("password_succes/",views.passwordsuccesview, name='changedpassword'),
    
    #password reset (in login page)
    path("resetpassword/", views.password_reset_request, name="password_reset"),
    path("resetpassword/done",views.My_PasswordResetDoneView.as_view(), name="password_reset_done"),
    path("resetpassword/<uidb64>/<token>/", views.My_PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path("resetpassword/complete",views.My_PasswordResetCompleteView.as_view(), name="password_reset_complete"),
    
    #other pages
    path("adddoctor", views.AddDoctorView.as_view(), name="adddoctor"),
    path("contact/", views.ContactView.as_view(), name='contact'),
    path("requestform/", views.RequestFormView.as_view(), name='requestform'),

    #email verification
    path("activate-user/<uidb64>/<token>/", views.activate_user, name='activate'),
    path("resend_verif_email/", views.resend_email, name="resend_email")
    
]
