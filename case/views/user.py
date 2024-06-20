from case import  models

from django.shortcuts import render, redirect
from case.utils.bootstrap import BootStrapModelForm
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

"""
用户列表:
用户id
用户编号
用户名
密码
昵称
部门
身份（超级管理员、管理员、普通用户）
创建时间
更新时间
是否删除
"""
class UserModelForm(BootStrapModelForm):
    class Meta:
        model = models.User
        fields = '__all__'

def user_list(request):
    queryset = models.User.objects.all()
    return render(request,"user_list.html",{'queryset':queryset})
def user_add(request):
    form = UserModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return JsonResponse({"status": True})
    return JsonResponse({'status':False,"error":form.errors})


"""
面试个人介绍：
面试官你好！ 我叫范正伟，是安徽人
从2018年开始从事软件测试工作至今有6年的，时间
对于软件测试的基础理论、测试流程、测试用例的设计方法已经非常熟悉了，也掌握bug的流程及管理工具的使用如jira、禅道等等，
之前也做过比较多的项目比如app、web、小程序端的项目都比较熟悉也积累了丰富的工作经验，也能够独立的负责一个项目，把控项目的整体进度和工作任务的协调安排
在过往的工作中对于mysql的使用非常熟悉，能够保障数据的准确性，也能够对于一些特殊测试场景构建场景数据，在测试中发现bug能熟练使用fiddle抓包工具，
分析定位前后端问题，也能够在服务器上分析报错日志，我们之前的项目属于敏捷迭代的模式，项目比较稳定。
我们每个项目也会做接口测试，
保障接口的质量，所以我对于接口测试和接口测试工具postman的使用也非常熟悉。
为了提升后端回归测试的效率，独立搭建了python+pytest+requests+allure+jekins+git的接口自动化框架进行每日构建，快速分析后端测试质量，项目测试中我也会独立分析性能需求，提炼性能场景。
搭建性能环境构建和构造性能数据，使用jmeter进行性能测试，分析性能指标， 推进开发解决，以上就是我的自我介绍，谢谢





"""
