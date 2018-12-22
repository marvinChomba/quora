from django.test import TestCase
from .models import Post,Category
from .forms import PostForm
from django.utils import timezone
from django.core.urlresolvers import reverse,resolve
from . import views
# Create your tests here.

"""
#####################################
VIEWS TESTS
#####################################
"""

class ViewsTestCase(TestCase):

    def test_index_view(self):
        url = reverse("index")
        response = self.client.get(url)
        return self.assertTrue(response.status_code == 200)

    def test_add_post_view(self):
        url = reverse("new_post")
        response = self.client.get(url)
        return self.assertTrue(response.status_code == 200)

    def test_index_url_resolves_index_view(self):
        view = resolve("/")
        self.assertEquals(view.func,views.index)

    def test_add_post_url_resolves_add_post_view(self):
        view = resolve("/add/post/")
        self.assertEquals(view.func,views.add_post)


"""
#####################################
FORMS TESTS
#####################################
"""

class FormsTestCase(TestCase):
    def test_valid_form(self):
        new_category = Category.objects.create(name = "Tech")
        new_post = Post.objects.create(title="Hye", content="There", category=new_category)
        data = {"title":new_post.title, "content":new_post.content,"category":new_post.category}
        form = PostForm(data = data)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        new_category = Category.objects.create(name="Tech")
        new_post = Post.objects.create(title="Hye", content="", category=new_category)
        data = {"title": new_post.title, "content": new_post.content,"category": new_post.category}
        form = PostForm(data=data)
        self.assertFalse(form.is_valid())
