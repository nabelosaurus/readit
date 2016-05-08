from django import forms
from .models import Book

class ReviewForm(forms.Form):
    """
    Form for reviewing book
    """
    is_favourite = forms.BooleanField(
            label="Favourite",
            help_text="In your top 100 books of all time?",
            required=False,
    )
    review = forms.CharField(
            widget=forms.Textarea,
            min_length=300,
            error_messages={
                'required': "Please enter your review",
                'min_length':"Minimum length of review is 300 characthers. You have written %(show_value)s"
            },
    )

class BookForm(forms.ModelForm):
    class Meta:
         model = Book
         fields = ['title', 'authors', 'reviewed_by']
         
    def clean(self):
        super(BookForm, self).clean()

        try:
            title = self.cleaned_data['title']
            author = self.cleaned_data['authors']
            book = Book.objects.get(title=title, authors=author)

            raise forms.ValidationError(
                "The book {} by {} already exists".format(title, book.list_authors()),
                code="bookexists"
            )
        except Book.DoesNotExist:
            return self.cleaned_data