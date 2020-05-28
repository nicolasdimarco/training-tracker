from django.contrib.auth.decorators import login_required
from django.db.models import F
from django.forms import ModelForm
from django.shortcuts import render, redirect
from django.views.decorators.clickjacking import xframe_options_exempt
from routine.models import Routine, RoutineInstruction
from django import forms


class RoutineForm(ModelForm):
    estimated_duration = forms.DurationField(label='Duración estimada', initial="00:00:00",
                                             help_text='Dejar en "00:00:00" si no quiere especificar duración.')

    def __init__(self, *args, **kwargs):
        super(RoutineForm, self).__init__(*args, **kwargs)
        self.fields['name'].label = "Nombre"
        self.fields['description'].label = "Descripción"
        self.fields['effort_level'].label = "Nivel de esfuerzo"
        self.fields['order'].label = "Órden"
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Routine
        fields = ['name', 'description', 'estimated_duration', 'effort_level', 'order']
        help_texts = {
            'order': 'Dejar vacío si no importa su orden',
        }


class RoutineInstructionForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(RoutineInstructionForm, self).__init__(*args, **kwargs)
        self.fields['title'].label = "Titulo"
        self.fields['description'].label = "Descripcion"
        self.fields['video_link'].label = "Link al video"
        self.fields['video_link'].widget.attrs['placeholder'] = "Ingrese solo videos de Youtube"
        self.fields['order'].label = "Orden"
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = RoutineInstruction
        fields = ['title', 'description', 'video_link', 'order']


@login_required
def routine_list(request):
    routines = Routine.objects.filter(training_group=request.user.training_group).order_by(F('order').asc(nulls_last=True), 'pk')
    return render(request, 'routine_list.html', {'routines': routines})


@login_required
@xframe_options_exempt
def routine_detail(request, pk):
    routine = Routine.objects.get(pk=pk)
    routine_instructions = RoutineInstruction.objects.filter(routine=routine).order_by(F('order').asc(nulls_last=True), 'pk')
    ctx = {'routine': routine, 'routine_instructions': routine_instructions}
    return render(request, 'routine_detail.html', ctx)


@login_required
def routine_create(request):
    if request.method == 'POST':
        form = RoutineForm(request.POST)
        if form.is_valid():
            routine = form.save(commit=False)
            routine.user = request.user
            routine.training_group = request.user.training_group
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


@login_required
def routine_instruction_list(request, pk):
    if not request.user.is_trainer:
        return redirect("/routine")
    try:
        routine = Routine.objects.get(pk=pk)
        instructions = RoutineInstruction.objects.filter(routine=routine).order_by(F('order').asc(nulls_last=True), 'pk')
        return render(request, 'routine_instruction_list.html', {'instructions': instructions, 'routine': routine})
    except Routine.DoesNotExist:
        return redirect("/routine")


@login_required
def routine_instruction_create(request, pk):
    if not request.user.is_trainer:
        return redirect("/routine")

    try:
        routine = Routine.objects.get(pk=pk)
        if request.method == 'POST':
            form = RoutineInstructionForm(request.POST)
            if form.is_valid():
                instruction = form.save(commit=False)
                instruction.routine = routine
                instruction.save()
                return redirect("/routine/{}/instruction".format(pk))
        return render(request, 'routine_instruction_create.html',
                      {'form': RoutineInstructionForm(), 'routine': routine})
    except Routine.DoesNotExist:
        return redirect("/routine")


@login_required
def routine_instruction_edit(request, routine_pk, instruction_pk):
    try:
        instruction = RoutineInstruction.objects.get(pk=instruction_pk, routine__id=routine_pk)
        if request.method == 'POST':
            form = RoutineInstructionForm(request.POST, instance=instruction)
            if form.is_valid():
                form.save()
                return redirect("/routine/{}/instruction".format(routine_pk))
        return render(request, 'routine_instruction_edit.html', {'form': RoutineInstructionForm(instance=instruction),
                                                                 'instruction': instruction})
    except RoutineInstruction.DoesNotExist:
        return redirect("/routine")
