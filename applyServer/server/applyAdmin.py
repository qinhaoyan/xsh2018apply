from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.core.paginator import Paginator
from server.models import Students,Asp,BUInformation,Admins,Queue
from qcloudsms_py import SmsSingleSender
from qcloudsms_py.httpclient import HTTPError
import time
import json
import hashlib
import requests
import pdb

sms_type = 0
ssender = SmsSingleSender("", "")
sms_sign = "重邮学生会"

def translateBU(asp):
    if asp == '1':
        BU = '综合部'
    if asp == '2':
        BU = '学习部'
    if asp == '3':
        BU = '宣传部'
    if asp == '4':
        BU = '权益提案部'
    if asp == '5':
        BU = '生活服务部'
    if asp == '6':
        BU = '文艺部'
    if asp == '7':
        BU = '体育部'
    if asp == '8':
        BU = '女生部'
    return BU

def genearteMD5(str):
    h1 = hashlib.md5()
    h1.update(str.encode(encoding = 'utf-8'))
    return h1.hexdigest();

def adminHome(request):
    name = request.session.get('name')
    if name:
        return render(request, 'adminIndex.html')
    else:
        return HttpResponseRedirect('/admin/login')
    
def adminHomeLogin(request):
    return render(request, 'adminIndex.html')

def adminLogin(request):
    try:
        name = request.POST['name']
        passWord = genearteMD5(request.POST['pwd'] + 'dhaf12jf-')
        print(name,passWord)
        re = Admins.objects.get(name = name, passWord = passWord)
        request.session['name'] = name
        request.session['BU'] = re.BU
        request.session.set_expiry(0)
        data = {
            'success': True,
            'message': '登录成功',
            'status': 4,
            'data':{
                'success': 2,
                'message': '登录成功'
            }
        }
        return HttpResponse(json.dumps(data),content_type="application/json")
    except Exception as e:
        data = {
            'success': True,
            'message': '密码或用户名错误',
            'status': 4,
            'data':{
                'success': 1,
                'message': '密码或用户名错误'
            }
        }
        return HttpResponse(json.dumps(data),content_type="application/json")

def getInformation(request):
    name = request.session.get('name')
    BU = request.session.get('BU')
    if not BU or not name:
        data = {
            'success': True,
            'message': '没有权限，请重新登录',
            'status': 4,
            'data':{
                'success': 0,
                'message': '没有权限，请重新登录',
            }
        }
        return HttpResponse(json.dumps(data),content_type="application/json")
    else:
        order = request.GET['order']
        asp_list = Asp.objects.filter(BU = BU).order_by('-'+order)
        paginator = Paginator(asp_list, 20)
        page = int(request.GET['page'])
        asp_lists = paginator.page(page)
        re_list = []
        for asp in asp_lists:
            tel = asp.tel
            stu = Students.objects.filter(tel = tel)
            if stu[0].sex == '1':
                sex = '男'
            else:
                sex = '女'
            re_list.append({
                'name': stu[0].name,
                'stu_id': stu[0].stu_id,
                'sex': sex,
                'academy': stu[0].academy,
                'tel': stu[0].tel,
                'QQ': stu[0].QQ,
                'asp': stu[0].asp,
                'scale1': asp.scale1,
                'scale2': asp.scale2,
                'scale3': asp.scale3,
                'applyStatus': asp.applyStatus,
                'isAdjust': stu[0].isAdjust,
                'isAdjusted': asp.isAdjust
            })
        data = {
            'success': True,
            'message': '获取成功',
            'status': 4,
            'data':{
                'success': 2,
                'message': '获取成功',
                'list': re_list,
                'curentpage': page,
                'count': len(asp_list)
            }
        }
        return HttpResponse(json.dumps(data),content_type="application/json")

def stage(request):
    name = request.session.get('name')
    BU = request.session.get('BU')
    if not BU or not name:
        data = {
            'success': True,
            'message': '没有权限，请重新登录',
            'status': 4,
            'data':{
                'success': 0,
                'message': '没有权限，请重新登录',
            }
        }
        return HttpResponse(json.dumps(data),content_type="application/json")
    else:
        BUStage = BUInformation.objects.get(BU = BU)
        data = {
            'success': True,
            'message': '获取成功',
            'status': 4,
            'data':{
                'success': 2,
                'message': '获取成功',
                'stage': BUStage.stage
            }
        }
        return HttpResponse(json.dumps(data),content_type="application/json")

