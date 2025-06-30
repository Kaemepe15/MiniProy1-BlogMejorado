from django import forms
from .models import Blog, Review, Tag
import os

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

    def clean_featured_image(self):
        featured_image = self.cleaned_data.get('featured_image')
        if featured_image:
            # Lista de extensiones permitidas
            allowed_extensions = ['.jpg', '.jpeg', '.png', '.gif']
            ext = os.path.splitext(featured_image.name)[1].lower()
            if ext not in allowed_extensions:
                raise forms.ValidationError("Solo se permiten archivos de imagen (.jpg, .jpeg, .png, .gif).")
            # Verifica que sea una imagen válida
            if not featured_image.content_type.startswith('image/'):
                raise forms.ValidationError("El archivo debe ser una imagen válida.")
        return featured_image

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['tags'].label = "Tags (select or add new ones)"