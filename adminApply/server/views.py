from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.core.paginator import Paginator
from server.models import Students,Asp,BUInformation,Admins,Queue
from qcloudsms_py import SmsSingleSender
from qcloudsms_py.httpclient import HTTPError
import time
import json
import random
import pdb

sms_type = 0
ssender = SmsSingleSender("1400145946", "a346cb074a15dd26680c61b6ba21894d")
sms_sign = "重邮学生会"

testAnswer = [
    '意志力强，头脑冷静，有较强的领导欲，事业心强，不达目的不罢休。外表和善，内心自傲，对有利于自己的人际关系比较看重，有时显得性格急噪，咄咄逼人，得理不饶人，不利于自己时顽强抗争，不轻易认输。思维理性，对爱情和婚姻的看法很现实，对金钱的欲望一般。',
    '聪明，性格活泼，人缘好，善于交朋友，心机较深。事业心强，渴望成功。思维较理性，崇尚爱情，但当爱情与婚姻发生冲突时会选择有利于自己的婚姻。金钱欲望强烈。',
    '爱幻想，思维较感性，以是否与自己投缘为标准来选择朋友。性格显得较孤傲，有时较急噪，有时优柔寡断。事业心较强，喜欢有创造性的工作，不喜欢按常规办事。性格倔强，言语犀利，不善于妥协。崇尚浪漫的爱情，但想法往往不切合实际。金钱欲望一般。',
    '好奇心强，喜欢冒险，人缘较好。事业心一般，对待工作，随遇而安，善于妥协。善于发现有趣的事情，但耐心较差，敢于冒险，但有时较胆小。渴望浪漫的爱情，但对婚姻的要求比较现实。不善理财。',
    '性情温良，重友谊，性格塌实稳重，但有时也比较狡黠。事业心一般，对本职工作能认真对待，但对自己专业以外事物没有太大兴趣，喜欢有规律的工作和生活，不喜欢冒险，家庭观念强，比较善于理财。',
    '散漫，爱玩，富于幻想。聪明机灵，待人热情，爱交朋友，但对朋友没有严格的选择标准。事业心较差，更善于享受生活，意志力和耐心都较差，我行我素。有较好的异性缘，但对爱情不够坚持认真，容易妥协。没有财产观念。'
]

# Create your views here.
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

def home(request):
    request.session['preTime'] = int(time.time())
    return render(request, 'index.html')

def homeLogin(request):
    return render(request, 'index.html')

def serviceWorker(request):
    return render(request, 'service-worker.js')

def apply(request):
    try:
        code = int(request.POST['code'])
        tel = request.POST['tel']
        verificationCode = request.session.get('verificationCode')
        sessionTel = request.session.get('tel')
        if code == verificationCode and sessionTel == tel:
            stu = Students.objects.filter(tel = tel)
            if stu:
                data = {
                    'success': True,
                    'message': '该手机号已被注册，如非本人操作，请联系管理员',
                    'status': 4,
                    'data':{
                        'success': 4,
                        'message': '该学号已被注册，如非本人操作，请联系管理员',
                    }
                }
                return HttpResponse(json.dumps(data),content_type="application/json")
            stu_id = request.POST['stu_id']
            name = request.POST['name']
            sex = request.POST['sex']
            QQ = request.POST['QQ']
            email = request.POST['email']
            academy = request.POST['academy']
            isAdjust = request.POST['isAdjust']
            resume = request.POST['resume']
            asp1 = request.POST['asp1']
            asp2 = request.POST['asp2']
            asp3 = request.POST['asp3']
            asp = '1.' + translateBU(asp1)
            code = 2
            message = '报名成功'
            if asp2 != '':
                asp += ' 2.' + translateBU(asp2)
            if asp3 != '':
                asp += ' 3.' + translateBU(asp3)
            Students.objects.create(
                name = name,
                stu_id = stu_id,
                sex = sex,
                tel = tel,
                QQ = QQ,
                email = email,
                academy = academy,
                isAdjust = isAdjust,
                resume = resume,
                asp = asp,
                characterStage = 0,
                character = '未完成测评'
            )
            try:
                Asp.objects.create(
                    name = name,
                    stu_id = stu_id,
                    BU = asp1,
                    tel = tel,
                    isAdjust = 0,
                    applyStatus = 101,
                    order = 1,
                    scale1 = 0,
                    scale2 = 0,
                    scale3 = 0
                )
                if asp2 != '':
                    Asp.objects.create(
                        name = name,
                        stu_id = stu_id,
                        BU = asp2,
                        tel = tel,
                        isAdjust = 0,
                        applyStatus = 101,
                        order = 2,
                        scale1 = 0,
                        scale2 = 0,
                        scale3 = 0
                    )
                    
                if asp3 != '':
                    Asp.objects.create(
                        name = name,
                        stu_id = stu_id,
                        BU = asp3,
                        tel = tel,
                        isAdjust = 0,
                        applyStatus = 101,
                        order = 3,
                        scale1 = 0,
                        scale2 = 0,
                        scale3 = 0
                    )
                    
                request.session['tel'] = tel
            except Exception as e:
                code = 1
                message = '报名失败'
                Students.objects.filter(tel = tel).delete()
                Asp.objects.filter(tel = tel).delete()
            
            data = {
                'success': True,
                'message': message,
                'status': 4,
                'data':{
                    'success':  code,
                    'message': message,
                }
            }
            return HttpResponse(json.dumps(data),content_type="application/json")
        else:
            data = {
                'success': True,
                'message': '验证码错误',
                'status': 4,
                'data':{
                    'success': 0,
                    'message': '验证码错误',
                }
            }
            return HttpResponse(json.dumps(data),content_type="application/json")
    except Exception as e:
        data = {
            'success': True,
            'message': '报名失败',
            'status': 4,
            'data':{
                'success': 1,
                'message': '报名失败',
            }
        }
        return HttpResponse(json.dumps(data),content_type="application/json")