def changeStage(request):
    name = request.session.get('name')
    BU = request.session.get('BU')
    if not BU or not name:
        data = {
            'success': True,
            'message': '没有权限，请重新登录',
            'status': 4,
            'data':{
                'success': 0,
                'message': '没有权限，请重新登录',
            }
        }
        return HttpResponse(json.dumps(data),content_type="application/json")
    else:
        try:
            newStage = request.POST['type']
            oldStage = BUInformation.objects.get(BU = BU)
            oldStage.stage = newStage
            oldStage.save()
            fallSend = []
            if int(newStage) == 1:
                unPass_list = Asp.objects.filter(BU = BU, applyStatus = 203)
                for unPass in unPass_list:
                    result = ssender.send_with_param(86, unPass.tel, 208201, [unPass.name, translateBU(BU)], sign=sms_sign, extend="", ext="123")
                    if result['result'] != 0:
                        fallSend.append(unPass.tel)
                asp_list = Asp.objects.filter(BU = BU, applyStatus__in = [101,105,200,201,202,203]).update(applyStatus = 204)
            if int(newStage) == 2:
                unPass_list = Asp.objects.filter(BU = BU, applyStatus = 303)
                for unPass in unPass_list:
                    result = ssender.send_with_param(86, unPass.tel, 208201, [unPass.name, translateBU(BU)], sign=sms_sign, extend="", ext="123")
                    if result['result'] != 0:
                        fallSend.append(unPass.tel)
                asp_list = Asp.objects.filter(BU = BU, applyStatus__in = [205,300,301,302,303]).update(applyStatus = 304)
            if int(newStage) == 3:
                unPass_list = Asp.objects.filter(BU = BU, applyStatus = 403)
                for unPass in unPass_list:
                    result = ssender.send_with_param(86, unPass.tel, 208201, [unPass.name, translateBU(BU)], sign=sms_sign, extend="", ext="123")
                    if result['result'] != 0:
                        fallSend.append(unPass.tel)
                asp_list = Asp.objects.filter(BU = BU, applyStatus__in = [305,400,401,402,403]).update(applyStatus = 404)
            queue = Queue.objects.get(BU = BU)
            queue.queue = ''
            queue.save()
            data = {
                'success': True,
                'message': '修改成功',
                'status': 4,
                'data':{
                    'success': 2,
                    'message': '修改成功',
                    'stage': newStage,
                    'fallSend': fallSend
                }
            }
            return HttpResponse(json.dumps(data),content_type="application/json")
        except Exception as e:
            data = {
                'success': True,
                'message': '修改失败',
                'status': 4,
                'data':{
                    'success': 0,
                    'message': '修改失败',
                }
            }
            return HttpResponse(json.dumps(data),content_type="application/json")

def passStage(request):
    name = request.session.get('name')
    BU = request.session.get('BU')
    if not BU or not name:
        data = {
            'success': True,
            'message': '没有权限，请重新登录',
            'status': 4,
            'data':{
                'success': 0,
                'message': '没有权限，请重新登录',
            }
        }
        return HttpResponse(json.dumps(data),content_type="application/json")
    else:
        try:
            typeStage = request.POST['type']
            tel = request.POST['tel']
            stu = Asp.objects.get(tel = tel, BU = BU)
            stu.applyStatus = (int(typeStage)+1)*100 + 5
            stu.save()
            data = {
                'success': True,
                'message': '修改成功',
                'status': 4,
                'data':{
                    'success': 2,
                    'message': '修改成功',
                    'applyStatus': (int(typeStage)+1)*100 + 5 
                }
            }
            return HttpResponse(json.dumps(data),content_type="application/json")
        except Exception as e:
            data = {
                'success': True,
                'message': '修改失败',
                'status': 4,
                'data':{
                    'success': 0,
                    'message': '修改失败',
                }
            }
            return HttpResponse(json.dumps(data),content_type="application/json")

