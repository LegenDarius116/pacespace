from django.db import models
from django.shortcuts import render, redirect
from database.models import SchoolClass
from database.user_functions import *
from .forms import ClassForm

# Create your views here.
def all_schoolclass(request):
    if request.user.is_authenticated:
        user = request.user
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

        all_schoolclass = user.school_classes.all
        class_form = ClassForm()
        context = {
            "all_schoolclass": all_schoolclass,
            "class_form": class_form,
        }

        return render(request, "all_schoolclass.html", context=context)
    else:
        return redirect('index')

def view_schoolclass(request, pk):
    if request.user.is_authenticated:
        schoolclass = request.user.school_classes.get(pk=pk)
        
        if schoolclass is not None:
            context = { 
                "schoolclass": schoolclass,
                'is_enrolled': "True",
            }

        else:
            print("Not enrolled")
            schoolclass = SchoolClass.objects.get(pk=pk)
            
            context = { 
                "schoolclass": schoolclass,
                'is_enrolled': "False",
            }  
        print(context)
        return render(request, "view_schoolclass.html", context=context)

    else:
        return redirect('index')