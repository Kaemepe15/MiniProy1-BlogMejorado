from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.http import HttpResponseRedirect
from .models import Blog, Review, Comment
from .forms import ReviewForm
import bleach

class BlogListView(ListView):
    model = Blog
    template_name = 'blogapp/blog_list.html'

class BlogDetailView(DetailView):
    model = Blog
    template_name = 'blogapp/blog_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        context['can_add_review'] = not Review.objects.filter(blog=self.get_object(), reviewer=self.request.user).exists()
        return context

class BlogCreateView(LoginRequiredMixin, CreateView):
    model = Blog
    fields = ['title', 'content', 'featured_image']
    template_name = 'blog_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        # Sanitizar el contenido del blog (para CKEditor)
        form.instance.content = bleach.clean(
            form.instance.content,
            tags=['p', 'b', 'i', 'a', 'ul', 'ol', 'li', 'strong', 'em'],
            attributes={'a': ['href']}
        )
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('blogapp:blog_detail', kwargs={'pk': self.object.pk})

class ReviewCreateView(LoginRequiredMixin, CreateView):
    model = Review
    form_class = ReviewForm
    template_name = 'blogapp/review_form.html'

    def get(self, request, *args, **kwargs):
        blog_id = self.kwargs['pk']
        reviewer = self.request.user
        if Review.objects.filter(blog_id=blog_id, reviewer=reviewer).exists():
            return HttpResponseRedirect(reverse_lazy('blogapp:blog_detail', kwargs={'pk': blog_id}))
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.reviewer = self.request.user
        form.instance.blog_id = self.kwargs['pk']
        # Sanitizar el comentario de la reseña
        form.instance.comment = bleach.clean(
            form.instance.comment,
            tags=['p', 'b', 'i', 'a', 'ul', 'ol', 'li', 'strong', 'em'],
            attributes={'a': ['href']}
        )
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('blogapp:blog_detail', kwargs={'pk': self.kwargs['pk']})

class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    fields = ['content']
    template_name = 'blogapp/comment_form.html'

    def form_valid(self, form):
        form.instance.commenter = self.request.user
        form.instance.review_id = self.kwargs['review_pk']
        # Sanitizar el contenido del comentario
        form.instance.content = bleach.clean(
            form.instance.content,
            tags=['p', 'b', 'i', 'a', 'ul', 'ol', 'li', 'strong', 'em'],
            attributes={'a': ['href']}
        )
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('blogapp:blog_detail', kwargs={'pk': self.kwargs['blog_pk']})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Gracias, {user.username}, por crear tu cuenta con nosotros. ¡Bienvenido!')
            return redirect('blogapp:blog_list')
        else:
            messages.error(request, 'Error en el formulario, por favor corrige para continuar')
    else:
        form = UserCreationForm()
    return render(request, 'blogapp/signup.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Qué bueno que volviste, {user.username}')
                return redirect('blogapp:blog_list')
            else:
                messages.error(request, 'Usuario o contraseña incorrectos')
        else:
            messages.error(request, 'Por favor corrige los errores en el formulario')
    else:
        form = AuthenticationForm()
    return render(request, 'blogapp/login.html', {'form': form})

def user_logout(request):
    logout(request)
    messages.success(request, 'Cierre de sesión exitoso')
    return redirect('blogapp:blog_list')