def search(request):
    name = request.session.get('name')
    BU = request.session.get('BU')
    if not BU or not name:
        data = {
            'success': True,
            'message': '没有权限，请重新登录',
            'status': 4,
            'data':{
                'success': 0,
                'message': '没有权限，请重新登录',
            }
        }
        return HttpResponse(json.dumps(data),content_type="application/json")
    else:
        searchType = request.GET['type']
        value = request.GET['value']
        if searchType == '1':
            stu = Asp.objects.filter(name__icontains = value, BU = BU)
        else:
            stu = Asp.objects.filter(tel__icontains = value, BU = BU)
        paginator = Paginator(stu, 20)
        page = 1
        asp_lists = paginator.page(page)
        re_list = []
        count = len(stu)
        for asp in asp_lists:
            tel = asp.tel
            stu = Students.objects.get(tel = tel)
            if stu.sex == '1':
                sex = '男'
            else:
                sex = '女'
            re_list.append({
                'name': stu.name,
                'stu_id': stu.stu_id,
                'sex': sex,
                'academy': stu.academy,
                'tel': stu.tel,
                'QQ': stu.QQ,
                'asp': stu.asp,
                'scale1': asp.scale1,
                'scale2': asp.scale2,
                'scale3': asp.scale3,
                'applyStatus': asp.applyStatus
            })
        data = {
            'success': True,
            'message': '获取成功',
            'status': 4,
            'data':{
                'success': 2,
                'message': '获取成功',
                'list': re_list,
                'curentpage': page,
                'count': count
            }
        }
        return HttpResponse(json.dumps(data),content_type="application/json")

def getDetail(request):
    name = request.session.get('name')
    BU = request.session.get('BU')
    if not BU or not name:
        data = {
            'success': True,
            'message': '没有权限，请重新登录',
            'status': 4,
            'data':{
                'success': 0,
                'message': '没有权限，请重新登录',
            }
        }
        return HttpResponse(json.dumps(data),content_type="application/json")
    else:
        try:
            tel = request.GET['tel']
            stu = Students.objects.get(tel = tel)
            asp = Asp.objects.get(tel = tel, BU = BU)
            data = {
                'success': True,
                'message': '获取成功',
                'status': 4,
                'data':{
                    'success': 2,
                    'message': '获取成功',
                    'name': stu.name,
                    'sex': stu.sex,
                    'stu_id': stu.stu_id,
                    'academy': stu.academy,
                    'tel': stu.tel,
                    'QQ': stu.QQ,
                    'email': stu.email,
                    'asp': stu.asp,
                    'isAdjust': int(stu.isAdjust),
                    'character': stu.character,
                    'resume': stu.resume,
                    'audition1': asp.audition1,
                    'scale1': asp.scale1,
                    'audition2': asp.audition2,
                    'scale2': asp.scale2,
                    'audition3': asp.audition3,
                    'scale3': asp.scale3,
                }
            }
            return HttpResponse(json.dumps(data),content_type="application/json")
        except Exception as e:
             data = {
            'success': True,
            'message': '数据库错误，请联系管理员',
            'status': 4,
            'data':{
                'success': 1,
                'message': '数据库错误，请联系管理员',
            }
        }
        return HttpResponse(json.dumps(data),content_type="application/json")

def getPic(request):
    stu_id = request.GET['stu_id']
    pic = requests.get('http://jwzx.cqupt.edu.cn/showstupic.php?xh=' + stu_id)
    return HttpResponse(pic.content,content_type="image/png")

def commits(request):
    name = request.session.get('name')
    BU = request.session.get('BU')
    if not BU or not name:
        data = {
            'success': True,
            'message': '没有权限，请重新登录',
            'status': 4,
            'data':{
                'success': 0,
                'message': '没有权限，请重新登录',
            }
        }
        return HttpResponse(json.dumps(data),content_type="application/json")
    else:
        try:
            stage = BUInformation.objects.get(BU = BU).stage 
            audition1 = request.POST.get('audition1')
            audition2 = request.POST.get('audition2')
            audition3 = request.POST.get('audition3')
            scale1 = request.POST['scale1']
            scale2 = request.POST['scale2']
            scale3 = request.POST['scale3']
            tel = request.POST['tel']
            asp = Asp.objects.get(tel = tel, BU = BU)
            if audition1:
                asp.audition1 = audition1
            if audition2:
                asp.audition2 = audition2
            if audition3:
                asp.audition3 = audition3
            asp.scale1 = float(scale1)
            asp.scale2 = float(scale2)
            asp.scale3 = float(scale3)
            if stage == '0':
                asp.applyStatus = 203
            if stage == '1':
                asp.applyStatus = 303
            if stage == '2':
                asp.applyStatus = 403
            asp.save()
            data = {
                'success': True,
                'message': '成功',
                'status': 4,
                'data':{
                    'success': 2,
                    'message': '成功',
                }
            }
            return HttpResponse(json.dumps(data),content_type="application/json")
        except Exception as e:
            data = {
                'success': True,
                'message': '失败',
                'status': 4,
                'data':{
                    'success': 1,
                    'message': '失败',
                }
            }
            return HttpResponse(json.dumps(data),content_type="application/json")

