from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import ListView, CreateView, DeleteView, UpdateView, TemplateView
from .models import Music, Folder, Favorite
from .forms import SignUpForm, Musicform, FolderForm, AddMusicToFolderForm
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse


def home(request):
    tracks = Music.objects.all()
    user_favorites = set()
    if request.user.is_authenticated:
        favorite, created = Favorite.objects.get_or_create(user=request.user)
        user_favorites = set(favorite.tracks.all())
    return render(request, 'index.html', {'tracks': tracks, 'user_favorites': user_favorites})


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            if user is not None:
                login(request, user)

                Folder.objects.create(name='Favorites', user=user, is_favorites=True)
                return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


class AddMusic(CreateView):
    template_name = 'addmusic.html'
    model = Music
    form_class = Musicform
    success_url = '/home'


class MusicDelete(DeleteView):
    model = Music
    template_name = 'confirm_delete.html'
    success_url = '/musiclist'


class Musiclist(ListView):
    template_name = 'listmusic.html'
    model = Music
    context_object_name = 'list'


class Musicupdate(UpdateView):
    model = Music
    template_name = 'addmusic.html'
    fields = ['title', 'artist', 'genre']
    success_url = '/musiclist'


class CreateFolder(LoginRequiredMixin, View):
    def get(self, request):
        form = FolderForm()
        return render(request, 'create_folder.html', {'form': form})

    def post(self, request):
        form = FolderForm(request.POST)
        if form.is_valid():
            folder = form.save(commit=False)
            folder.user = request.user
            folder.save()
            return redirect('folder_detail', folder_id=folder.id)
        return render(request, 'create_folder.html', {'form': form})


class FolderListView(LoginRequiredMixin, ListView):
    model = Folder
    template_name = 'folder_list.html'
    context_object_name = 'folders'

    def get_queryset(self):
        return Folder.objects.filter(user=self.request.user)


def folder_detail(request, folder_id):
    folder = get_object_or_404(Folder, pk=folder_id, user=request.user)
    tracks = folder.tracks.all()
    return render(request, 'folder_detail.html', {'folder': folder, 'tracks': tracks})


def add_music_to_folder(request, folder_id):
    if not request.user.is_authenticated:
        messages.error(request, 'You must be logged in to add music to a folder.')
        return redirect('login')

    folder = get_object_or_404(Folder, pk=folder_id, user=request.user)

    if request.method == 'POST':
        form = AddMusicToFolderForm(request.POST)
        if form.is_valid():
            selected_tracks = form.cleaned_data.get('selected_tracks', [])
            for track in selected_tracks:
                if track.genre == folder.genre:
                    folder.tracks.add(track)
                else:
                    messages.error(request, f'Track "{track.title}" genre does not match the genre of the folder.')
            messages.success(request, 'Tracks added to folder successfully.')
            return HttpResponseRedirect(reverse('folder_detail', args=[folder_id]))
        else:
            messages.error(request, 'Invalid form submission.')
    else:
        form = AddMusicToFolderForm()

    return render(request, 'add_music_to_folder.html', {'form': form, 'folder': folder})


def add_to_favorites(request, track_id):
    if request.user.is_authenticated:
        track = get_object_or_404(Music, pk=track_id)
        favorite, created = Favorite.objects.get_or_create(user=request.user)
        favorite.tracks.add(track)
        messages.success(request, f'Added "{track.title}" to favorites.')
    return redirect('home')


def remove_from_favorites(request, track_id):
    if request.user.is_authenticated:
        track = get_object_or_404(Music, pk=track_id)
        favorite, created = Favorite.objects.get_or_create(user=request.user)
        favorite.tracks.remove(track)
        messages.success(request, f'Removed "{track.title}" from favorites.')
    return redirect('home')


class Folderdelete(DeleteView):
    model = Folder
    template_name = 'confirm_delete.html'
    success_url = '/folders'


def favorites(request):
    user_favorites = []
    if request.user.is_authenticated:
        favorite, created = Favorite.objects.get_or_create(user=request.user)
        user_favorites = favorite.tracks.all()
    return render(request, 'favorites.html', {'user_favorites': user_favorites})