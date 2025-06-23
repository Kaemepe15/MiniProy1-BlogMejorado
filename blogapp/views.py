from django.views.generic import ListView, DetailView, CreateView, TemplateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Blog, Review, Comment, Tag
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .forms import ReviewForm, BlogForm
from django.http import HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Count

class BlogListView(ListView):
    model = Blog
    template_name = 'blogapp/blog_list.html'
    paginate_by = 4  # Muestra 4 blogs por página

class BlogDetailView(DetailView):
    model = Blog
    template_name = 'blogapp/blog_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['user'] = self.request.user
            context['can_add_review'] = not Review.objects.filter(blog=self.get_object(), reviewer=self.request.user).exists()
        else:
            context['user_id'] = None  # Para manejar el caso de usuario no autenticado
        return context

class BlogCreateView(LoginRequiredMixin, CreateView):
    model = Blog
    form_class = BlogForm  # Nuevo formulario para Tags
    template_name = 'blog_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('blogapp:blog_detail', kwargs={'pk': self.object.pk})

class ReviewCreateView(LoginRequiredMixin, CreateView):
    model = Review
    form_class = ReviewForm  # Usa el formulario personalizado
    template_name = 'blogapp/review_form.html'

    def get(self, request, *args, **kwargs):
        # Verifica si el usuario ya ha dejado una reseña para este blog
        blog_id = self.kwargs['pk']
        reviewer = self.request.user
        if Review.objects.filter(blog_id=blog_id, reviewer=reviewer).exists():
            # Redirige a la página de detalles si ya existe una reseña
            return HttpResponseRedirect(reverse_lazy('blogapp:blog_detail', kwargs={'pk': blog_id}))
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.reviewer = self.request.user
        form.instance.blog_id = self.kwargs['pk']
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('blogapp:blog_detail', kwargs={'pk': self.kwargs['pk']})

class CommentCreateView(CreateView):
    model = Comment
    fields = ['content']
    template_name = 'blogapp/comment_form.html'

    def form_valid(self, form):
        form.instance.commenter = self.request.user
        form.instance.review_id = self.kwargs['review_pk']
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('blogapp:blog_detail', kwargs={'pk': self.kwargs['blog_pk']})

class RegisterView(CreateView):
    form_class = UserCreationForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('accounts:login')

# Vista para filtrar por Tag
class BlogListByTagView(ListView):
    model = Blog
    template_name = 'blogapp/blog_list.html'

    def get_queryset(self):
        tag_name = self.kwargs['tag_name']
        return Blog.objects.filter(tags__name=tag_name)

class AdminDashboardView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = 'blogapp/admin_dashboard.html'

    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_staff

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Datos existentes
        context['blogs'] = Blog.objects.all()
        context['tags'] = Tag.objects.all()
        context['blog_count'] = Blog.objects.count()
        context['tag_count'] = Tag.objects.count()

        # Blogs más comentados
        blogs_with_comments = Blog.objects.annotate(
            comment_count=Count('reviews__comments')
        ).order_by('-comment_count')[:5]  # Top 5 blogs más comentados
        context['most_commented_blogs'] = blogs_with_comments

        # Blogs mejor puntuados
        blogs_by_rating = Blog.objects.annotate(
            avg_rating=Count('reviews__rating')
        ).order_by('-avg_rating')[:5]  # Top 5 blogs mejor puntuados
        context['top_rated_blogs'] = [
            {'blog': blog, 'rating': blog.average_rating()}
            for blog in Blog.objects.all()
        ]
        context['top_rated_blogs'] = sorted(
            context['top_rated_blogs'],
            key=lambda x: x['rating'],
            reverse=True
        )[:5]

        return context

# Vistas para Blogs 
class BlogUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Blog
    form_class = BlogForm
    template_name = 'blogapp/blog_form.html'

    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_staff

    def get_success_url(self):
        return reverse_lazy('blogapp:admin_dashboard')

class BlogDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Blog
    template_name = 'blogapp/blog_confirm_delete.html'

    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_staff

    def get_success_url(self):
        return reverse_lazy('blogapp:admin_dashboard')

#Vistas para Etiquetas
class TagCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Tag
    fields = ['name']
    template_name = 'blogapp/tag_form.html'

    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_staff

    def get_success_url(self):
        return reverse_lazy('blogapp:admin_dashboard')

class TagUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Tag
    fields = ['name']
    template_name = 'blogapp/tag_form.html'

    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_staff

    def get_success_url(self):
        return reverse_lazy('blogapp:admin_dashboard')

class TagDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Tag
    template_name = 'blogapp/tag_confirm_delete.html'

    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_staff

    def get_success_url(self):
        return reverse_lazy('blogapp:admin_dashboard')