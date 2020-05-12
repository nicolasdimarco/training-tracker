from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.decorators.clickjacking import xframe_options_exempt

from routine.models import Routine, RoutineInstruction


@login_required
def routines_list(request):
    routines = Routine.objects.all()
    return render(request, 'routine_list.html', {'routines': routines})


@login_required
@xframe_options_exempt
def routine_detail(request, id):
    routine = Routine.objects.get(pk=id)
    routine_instructions = RoutineInstruction.objects.filter(routine=routine)
    ctx = {'routine': routine, 'routine_instructions': routine_instructions}
    return render(request, 'routine_detail.html', ctx)
