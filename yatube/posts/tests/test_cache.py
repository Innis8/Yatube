# from time import sleep
from datetime import datetime
from django.urls import reverse
from django.core.cache import cache
from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from posts.models import Post

User = get_user_model()


class CacheTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.author = User.objects.create_user(username='author')
        cls.authorized_author = Client()
        cls.authorized_author.force_login(cls.author)

        cls.post = Post.objects.create(
            author=cls.author,
            pub_date=datetime.now(),
            text='1 Тестовый пост 1',
        )

    def test_cache_index(self):
        """
        Тест для проверки кеширования главной страницы
        """
        response_bfr = self.authorized_author.get(reverse('posts:index'))
        post2 = Post.objects.create(text='2 тест пост 2', author=self.author)
        # sleep(20)
        response_aft = self.authorized_author.get(reverse('posts:index'))
        self.assertEqual(len(response_aft.context['page_obj']), 2,)

        Post.objects.filter(id=post2.id).delete()
        response_aft_del = self.authorized_author.get(reverse('posts:index'))
        self.assertEqual(response_aft.content, response_aft_del.content)

        cache.clear()
        response_aft_clr = self.authorized_author.get(reverse('posts:index'))
        self.assertEqual(len(response_aft_clr.context['page_obj']), 1,)
        self.assertEqual(
            response_aft_clr.context['paginator'].count,
            response_bfr.context['paginator'].count)
