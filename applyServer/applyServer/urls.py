"""applyServer URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.conf.urls import url
from server import applyAdmin,views

urlpatterns = [
    url(r'^superadmin/', admin.site.urls),

    url(r'^api/apply', views.apply),
    url(r'^api/getVerificationCode', views.getVerificationCode),
    url(r'^api/login', views.login),
    url(r'^api/testResult', views.testResult),
    url(r'^api/getApplyStatus', views.getApplyStatus),
    url(r'^api/signIn', views.signIn),
    url(r'^api/toSignIn', views.loginSignIn),

    url(r'^api/admin/login', applyAdmin.adminLogin),
    url(r'^api/admin/getInformation', applyAdmin.getInformation),
    url(r'^api/admin/stage', applyAdmin.stage),
    url(r'^api/admin/changeStage', applyAdmin.changeStage),
    url(r'^api/admin/pass', applyAdmin.passStage),
    url(r'^api/admin/search', applyAdmin.search),
    url(r'^api/admin/getDetail', applyAdmin.getDetail),
    url(r'^api/admin/getPic', applyAdmin.getPic),
    url(r'^api/admin/commits', applyAdmin.commits),
    url(r'^api/admin/begin', applyAdmin.begin),
    url(r'^api/admin/next', applyAdmin.next),
    url(r'^api/admin/getBUName', applyAdmin.getBUName),
    url(r'^api/admin/getStudentsByStage', applyAdmin.getStudentsByStage),
    url(r'^api/admin/sendSortMessage', applyAdmin.sendSortMessage),
    url(r'^api/admin/onAdjust', applyAdmin.onAdjust),
    url(r'^api/admin/getSigned', applyAdmin.getSigned),

    url(r'^api/admin/createQueue', applyAdmin.createQueue),
    url(r'api/admin/createApply', applyAdmin.createApply),

    url(r'^admin/login', applyAdmin.adminHomeLogin),
    url(r'^admin', applyAdmin.adminHome),

    url(r'^login', views.homeLogin),
    url(r'^service-worker.js', views.serviceWorker),
    url(r'^$', views.home),
]
