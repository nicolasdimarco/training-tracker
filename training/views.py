from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from training.models import Training


@login_required
def dashboard(request):
    return render(request, 'dashboard.html')


@login_required
def training_list(request):
    trainings = Training.objects.filter(user=request.user)
    return render(request, 'training_list.html', {'trainings': trainings})


@login_required
def training_create(request):
    if request.method == 'POST':
        pass
    else:
        pass
    return render(request, 'training_create.html', {'trainings': trainings})


@login_required
def training_delete(request, id):
    try:
        training = Training.objects.get(pk=id)
        training.delete()
        return redirect("/training")
    except Training.ObjectDoesNotExist:
        trainings = Training.objects.filter(user=request.user)
        ctx = {'trainings': trainings, 'error': 'El entrenamiento que intenta borrar no existe'}
        return render(request, 'training_list.html', ctx)


