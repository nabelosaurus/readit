from django.core.exceptions import NON_FIELD_ERRORS
from django.test import TestCase
from books.factories import AuthorFactory, BookFactory
from books.forms import BookForm, ReviewForm

# Create your tests here.
class ReviewFormTest(TestCase):
    def test_no_review(self):
        form = ReviewForm(
            data={
                'is_favourite': False,
            }
        )
        self.assertFalse(form.is_valid())
        self.assertTrue(form.has_error('review', code='required'))


    def test_review_too_short(self):
        form = ReviewForm(
            data={
                'is_favourite': False,
                'review': "Too short",
            }
        )
        self.assertFalse(form.is_valid())
        self.assertTrue(form.has_error('review', code='min_length'))

class BookFormTest(TestCase):
    def setUp(self):
        self.author = AuthorFactory()
        self.book = BookFactory(title="Reject This Book", authors=[self.author,])

    def test_custom_validation_rejects_book_that_already_exists(self):
         form = BookForm(
             data={
                 'title':'Reject This Book',
                 'authors': [self.author.pk,],
             }
         )
         self.assertFalse(form.is_valid())
         self.assertTrue(form.has_error(NON_FIELD_ERRORS, code="bookexists"))

    def test_custom_validation_accepts_new_book(self):
        form = BookForm(
            data={
                'title':'Accept This Book',
                'authors': [self.author.pk,],
            }
        )
        self.assertTrue(form.is_valid())