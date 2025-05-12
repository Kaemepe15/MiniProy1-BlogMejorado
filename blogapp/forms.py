from django import forms
from .models import Blog, Review, Tag

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.Select(choices=[(i, str(i)) for i in range(1, 6)]),
            'comment': forms.Textarea(attrs={'rows': 4}),
        }

#Manejara los campos de blog, creado para tags
class BlogForm(forms.ModelForm): 
    tags = forms.ModelMultipleChoiceField( #Permite seleccionar multiples etiquetas existentes
        queryset=Tag.objects.all(),
        widget=forms.CheckboxSelectMultiple, #etiquetas salen como checkbox
        required=False
    )

    class Meta:
        model = Blog
        fields = ['title', 'content', 'featured_image', 'tags']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 6}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['tags'].label = "Tags (select or add new ones)"