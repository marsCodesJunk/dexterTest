from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView
urlpatterns = [
    path('', views.homepage, name='home'),  # Home page
    path('about/', views.about_us, name='about'),  # About page
    path('contact/', views.contact_us, name='contact'),  # Contact page
    path('text/', views.text,name='text'),
    path('websiteScanner/', views.websiteScanner,name='website'),
    path('Login/', views.Login,name='Login'),
    path('SignUp/', views.SignUp,name='SignUp'),
    path('ForgotPassword/', views.ForgotPassword,name='ForgotPassword'),
    path('AccDel/', views.AccDel,name='AccDel'),
    path('PassUpd/', views.PassUpd,name='PassUpd'),
    path('emailsent/', views.emailsent,name='emailsent'),
    path('ResetPassword/', views.ResetPassword,name='ResetPassword'),
    path('welcome/', views.welcome,name='welcome'),
    path('webResult/', views.webResult, name='webResult'),
    path('result/', views.text_result, name='TextResult'),
    path('setings/', views.account_settings, name='setings'),
    path('textScanner/', views.textScanner, name='textScanner'),
    path('Verify_OTP/', views.Verify_OTP, name='Verify_OTP'),
    path('Resend_OTP/', views.Resend_OTP, name='Resend_OTP'),
    path('extension/', views.extension_view, name='extension_view'),
    path('logout/', LogoutView.as_view(next_page='/Login/'), name='logout'),
     path('homepage/', views.homepage, name='homepage'),  # Add this
]