def begin(request):
    name = request.session.get('name')
    BU = request.session.get('BU')
    if not BU or not name:
        data = {
            'success': True,
            'message': '没有权限，请重新登录',
            'status': 4,
            'data':{
                'success': 0,
                'message': '没有权限，请重新登录',
            }
        }
        return HttpResponse(json.dumps(data),content_type="application/json")
    else:
        try:
            BUqueue = Queue.objects.get(BU = BU)
            queue = BUqueue.queue.split(',')
            tel = queue[0]
            if tel :
                #admin = Admins.objects.get(BU = BU)
                name = request.session.get('name')
                order = name[-1]
                nextStu = Students.objects.get(tel = tel)
                params = [nextStu.name, translateBU(BU), order]
                result = ssender.send_with_param(86, tel, 205789, params, sign=sms_sign, extend="", ext="123")
                #result = {'errmsg':'OK','result':0}
                code = 2
                message = result['errmsg']
                if result['result'] != 0:
                    code = 3
                str_queue = ','.join(queue[1:])
                BUqueue.queue = str_queue
                BUqueue.save()
                data = {
                    'success': True,
                    'message': '成功',
                    'status': 4,
                    'data':{
                        'success': code,
                        'message': message,
                        'tel': tel
                    }
                }
            else:
                data = {
                    'success': True,
                    'message': '暂无数据',
                    'status': 4,
                    'data':{
                        'success': 4,
                        'message': '暂无数据',
                        'tel': ''
                    }
                }
            return HttpResponse(json.dumps(data),content_type="application/json")
        except Exception as e:
            data = {
                'success': True,
                'message': '失败',
                'status': 4,
                'data':{
                    'success': 1,
                    'message': '失败',
                }
            }
            return HttpResponse(json.dumps(data),content_type="application/json")

def next(request):
    name = request.session.get('name')
    BU = request.session.get('BU')
    if not BU or not name:
        data = {
            'success': True,
            'message': '没有权限，请重新登录',
            'status': 4,
            'data':{
                'success': 0,
                'message': '没有权限，请重新登录',
            }
        }
        return HttpResponse(json.dumps(data),content_type="application/json")
    else:
        try:
            #preTel = request.POST['tel']
            #preStu = Asp.objects.get(BU = BU, tel = preTel)
            #admin = Admins.objects.get(BU = BU)
            name = request.session.get('name')
            order = name[-1]
            #BUInfor = BUInformation.objects.get(BU = BU)
            #stage = int(BUInfor.stage)
            #if stage == 3:
            #    stage = 2
            #if preStu.applyStatus == (stage + 2) * 100 + 1:
            #    preStu.applyStatus = (stage + 2) * 100 + 3
            #preStu.save()
            BUqueue = Queue.objects.get(BU = BU)
            queue = BUqueue.queue.split(',')
            tel = queue[0]
            if tel:
                nextStu = Students.objects.get(tel = tel)
                params = [nextStu.name, translateBU(BU), order]
                #tel = nextStu.tel
                result = ssender.send_with_param(86, tel, 205789, params, sign=sms_sign, extend="", ext="123")
                #result = {'errmsg':'OK','result':0}
                code = 2
                if result['result'] != 0:
                    code = 3
                str_queue = ','.join(queue[1:])
                BUqueue.queue = str_queue
                BUqueue.save()
                data = {
                    'success': True,
                    'message': '成功',
                    'status': 4,
                    'data':{
                        'success': code,
                        'message': '成功',
                        'tel': tel,
                    }
                }
            else:
                data = {
                    'success': True,
                    'message': '暂无数据',
                    'status': 4,
                    'data':{
                        'success': 4,
                        'message': '暂无数据',
                        'tel': '',
                    }
                }
            return HttpResponse(json.dumps(data),content_type="application/json")
        except Exception as e:
            data = {
                'success': True,
                'message': '失败',
                'status': 4,
                'data':{
                    'success': 1,
                    'message': '失败',
                }
            }
            return HttpResponse(json.dumps(data),content_type="application/json")

