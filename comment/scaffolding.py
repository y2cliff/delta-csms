from base.scaffolding import CrudManager

from .forms import PostForm
from .models import Post
from .tables import PostTable
from .filters import PostFilter


class PostCrudManager(CrudManager):
    form_class = PostForm
    model = Post
    module = 'comment'
    prefix = 'post'
    table_class = PostTable
