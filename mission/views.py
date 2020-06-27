from django.db import models
from django.shortcuts import render, redirect
from database.models import SchoolClass, Mission, PaceUser
from database.user_functions import *
from .forms import CreateMissionForm, SubmissionForm
import datetime 
from database.helper import parse_req_body
from django.contrib import messages 

def class_mission(request, pk):
    if request.user.is_authenticated:
        user = request.user   
        schoolclass = SchoolClass.objects.get(pk=pk)
        if user == schoolclass.teacher:
            all_mission = Mission.objects.filter(schoolclass__pk=pk)

            if request.method == 'GET':
                create_mission_form = CreateMissionForm()

                context = {
                    'all_mission': all_mission,
                    'pk': pk,
                    'create_mission_form': create_mission_form,
                }

            else:
                form = CreateMissionForm(request.POST, request.FILES)
                if form.is_valid():
                    name = form.cleaned_data["name"]
                    description = form.cleaned_data['description']
                    instructions = form.cleaned_data['instructions']
                    date_due = form.cleaned_data['date_due']
                    schoolclass = schoolclass

                    mission = Mission(
                        name=name, 
                        description=description,
                        instructions=instructions,
                        date_due=date_due,
                        schoolclass=schoolclass,
                    )
                    mission.save()
                    print('success mission saved')
                
                all_mission = Mission.objects.filter(schoolclass__pk=pk)
                create_mission_form = CreateMissionForm()

                context = {
                    'all_mission': all_mission,
                    'pk': pk,
                    'create_mission_form': create_mission_form,
                }
                
            return render(request, "class_mission.html", context=context)
        else:
            print('Not teacher of this class')
            return redirect('all_schoolclass')
    else:
        return redirect('index')

def view_mission(request, pk):
    if request.user.is_authenticated:
        user = request.user
        mission = Mission.objects.get(pk=pk)

        if request.method=='POST':
            form = SubmissionForm(request.POST, request.FILES)
            if form.is_valid():    
                message=form.cleaned_data['message']
                file_submission=form.cleaned_data['file_submission']

                submission = MissionSubmission(
                    student=user,
                    mission=mission,
                    message=message,
                    file_submission=file_submission,
                )
                submission.save()
        
        if user.is_student:
            all_submission = MissionSubmission.objects.filter(student=user).filter(mission=mission)
        else:
            all_submission = MissionSubmission.objects.filter(mission=mission)
        submission_form = SubmissionForm()
        context = {
            'mission': mission,
            'all_submission': all_submission,
            'submission_form': submission_form,
        }
        
        return render(request, "view_mission.html", context=context)
    else:
        return redirect('index')    

# def calendar(request):

def all_mission(request):
    if request.user.is_authenticated:
        user=request.user
        all_mission = Mission.objects.filter(schoolclass__paceuser=user)
        context = {
            'all_mission': all_mission,
        }
        print(context)
        return render(request, "all_mission.html", context=context)