def getBUName(request):
    name = request.session.get('name')
    BU = request.session.get('BU')
    if not BU or not name:
        data = {
            'success': True,
            'message': '没有权限，请重新登录',
            'status': 4,
            'data':{
                'success': 0,
                'message': '没有权限，请重新登录',
            }
        }
        return HttpResponse(json.dumps(data),content_type="application/json")
    else:
        data = {
            'success': True,
            'message': '成功',
            'status': 4,
            'data':{
                'success': 2,
                'message': '成功',
                'BU': translateBU(BU)
            }
        }
        return HttpResponse(json.dumps(data),content_type="application/json")

def getStudentsByStage(request):
    name = request.session.get('name')
    BU = request.session.get('BU')
    if not BU or not name:
        data = {
            'success': True,
            'message': '没有权限，请重新登录',
            'status': 4,
            'data':{
                'success': 0,
                'message': '没有权限，请重新登录',
            }
        }
        return HttpResponse(json.dumps(data),content_type="application/json")
    else:
        try:
            stage = request.GET['stage']
            if stage == '1':
                asp = Asp.objects.filter(BU = BU, applyStatus__in = [101, 105, 200])
            else:
                asp = Asp.objects.filter(BU = BU, applyStatus__in = [(int(stage) * 100 +5), (int(stage)+1) * 100])
            data_list = []
            for item in asp:
                data_list.append({
                    'applyStatus': item.applyStatus,
                    'name': item.name,
                    'tel': item.tel
                })
            data = {
                'success': True,
                'message': '获取成功',
                'status': 4,
                'data':{
                    'success': 2,
                    'message': '获取成功',
                    'list': data_list
                }
            }
            return HttpResponse(json.dumps(data),content_type="application/json")
        except Exception as e:
            data = {
                'success': True,
                'message': '获取失败',
                'status': 4,
                'data':{
                    'success': 1,
                    'message': '获取失败',
                }
            }
            return HttpResponse(json.dumps(data),content_type="application/json")

def sendSortMessage(request):
    name = request.session.get('name')
    BU = request.session.get('BU')
    if not BU or not name:
        data = {
            'success': True,
            'message': '没有权限，请重新登录',
            'status': 4,
            'data':{
                'success': 0,
                'message': '没有权限，请重新登录',
            }
        }
        return HttpResponse(json.dumps(data),content_type="application/json")
    else:
        try:
            tel_list = request.POST['data'].split(',')
            input_list = request.POST['input'].split(',')
            sortMessageType = request.POST['type']
            stu_list = []
            for tel in tel_list:
                stu = Students.objects.get(tel = tel)
                stu_list.append({
                    'tel': stu.tel,
                    'params': [stu.name, translateBU(BU)] + input_list
                })
            if sortMessageType == '1':
                template_id = 205853
            if sortMessageType == '2':
                template_id = 205852
            if sortMessageType == '3':
                template_id = 205854
            if sortMessageType == '4':
                template_id = 205252
            errList = []
            for stu in  stu_list:
                result = ssender.send_with_param(86, stu['tel'], template_id, stu['params'], sign=sms_sign, extend="", ext="123")
                #result = {'errmsg':'OK','result':0}
                if result['result'] == 0 and int(sortMessageType) < 4:
                    asp = Asp.objects.get(tel = stu['tel'], BU = BU)
                    asp.applyStatus = (int(sortMessageType) + 1) * 100
                    asp.save()
                else:
                    errList.append(stu['tel'])
            if len(errList) == 0:
                data = {
                    'success': True,
                    'message': '发送完成',
                    'status': 4,
                    'data':{
                        'success': 2,
                        'message': '发送完成',
                    }
                }
            else:
                data = {
                    'success': True,
                    'message': '发送未完成',
                    'status': 4,
                    'data':{
                        'success': 3,
                        'message': '发送未完成',
                        'errList': errList
                    }
                }
            return HttpResponse(json.dumps(data),content_type="application/json")
        except Exception as e:
            data = {
                'success': True,
                'message': '发送失败',
                'status': 4,
                'data':{
                    'success': 1,
                    'message': '发送失败',
                }
            }
            return HttpResponse(json.dumps(data),content_type="application/json")
        
