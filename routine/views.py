from django.contrib.auth.decorators import login_required
from django.forms import ModelForm
from django.shortcuts import render, redirect
from django.views.decorators.clickjacking import xframe_options_exempt
from routine.models import Routine, RoutineInstruction


class RoutineForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(RoutineForm, self).__init__(*args, **kwargs)
        self.fields['name'].label = "Nombre"
        self.fields['description'].label = "Descripción"
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Routine
        fields = ['name', 'description']


@login_required
def routines_list(request):
    routines = Routine.objects.all()
    return render(request, 'routine_list.html', {'routines': routines})


@login_required
@xframe_options_exempt
def routine_detail(request, pk):
    routine = Routine.objects.get(pk=pk)
    routine_instructions = RoutineInstruction.objects.filter(routine=routine)
    ctx = {'routine': routine, 'routine_instructions': routine_instructions}
    return render(request, 'routine_detail.html', ctx)


@login_required
def routine_create(request):
    if request.method == 'POST':
        form = RoutineForm(request.POST)
        if form.is_valid():
            routine = form.save(commit=False)
            routine.user = request.user
            routine.save()
            return redirect("/routine")
    return render(request, 'routine_create.html', {'form': RoutineForm()})


@login_required
def routine_edit(request, pk):
    try:
        routine = Routine.objects.get(pk=pk)
        if request.method == 'POST':
            form = RoutineForm(request.POST, instance=routine)
            if form.is_valid():
                form.save()
                return redirect("/routine")
        return render(request, 'routine_edit.html', {'form': RoutineForm(instance=routine), 'routine': routine})
    except Routine.DoesNotExist:
        return redirect("/routine")