def getVerificationCode(request):
    nowTime = int(time.time())
    preTime = request.session.get('preTime')
    flag = False
    if preTime:
        if nowTime - int(preTime) < 60:
            data = {
                'success': True,
                'message': '操作太快啦，校会君思考跟不上啦',
                'status': 4,
                'data':{
                    'success': 0,
                    'message': '操作太快啦，校会君思考跟不上啦',
                }
            }
            return HttpResponse(json.dumps(data),content_type="application/json")
        else:
            request.session['preTime'] = nowTime
            flag = True
    else:
        data = {
            'success': True,
            'message': '短信是要钱的',
            'status': 4,
            'data':{
                'success': 0,
                'message': '短信是要钱的',
            }
        }
        return HttpResponse(json.dumps(data),content_type="application/json")
    if flag:
        verificationCode = random.randint(1000,9999)
        tel = request.POST['tel']
        template_id = 205255
        params = [verificationCode,"10"]
        message = '获取成功'
        code = 2
        try:
            result = ssender.send_with_param(86, tel, template_id, params, sign=sms_sign, extend="", ext="123")
            message = result['errmsg']
            if result['result'] != 0:
                code = 1
            if result['result'] == 1016:
                code = 3
            if result['result'] == 0:
                request.session['verificationCode'] = verificationCode
                request.session['tel'] = tel
        except HTTPError as e:
            message = e
            code = 1
        except Exception as e:
            message = e
            code = 1
        data = {
            'success': True,
            'message': message,
            'status': 4,
            'data':{
                'success': code,
                'message': message,
            }
        }
        return HttpResponse(json.dumps(data),content_type="application/json")

def login(request):
    try:
        stu_id = request.POST['stu_id']
        tel = request.POST['tel']
        re = Students.objects.get(stu_id = stu_id, tel = tel)
        request.session['tel'] = tel
        data = {
            'success': True,
            'message': '成功',
            'status': 4,
            'data':{
                'success': 2,
                'message': '成功',
                'name': re.name
            }
        }
        return HttpResponse(json.dumps(data),content_type="application/json")
    except Exception as e:
        data = {
            'success': True,
            'message': '学号和注册手机不匹配',
            'status': 4,
            'data':{
                'success': 0,
                'message': '学号和注册手机不匹配',
            }
        }
        return HttpResponse(json.dumps(data),content_type="application/json")

def testResult(request):
    try:
        tel = request.session.get('tel')
        testScale = int(request.POST['testScale'])
        if testScale >= 180:
            answer = testAnswer[0]
        if testScale < 179 and testScale >= 140:
            answer = testAnswer[1]
        if testScale < 139 and testScale >= 100:
            answer = testAnswer[2]
        if testScale < 99 and testScale >= 70:
            answer = testAnswer[3]
        if testScale < 69 and testScale >= 40:
            answer = testAnswer[4]
        if testScale < 40:
            answer = testAnswer[5]
        stu = Students.objects.get(tel = tel)
        stu.characterStage = 1
        stu.character = answer
        stu.save()
        Asp.objects.filter(tel = tel, applyStatus = 101).update(applyStatus = 105)
        data = {
            'success': True,
            'message': '提交成功',
            'status': 4,
            'data':{
                'success': 2,
                'message': '提交成功',
            }
        }
        return HttpResponse(json.dumps(data),content_type="application/json")

    except Exception as e:
        data = {
            'success': True,
            'message': '提交失败',
            'status': 4,
            'data':{
                'success': 0,
                'message': '提交失败，请重试',
            }
        }
        return HttpResponse(json.dumps(data),content_type="application/json")