def onAdjust(request):
    name = request.session.get('name')
    BU = request.session.get('BU')
    if not BU or not name:
        data = {
            'success': True,
            'message': '没有权限，请重新登录',
            'status': 4,
            'data':{
                'success': 0,
                'message': '没有权限，请重新登录',
            }
        }
        return HttpResponse(json.dumps(data),content_type="application/json")
    else:
        try:
            newBU = request.POST['BU']
            tel = request.POST['tel']
            asp = Asp.objects.get(tel = tel, BU = BU)
            asp.BU = newBU
            asp.isAdjust = 1
            if asp.applyStatus == 204:
                asp.applyStatus = 203
            if asp.applyStatus == 304:
                asp.applyStatus = 303
            if asp.applyStatus == 404:
                asp.applyStatus = 403
            asp.save()
            data = {
                'success': True,
                'message': '完成',
                'status': 4,
                'data':{
                    'success': 2,
                    'message': '完成',
                }
            }
            return HttpResponse(json.dumps(data),content_type="application/json")
        except Exception as e:
            data = {
                'success': True,
                'message': '失败',
                'status': 4,
                'data':{
                    'success': 1,
                    'message': '失败',
                }
            }
            return HttpResponse(json.dumps(data),content_type="application/json")

def getSigned(request):
    name = request.session.get('name')
    BU = request.session.get('BU')
    if not BU or not name:
        data = {
            'success': True,
            'message': '没有权限，请重新登录',
            'status': 4,
            'data':{
                'success': 0,
                'message': '没有权限，请重新登录',
            }
        }
        return HttpResponse(json.dumps(data),content_type="application/json")
    else:
        try:
            tel_list = Queue.objects.get(BU = BU).queue.split(',')
            re_list = []
            for tel in tel_list:
                stu = Students.objects.get(tel = tel)
                if stu.sex == '1':
                    sex = '男'
                else:
                    sex = '女'
                re_list.append({
                    'name': stu.name,
                    'stu_id': stu.stu_id,
                    'sex': sex,
                    'academy': stu.academy,
                    'tel': stu.tel,
                    'QQ': stu.QQ,
                    'asp': stu.asp
                })
            data = {
                'success': True,
                'message': '获取成功',
                'status': 4,
                'data':{
                    'success': 2,
                    'message': '获取成功',
                    'list': re_list,
                }
            }
            return HttpResponse(json.dumps(data),content_type="application/json")
        except Exception as e:
            data = {
                'success': True,
                'message': '获取失败',
                'status': 4,
                'data':{
                    'success': 1,
                    'message': '获取失败',
                    'list': re_list,
                }
            }
            return HttpResponse(json.dumps(data),content_type="application/json")

def createQueue(request):
    BU = request.GET['BU']
    pdb
    Queue.objects.create(BU = BU)
    return HttpResponse(json.dumps({'data':1}),content_type="application/json")

def createApply(request):
    try:
        name = request.GET['name']
        sex = request.GET['sex']
        stu_id = request.GET['stu_id']
        academy = request.GET['academy']
        tel = request.GET['tel']
        BU = request.GET['BU']
        QQ = request.GET.get('QQ')
        try:
            stu =  Students.objects.get(tel = tel)
            i = len(stu.asp.split(' ')) +1
            stu.asp = stu.asp + ' ' + str(i) + '.' + translateBU(BU)
            stu.save()
        except Exception as e:
            if QQ:
                Students.objects.create(
                    name = name,
                    sex = sex,
                    stu_id = stu_id,
                    academy = academy,
                    tel = tel,
                    QQ = QQ,
                    isAdjust = 1,
                    asp = '1.' + translateBU(BU),
                    character = '未完成测评',
                    characterStage = 0
                )
            else:
                Students.objects.create(
                    name = name,
                    sex = sex,
                    stu_id = stu_id,
                    academy = academy,
                    tel = tel,
                    isAdjust = 1,
                    asp = '1.' + translateBU(BU),
                    character = '未完成测评',
                    characterStage = 0
                )
        Asp.objects.create(
            name = name,
            stu_id = stu_id,
            BU = BU,
            tel = tel,
            isAdjust = 0,
            applyStatus = 101,
            order = 1,
            scale1 = 0,
            scale2 = 0,
            scale3 = 0
        )
        return HttpResponse(json.dumps({'data':1}),content_type="application/json")
    except Exception as e:
        return HttpResponse(json.dumps({'data':0}),content_type="application/json")

        
        


       

          


         
       
        





        
    


