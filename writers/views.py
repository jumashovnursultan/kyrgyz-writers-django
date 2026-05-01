from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count, Q
from .models import Writer, Quote, Work, Favorite
import random


def home(request):
    query = request.GET.get('q', '')
    epoch = request.GET.get('epoch', '')
    letter = request.GET.get('letter', '')
    language = request.GET.get('language', '')
    genre = request.GET.get('genre', '')

    writers = list(Writer.objects.all())

    if query:
        q = query.lower()
        matched = [w for w in writers if
                   q in w.name.lower() or
                   q in w.biography.lower() or
                   q in w.tags.lower()]
        writers = sorted(matched, key=lambda w: (0 if q in w.name.lower() else 1))           

    if epoch:
        writers = [w for w in writers if epoch.lower() in w.epoch.lower()]

    if letter:
        writers = [w for w in writers if w.name.startswith(letter)]

    if language:
        writers = [w for w in writers if w.language == language]

    if genre:
        genre_ids = set(Work.objects.filter(genre__icontains=genre).values_list('writer_id', flat=True))
        writers = [w for w in writers if w.pk in genre_ids]

    epochs = Writer.objects.values_list('epoch', flat=True).distinct()
    genres = Work.objects.values_list('genre', flat=True).distinct().exclude(genre='')
    letters = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'

    favorite_ids = set()
    if request.user.is_authenticated:
        favorite_ids = set(
            Favorite.objects.filter(user=request.user).values_list('writer_id', flat=True)
        )

    return render(request, 'writers/home.html', {
        'writers': writers,
        'epochs': epochs,
        'genres': genres,
        'query': query,
        'selected_epoch': epoch,
        'selected_letter': letter,
        'selected_language': language,
        'selected_genre': genre,
        'letters': letters,
        'favorite_ids': favorite_ids,
    })


def writer_detail(request, pk):
    writer = get_object_or_404(Writer, pk=pk)

    writer_genres = writer.work_set.values_list('genre', flat=True)
    similar = Writer.objects.exclude(pk=writer.pk).filter(
        Q(epoch=writer.epoch) |
        Q(work_set__genre__in=writer_genres)
    ).distinct()[:4]

    is_favorite = False
    if request.user.is_authenticated:
        is_favorite = Favorite.objects.filter(user=request.user, writer=writer).exists()

    return render(request, 'writers/detail.html', {
        'writer': writer,
        'similar': similar,
        'is_favorite': is_favorite,
    })


def random_writer(request):
    writers = Writer.objects.all()
    if writers.exists():
        writer = random.choice(list(writers))
        return redirect('writer_detail', pk=writer.pk)
    return redirect('home')


def statistics(request):
    total = Writer.objects.count()
    by_epoch = Writer.objects.values('epoch').annotate(count=Count('id')).order_by('-count')
    by_language = Writer.objects.values('language').annotate(count=Count('id'))
    total_works = Work.objects.count()
    total_quotes = Quote.objects.count()
    return render(request, 'writers/statistics.html', {
        'total': total,
        'by_epoch': by_epoch,
        'by_language': by_language,
        'total_works': total_works,
        'total_quotes': total_quotes,
    })


def timeline(request):
    writers = Writer.objects.all().order_by('birth_year')
    return render(request, 'writers/timeline.html', {'writers': writers})


def about(request):
    total_writers = Writer.objects.count()
    total_works = Work.objects.count()
    total_quotes = Quote.objects.count()
    return render(request, 'writers/about.html', {
        'total_writers': total_writers,
        'total_works': total_works,
        'total_quotes': total_quotes,
    })


# ─── Авторизация ──────────────────────────────────────────────────────────────

def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Каттоо ийгиликтүү өттү! Кош келиңиз!')
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'writers/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect(request.GET.get('next', 'home'))
        else:
            messages.error(request, 'Логин же сырсөз туура эмес.')
    else:
        form = AuthenticationForm()
    return render(request, 'writers/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('home')


# ─── Избранное ────────────────────────────────────────────────────────────────

@login_required
def toggle_favorite(request, pk):
    writer = get_object_or_404(Writer, pk=pk)
    fav, created = Favorite.objects.get_or_create(user=request.user, writer=writer)
    if not created:
        fav.delete()
    next_url = request.GET.get('next', 'writer_detail')
    if next_url == 'home':
        return redirect('home')
    return redirect('writer_detail', pk=pk)


@login_required
def my_favorites(request):
    favorites = Favorite.objects.filter(user=request.user).select_related('writer').order_by('-created_at')
    return render(request, 'writers/favorites.html', {'favorites': favorites})