from django.urls import path
from .views import add_post, delete_post
from .scaffolding import PostCrudManager
from base.views import TemplateHomeView

app_name = 'comment'

urlpatterns = [
    path('add-for/<app_label>/<model_name>/<int:pk>/',add_post,name="add"),
    path('delete/<int:post_pk>/', delete_post, name="delete"),
    path('', TemplateHomeView.as_view(template_name='comment/comment_home.html'),name='home'),
]

urlpatterns += PostCrudManager().get_url_patterns()