def getApplyStatus(request):
    try:
        tel = request.session.get('tel')
        if tel:
            asps = Asp.objects.filter(tel = tel)
            stu = Students.objects.get(tel = tel)
            data_list = []
            for asp in asps:
                if asp.BU:
                    if asp.isAdjust == '1':
                        BU = translateBU(asp.BU) + '(调剂)'
                    else:
                        BU = translateBU(asp.BU)
                    data_list.append({
                        'BU': BU,
                        'applyStatus': asp.applyStatus,
                        'order': asp.order
                    })
            data = {
                'success': True,
                'message': '获取成功',
                'status': 4,
                'data':{
                    'success': 2,
                    'message': '获取成功',
                    'list': data_list,
                    'characterStage': stu.characterStage
                }
            }
            return HttpResponse(json.dumps(data),content_type="application/json")
        else:
            data = {
                'success': True,
                'message': '请重新登录',
                'status': 4,
                'data':{
                    'success': 1,
                    'message': '请重新登录',
                }
            }
            return HttpResponse(json.dumps(data),content_type="application/json")
    except Exception as e:
        data = {
            'success': True,
            'message': '获取失败',
            'status': 4,
            'data':{
                'success': 0,
                'message': '获取失败',
            }
        }
        return HttpResponse(json.dumps(data),content_type="application/json")

def signIn(request):
    try:
        BU = request.GET['BU']
        pdb.set_trace()
        tel = request.session.get('tel')
        if tel:
            stu = Asp.objects.get(tel = tel, BU = BU)
            if stu.applyStatus not in [204, 304, 404]:
                queue_list = Queue.objects.get(BU = BU)
                queue = queue_list.queue
                if tel not in queue.split(','):
                    if queue:
                        queue += ','+tel
                    else:
                        queue = tel
                    queue_list.queue = queue
                    queue_list.save()
                    if stu.applyStatus in [101, 105, 200]:
                        stu.applyStatus = 201
                    if stu.applyStatus in [205, 300]:
                        stu.applyStatus = 301
                    if stu.applyStatus in [305, 400]:
                        stu.applyStatus = 401
                    stu.save()
                    return HttpResponseRedirect('/signSuccess')
                else:
                    return HttpResponseRedirect('/signFailing?status=0')
            else:
                return HttpResponseRedirect('/signFailing?status=1')
        else:
            return HttpResponseRedirect('/login?BU='+BU)

    except Exception as e:
        return HttpResponseRedirect('/')

def loginSignIn(request):
    try:
        BU = request.GET['BU']
        tel = request.session.get('tel')
        if tel:
            stu = Asp.objects.get(tel = tel, BU = BU)
            if stu.applyStatus not in [204, 304, 404]:
                queue_list = Queue.objects.get(BU = BU)
                queue = queue_list.queue
                li_queue = queue.split(',')
                if tel not in li_queue:
                    if queue:
                        queue += ','+tel
                    else:
                        queue = tel
                    queue_list.queue = queue
                    queue_list.save()
                    if stu.applyStatus in [101, 105, 200]:
                        stu.applyStatus = 201
                    if stu.applyStatus in [205, 300]:
                        stu.applyStatus = 301
                    if stu.applyStatus in [305, 400]:
                        stu.applyStatus = 401
                    stu.save() 
                    data = {
                        'success': True,
                        'message': '签到成功',
                        'status': 4,
                        'data':{
                            'success': 2,
                            'message': '签到成功',
                        }
                    }
                else:
                    data = {
                        'success': True,
                        'message': '请勿重复签到',
                        'status': 4,
                        'data':{
                            'success': 4,
                            'message': '请勿重复签到',
                        }
                    }
                return HttpResponse(json.dumps(data),content_type="application/json")
            else:
                data = {
                    'success': True,
                    'message': '没有签到权限',
                    'status': 4,
                    'data':{
                        'success': 3,
                        'message': '没有签到权限',
                    }
                }
                return HttpResponse(json.dumps(data),content_type="application/json")
        else:
            return HttpResponseRedirect('/login?BU='+BU)

    except Exception as e:
        data = {
            'success': True,
            'message': '请重新登录',
            'status': 4,
            'data':{
                'success': 1,
                'message': '请重新登录',
            }
        }
        return HttpResponse(json.dumps(data),content_type="application/json")