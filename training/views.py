import datetime
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.shortcuts import render, redirect
from django.forms import ModelForm
from django import forms

from authentication.models import User
from routine.models import Routine, RoutineInstruction
from training.models import Training


class TrainingForm(ModelForm):
    routine = forms.ModelChoiceField(label='Rutina', queryset=Routine.objects.all())
    date = forms.DateField(label='Fecha', initial=datetime.date.today)
    duration = forms.DurationField(label='Duración', initial="01:00:00")

    def __init__(self, *args, **kwargs):
        super(TrainingForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Training
        fields = ['routine', 'date', 'duration']


@login_required
def dashboard(request):
    return render(request, 'dashboard.html')


@login_required
def training_list(request):
    trainings = Training.objects.filter(user=request.user).order_by('-date', 'duration')
    hours = trainings.aggregate(Sum('duration'))
    total_hours = hours['duration__sum'] if hours['duration__sum'] else 0
    qty = trainings.count()
    return render(request, 'training_list.html', {'trainings': trainings, 'total_time': total_hours, 'weekly_average': qty})


@login_required
def trainer_dashboard(request):
    if request.user.is_trainer:
        trainings = Training.objects.filter(user__training_group=request.user.training_group).order_by('user', '-date', 'duration')
        members = User.objects.filter(training_group=request.user.training_group).count()
        instructions = RoutineInstruction.objects.filter(routine__training_group=request.user.training_group).count()
        hours = trainings.aggregate(Sum('duration'))
        total_hours = hours['duration__sum'] if hours['duration__sum'] else 0
        routines = Routine.objects.filter(training_group=request.user.training_group).count()
        ctx = {
            'trainings': trainings,
            'members': members,
            'routines': routines,
            'instructions': instructions,
            'hours': total_hours
        }
        return render(request, 'trainer_dashboard.html', ctx)
    return redirect("/training")


@login_required
def training_create(request):
    if request.method == 'POST':
        form = TrainingForm(request.POST)
        if form.is_valid():
            training = form.save(commit=False)
            training.user = request.user
            training.save()
            return redirect("/training")
    return render(request, 'training_create.html', {'form': TrainingForm()})


@login_required
def training_delete(request, pk):
    try:
        training = Training.objects.get(pk=pk)
        training.delete()
        return redirect("/training")
    except Training.DoesNotExist:
        trainings = Training.objects.filter(user=request.user)
        ctx = {'trainings': trainings, 'error': 'El entrenamiento que intenta borrar no existe'}
        return render(request, 'training_list.html', ctx)


