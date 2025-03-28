from rest_framework import viewsets
from .models import UserModel
from .serializers import UserModelSerializer

class UserModelViewSet(viewsets.ModelViewSet):
    queryset = UserModel.objects.all()
    serializer_class = UserModelSerializer

from django.shortcuts import render, get_object_or_404, redirect
from .models import UserModel
from .forms import UserModelForm

def user_list(request):
    users = UserModel.objects.all()
    return render(request, 'user/user_list.html', {'users': users})

def user_create(request):
    if request.method == 'POST':
        form = UserModelForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('user_list')
    else:
        form = UserModelForm()
    return render(request, 'user/user_form.html', {'form': form})

def user_update(request, pk):
    user = get_object_or_404(UserModel, pk=pk)
    if request.method == 'POST':
        form = UserModelForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user_list')
    else:
        form = UserModelForm(instance=user)
    return render(request, 'user/user_form.html', {'form': form})

def user_delete(request, pk):
    user = get_object_or_404(UserModel, pk=pk)
    if request.method == 'POST':
        user.delete()
        return redirect('user_list')
    return render(request, 'user/user_confirm_delete.html', {'user': user})
