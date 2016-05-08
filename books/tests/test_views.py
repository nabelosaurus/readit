from django.core.urlresolvers import resolve, reverse
from django.test import TestCase
from books.factories import AuthorFactory, BookFactory, UserFactory, ReviewFactory
from books.models import Book
from books.views import list_books, ReviewList

# Create your tests here.
class TestListBooks(TestCase):
    def test_list_books_url(self):
        url = resolve('/')
        self.assertEquals(url.func, list_books)
        self.assertEquals(url.args, ())
        self.assertEquals(url.view_name, 'books')
        self.assertEquals(url.url_name, 'books')

    def test_list_books_template(self):
        response = self.client.get(reverse(list_books))
        self.assertTemplateUsed(response, 'list.html')

    def test_list_books_returns_books_with_reviews(self):
        author = AuthorFactory()
        books_with_reviews = ReviewFactory.create_batch(2, authors=[author,])
        books_without_reviews = BookFactory.create_batch(4, authors=[author,])

        response = self.client.get(reverse(list_books))
        books = list(response.context['books'])
        self.assertEquals(books, books_with_reviews)
        self.assertNotEquals(books, books_without_reviews)


class TestReviewList(TestCase):
    def setUp(self):
        self.user = UserFactory(username='test')
        self.author = AuthorFactory()

    def test_reviews_url(self):
        url = resolve('/review/')
        self.assertEquals(url.func.__name__, ReviewList.__name__)

    def test_authentication_control(self):
        response = self.client.get(reverse('review-books'))
        self.assertEquals(response.status_code, 302)

        self.client.login(username='test', password='test')
        response = self.client.get(reverse('review-books'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'list-to-review.html')

    def test_review_list_returns_books_to_review(self):
        books_without_revies = BookFactory.create_batch(10, authors=[self.author,])
        self.client.login(username='test', password='test')
        response = self.client.get(reverse('review-books'))
        books = list(response.context['books'])
        self.assertEquals(books_without_revies, books)

    def test_can_create_new_book(self):
        self.client.login(username='test', password='test')
        self.client.post(
            reverse('review-books'),
            data = {
                'title': 'Test Book',
                'authors': [self.author.pk,],
                'reviewed_by': self.user.pk,
            }
        )
        self.assertIsNotNone(Book.objects.get(title="Test Book"))



