from django.urls import path
from django.views.generic import TemplateView

from . views import (user_signup, verify_user_email,
                        UserProfile, UserLoginView, IndexView,
                        ContactView, FaqView, contact_form_view,
                        referal_link_view, AboutView, UpgradeView,
                        BlogView, UpgradeView, upgrade_success_view,
                        withdraw_request_view, BlogDetailView, blog_like,
                        comment_proccess, forgot_pass, validate_password_reset_link,
                        reset_password
                        )
from django.contrib.auth import views as auth_view
from . ajax_views import forgot_pass_ajax, signup_ajax, login_ajax

app_name = "main"
urlpatterns=[
    path("", IndexView.as_view(), name="index"),
    path("about-us/", AboutView.as_view(), name="about"),
    path("contact-us/", ContactView.as_view(), name="contact"),
    path("contact-form/", contact_form_view, name="contact_form"),
    path("faq/", FaqView.as_view(), name="faq"),
    path("upgrade/", UpgradeView.as_view(), name="upgrade"),
    path("get_referal_link/", referal_link_view, name="referal_link"),
    path("login/", UserLoginView.as_view(), name="login"),
    path("ajaxlogin/", login_ajax, name="ajaxlogin"),
    path("logout/", auth_view.LogoutView.as_view(template_name = "main/user_logout.html"), name="logout"),
    path("signup/", user_signup, name="signup"),
    path("signupajax/", signup_ajax, name="signupajax"),
    path("withdraw-request/", withdraw_request_view, name="withdraw_request"),
    path('forum/<slug:slug>/', BlogDetailView.as_view(), name='blog-detail'),
    path("verify_email/<str:uidb64>/<str:token>", verify_user_email, name="verify"),
    path("refer/<str:refid>/", user_signup, name="referred_register"),
    path("forum/", BlogView.as_view(), name="blog"),
    path("upgrade_success/", upgrade_success_view, name="upgrade_success"),
    path("comment/", comment_proccess, name="comment"),
    # path("forgotpassword/", forgot_pass, name="forgot-password"),
    path("forgotpasswordajax/", forgot_pass_ajax, name="forgot-password"),
    path("reset-password/<int:pk>", reset_password, name="reset-password"),
    path("password-reset-validate/<str:uidb64>/<str:token>", validate_password_reset_link, name="password-reset-validate"),
    path("blog-like/", blog_like, name="like"),
    path("profile/<int:pk>/", UserProfile.as_view(), name="profile"),

]
