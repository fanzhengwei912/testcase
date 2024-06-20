from django import forms
from django.http import JsonResponse
from django.shortcuts import render
from case.models import Grouping
from case.utils.bootstrap import BootStrapModelForm
from django.views.decorators.csrf import csrf_exempt
import datetime



class GroupingModelForm(BootStrapModelForm):

    class Meta:
        model = Grouping
        # fields = ['group_code','group_name','leader_name','desc']
        exclude=["id","create_time"]


def group_list(request):
    queryset = Grouping.objects.all()
    form = GroupingModelForm()

    return render(request,'group_list.html',{'queryset': queryset,'form':form})
@csrf_exempt
def group_add(request):
    form = GroupingModelForm(data=request.POST)
    if form.is_valid():
        form.instance.create_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        form.save()
        return JsonResponse({'status':True})
    return JsonResponse({'status':False,'error':form.errors})


def group_edit_click(request):
    uid = request.GET.get('uid')
    row_dict = Grouping.objects.filter(id=uid).values("group_code", "group_name", "leader_name", 'desc').first()
    return JsonResponse({'status':True,'data':row_dict})

@csrf_exempt
def group_edit(request):
    uid = request.GET.get('uid')
    row_dict = Grouping.objects.filter(id=uid).first()
    print(row_dict)
    form = GroupingModelForm(data=request.POST,instance=row_dict)

    if form.is_valid():
        # create = form.cleaned_data["create_time"]
        form.instance.create_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        form.save()
        return JsonResponse({'status':True})
    return JsonResponse({'status':False,'error':form.errors})

def group_delete(request):

    uid = request.GET.get('uid')
    Grouping.objects.filter(id=uid).delete()
    exists = Grouping.objects.filter(id=uid).exists()
    if not exists:
        return JsonResponse({'status':True})
    return JsonResponse({'status':False,'error':"删除失败"})
