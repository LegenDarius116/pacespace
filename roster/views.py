from django.db.models import Q
from django.shortcuts import render, redirect
from database.models import SchoolClass, PaceUser
from database.user_functions import *
from database.helper import parse_req_body

def enrollment(request, pk):
    if request.user.is_authenticated:
        user = request.user
        schoolclass = SchoolClass.objects.get(pk=pk)
        # user is teacher of class
        if user == schoolclass.teacher:
            if request.method == 'GET':
                query = request.GET.get('q')
                submitbutton = request.GET.get('submit')

                if query is not None:
                    lookups= Q(username__icontains=query) | Q(email__icontains=query)
                    results= PaceUser.objects.filter(lookups).distinct().exclude(schoolclasses=schoolclass).filter(is_student=True)
                
                else:
                    lookups = None
                    results = None
                context = {
                    'results': results,
                    'submitbutton': submitbutton,
                    'pk':pk
                }
                return render(request, "enrollment.html", context=context)
            else:
                body = parse_req_body(request.body)
                print(body)
                student = PaceUser.objects.get(pk=body['user_id'])
                add_student_to_class(user, schoolclass, student)
                print('added student')
                
                context = {
                    'results': None,
                    'submitbutton': None,
                    'pk':pk
                }

                return render(request, "enrollment.html", context=context)
        else:
            print('Not teacher of class')
            return redirect('index')
    else:
        return redirect('index')

def students(request, pk):
    if request.user.is_authenticated:
        user = request.user
        schoolclass = user.schoolclasses.get(pk=pk)
        # user is in the class
        if schoolclass is not None:
            students = PaceUser.objects.filter(schoolclasses=schoolclass).filter(is_student=True)
            context = {
                'students':students,
                'schoolclass':schoolclass,
            }
            return render(request, "students.html", context=context)
        # user is not in the class
        else:
            return redirect('all_schoolclass')
    else:
        return redirect('index')
