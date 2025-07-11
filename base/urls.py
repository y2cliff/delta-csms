from django.urls import path
from . import views, forms
from django.contrib.auth.views import (
    PasswordResetView, PasswordResetDoneView,
    PasswordResetConfirmView, PasswordResetCompleteView,
    PasswordChangeDoneView
)
from . import scaffolding
from utils import navigate


urlpatterns = [
    # MAIN
    path('', views.TemplateHomeView.as_view(), name="home"),
    path('login/',views.MyLoginView.as_view(),name='login'),
    path('logout/', views.logoutview, name='logout'),
    path('my-profile/', views.MyProfileView.as_view(), name="my-profile"),
    path('page-faq/', views.TemplateHomeView.as_view(template_name='pages-faq.html'), name="pages-faq"),
    path('icons-bootstrap/', views.TemplateHomeView.as_view(template_name='base/icons-bootstrap.html'), name="icons-bootstrap"),

    path('password-reset/', PasswordResetView.as_view(template_name='registration/password_reset_form.html'), name='password_reset'),
    path('password-reset/done/', PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password-reset-complete/', PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'), name='password_reset_complete'),
    path('password-change-done/', views.MyProfileView.as_view(), name='password_change_done'),

    path('next/<str:app_name>/<str:model_name>/<int:current_id>/', 
        navigate.next_record_view, name='next_record'),
    path('previous/<str:app_name>/<str:model_name>/<int:current_id>/', 
        navigate.previous_record_view, name='previous_record'),
    path('first/<str:app_name>/<str:model_name>/', navigate.first_record_view, name='first_record'), 
    path('last/<str:app_name>/<str:model_name>/', navigate.last_record_view, name='last_record'),
    path('toggle-follow/<str:app_name>/<str:model_name>/<int:current_id>/', navigate.toggle_follow_view, name='toggle_follow'),


    # path('password_update/<int:id>/', views.UserUpdateView.as_view(
    #         form_class=UserPasswordUpdateModelForm,
    #     ),
    #     name='userpassword_update'),
]

urlpatterns += scaffolding.MenuCrudManager().get_url_patterns()
urlpatterns += scaffolding.UserProfileCrudManager().get_url_patterns()
urlpatterns += scaffolding.UserProfileChildCrudManager().get_url_patterns()
urlpatterns += scaffolding.GroupProfileCrudManager().get_url_patterns()
urlpatterns += scaffolding.GroupProfileChildCrudManager().get_url_patterns()
# urlpatterns += scaffolding.UserMenuOrderCrudManager().get_url_patterns()
urlpatterns += scaffolding.DepartmentCrudManager().get_url_patterns()
