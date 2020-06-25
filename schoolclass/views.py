from django.db import models
from django.shortcuts import render, redirect
from database.models import SchoolClass
from database.user_functions import *
from .forms import ClassForm
from database.helper import parse_req_body

def all_schoolclass(request):
    if request.user.is_authenticated:
        user = request.user
        if user.is_teacher:
            if request.method == "POST":
                class_form = ClassForm(data=request.POST)
                print(class_form)
                try:
                    if class_form.is_valid():
                        name = class_form.cleaned_data["name"]
                        create_class(user, name)
                        
                except:
                    import traceback
                    traceback.print_exc()
                    return render(request, "all_schoolclass.html")
            class_form = ClassForm()
        else:
            class_form = None
        all_schoolclass = user.schoolclasses.all()
        
        context = {
            "all_schoolclass": all_schoolclass,
            "class_form": class_form,
        }

        return render(request, "all_schoolclass.html", context=context)
    else:
        return redirect('index')

def view_schoolclass(request, pk):
    user = request.user
    if user.is_authenticated:
        schoolclass = user.schoolclasses.get(pk=pk)
        if request.method == 'GET':
            if schoolclass is not None:
                context = { 
                    "schoolclass": schoolclass,
                    'is_enrolled': "True",
                    'pk':pk,
                }

            else:
                schoolclass = SchoolClass.objects.get(pk=pk)
                
                context = { 
                    "schoolclass": schoolclass,
                    'is_enrolled': "False",
                    'pk':pk,
                }  
            print(context)
            return render(request, "view_schoolclass.html", context=context)
        else:
            if user == schoolclass.teacher:
                body = parse_req_body(request.body)
                print(body)
                if schoolclass is not None:
                    if body['submit'] == 'Delete Class':
                        print('Delete class')
                        # to just remove teacher
                        request.user.schoolclasses.remove(schoolclass)
                        # to delete actual class
                        # SchoolClass.objects.get(pk=pk).delete()
                        return redirect('all_schoolclass')
            
            schoolclass = SchoolClass.objects.get(pk=pk)
            
            context = { 
                "schoolclass": schoolclass,
                'is_enrolled': "False",
                'pk':pk,
            }  
        
            return render(request, "view_schoolclass.html", context=context)
    else:
        return redirect('index')