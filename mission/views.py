from django.db import models
from django.shortcuts import render, redirect
from database.models import SchoolClass, Mission, PaceUser
from database.user_functions import *
from .forms import CreateMissionForm, SubmitMissionForm
import datetime 

STATUS_CHOICES = [
    ('A', 'Assigned'),
    ('S', 'Submitted'),
    ('O', 'Overdue'),
    ('SL', 'Submitted Late')
]    

status = models.CharField(
    max_length=2,
    choices=STATUS_CHOICES,
    default="A"
)

def all_mission(request, pk):
    if request.user.is_authenticated:
        user = request.user
        schoolclass = user.schoolclasses.get(pk=pk)
        if schoolclass is not None:
            all_mission = Mission.objects.filter(schoolclass__pk=pk)

            if request.method == 'GET':
                if user == schoolclass.teacher:
                    create_mission_form = CreateMissionForm()
                else:
                    create_mission_form = None

                context = {
                    'all_mission': all_mission,
                    'pk': pk,
                    'create_mission_form': create_mission_form,
                }

            else:
                create_mission_form = CreateMissionForm(data=request.POST)
                try:
                    if create_mission_form.is_valid():
                        name = create_mission_form.cleaned_data["name"]
                        description = create_mission_form.cleaned_data["description"]
                        instructions = create_mission_form.cleaned_data["instructions"]
                        date_due = create_mission_form.clean_date()
                        mission = Mission(
                            name=name, 
                            description=description,
                            instructions=instructions,
                            date_due=date_due,
                            schoolclass=schoolclass,
                        )
                        mission.save()
                        print('success mission saved')
                    else:
                        print('not valid form')
                except:
                    import traceback
                    traceback.print_exc()
                    return render(request, "all_schoolclass.html")
            
                all_mission = Mission.objects.filter(schoolclass__pk=pk)
                create_mission_form = CreateMissionForm()

                context = {
                    'all_mission': all_mission,
                    'pk': pk,
                    'create_mission_form': create_mission_form,
                }
            
            return render(request, "all_mission.html", context=context)
        else:
            print('Not in this class!')
            return redirect('all_schoolclass')
    else:
        return redirect('index')

def view_mission(request, pk):
    if request.user.is_authenticated:
        # user = request.user
        # if in user.schoolclass
        mission = Mission.objects.get(pk=pk)
        context = {
            'mission':mission,
        }
        return render(request, "view_mission.html", context=context)
    else:
        return redirect('index')    

# def calendar(request):