"""
URL configuration for testcase_platform project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from django.views.static import serve
from django.conf import settings

from django.urls import path
from case.views import version, user, group # , demand, case, step, expectation

urlpatterns = [
    # path('admin/', admin.site.urls),
    # 匹配media文件目录
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}, name='media'),
    #分组列表
    path('group/list/', group.group_list),
    path('group/add/', group.group_add),
    path('group/edit/ck/', group.group_edit_click),
    path('group/edit/', group.group_edit),
    path('group/delete/', group.group_delete),
    # 用户列表
    path('user/list/', user.user_list),
    path('user/add/', user.user_add),
    #版本列表
    path('version/list/', version.version_list),
]
