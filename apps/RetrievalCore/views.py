from django.shortcuts import render
from django.views.generic.base import View
from django.http import JsonResponse
from django.db.models import Q

import json
import apps.RetrievalCore.CommonTools as tool
from RetrievalCore.models import Document, Session, UserProfile


class DocumentListView(View):
    def get(self, request):
        """
        未实现
        验证用户是否登录
            已登录:
                查找当前用户是否有未完成的Session、没有:
                    1.从Document取出20个该用户还未打分过的文档
                    2.根据当前用户、1中取出的20个文档生成Session记录存库
                    3.返回页面（需要包含 用户实体、Session实体、Documents实体列表）
                有未完成的Session:
                    恢复session
            未登录:
                返回登录页面
        :param request:
        :return:
        """
        user_id = request.path.split("list")[1].replace("/", "")
        if len(user_id) < 1:
            return render(request, "login.html")
        user_id = int(user_id)
        user = UserProfile.objects.filter(id=user_id)
        if len(user) < 1:
            # 用户未登录
            return render(request, "login.html")
        user = user[0]
        user_sessions = Session.objects.filter(user=user, D_vector=None, P_vector=None)
        if len(user_sessions) > 0:
            # 有未完成的session
            user_session = user_sessions[0]
            documents = user_session.documents.all()
            documents = tool.sort_docs_by_dp(documents, user.get_D_vector(), user.get_P_vector())
            return render(request, "list.html", {
                "documents": documents,
                "session": user_session,
                "user_id": user_id
            })
            pass
        else:
            # 所有session都已完成
            user_sessions = Session.objects.filter(user=user)
            # user_documents = Document.objects.filter(session__user__in=list(user_sessions))
            # all_documents = Document.objects.all()
            # new_documents = all_documents.difference(user_documents)[:20]
            new_documents = Document.objects.filter(~Q(session__documents__session__in=list(user_sessions)))[:20]
            new_session = Session.objects.create(user=user, D_vector=None, P_vector=None, precision=None)
            new_session.documents.set(list(new_documents))
            new_session.save()
            new_documents = tool.sort_docs_by_dp(new_documents, user.get_D_vector(), user.get_P_vector())
            return render(request, "list.html", {
                "documents": new_documents,
                "session": new_session,
                "user_id": user_id
            })

    def post(self, request):
        """
        {
           "1":{
              "classification":3,
              "relevance":0.8
           },...
        }
        :param request:
        :return:
        """
        json_response = {
            "success": False,
            "msg": "",
            "user_id": None,
            "redirect": None
        }
        user_relevance = json.loads(request.POST.get("session_relevance"))
        user_id = request.POST.get("user_id")
        print(user_relevance)
        if len(user_id) < 1:
            json_response["redirect"] = "/user/login/"
            return JsonResponse(json_response, json_dumps_params={"ensure_ascii": False})
        user_id = int(user_id)
        user = UserProfile.objects.filter(id=user_id)
        if len(user) < 1:
            json_response["redirect"] = "/user/login/"
            return JsonResponse(json_response, json_dumps_params={"ensure_ascii": False})
        user = user[0]
        user_sessions = Session.objects.filter(user=user, D_vector=None, P_vector=None)
        if len(user_sessions) > 0:
            user_session = user_sessions[0]
            d = user.get_D_vector()
            user_d = [0 for i in range(len(d))]
            num_d = [0 for i in range(len(d))]
            if user_relevance:
                for k, v in user_relevance.items():
                    user_d[v['classification']] += v['relevance']
                    num_d[v['classification']] += 1
                for k, v in enumerate(user_d):
                    if v > 0:
                        v /= num_d[k]
            new_d = json.dumps(tool.update_d_value(d, user_d, 300))
            new_p = json.dumps(tool.update_p_value(user.get_P_vector(), new_d, 0.5))
            user_session.D_vector = new_d
            user_session.P_vector = new_p
            user.D_vector = new_d
            user.P_vector = new_p
            user_session.save()
            user.save()
            # session_documents = Document.objects.filter(session__documents__session__in=[user_session])
            json_response["redirect"] = "/user/assess/{0}/".format(user_session.id)
            return JsonResponse(json_response, json_dumps_params={"ensure_ascii": False})


class DocumentDetailView(View):
    def get(self, request, document_id, session_id):
        """
        未实现
        验证用户是否登录
            已登录:
                1.根据document_id从Document中取出该文献详细信息
                2.返回页面（需要包含 Document实体、用户实体、Session实体）
            未登录:
                返回登录页面
        :param session_id:
        :param document_id:
        :param request:
        :return:
        """
        session = Session.objects.filter(id=session_id)[0]
        document = Document.objects.filter(id=document_id)[0]
        return render(request, "doc_detail.html", {
            "document": document,
            "session": session
        })

    def post(self, request, document_id, session_id):
        """
        未实现(用户在文献详情页打分后将打分分值传至后端)
        验证用户是否登录
            已登录:
                1.根据document_id从Document中取出该文献详细信息
                2.返回页面（需要包含 Document实体、用户实体、Session实体）
            未登录:
                返回登录页面
        :param request:
        :param document_id:
        :param session_id:
        :return:
        """
        # 用户打分取值方式request.POST.get("user_relevance"),类型为float
        pass


class UserLogin(View):
    """
    用戶登录
    """
    def get(self, request):
        """
        访问用户登录界面
        :param request:
        :return:
        """
        return render(request, "login.html")

    def post(self, request):
        """
        提交登录信息(账户名，密码)
        :param request:
        :return:
        """
        json_response = {
            "success": False,
            "msg": "",
            "user_id": None,
            "redirect": None
        }
        username = request.POST.get("username")
        password = request.POST.get("password")
        if username is None or password is None:
            json_response["msg"] = "用户名或密码为空！"
            return JsonResponse(json_response, json_dumps_params={"ensure_ascii": False})
        user = UserProfile.objects.filter(username=username)
        if len(user) < 1:
            json_response["msg"] = "未找到该用户"
            return JsonResponse(json_response, json_dumps_params={"ensure_ascii": False})
        else:
            user = user[0]
        if user.password == password:
            json_response["success"] = True
            json_response["user_id"] = user.id
            print(sum(user.get_D_vector()))
            if sum(user.get_D_vector()) == 0:
                json_response["redirect"] = "/user/preference_customize/{0}/".format(user.id)
        else:
            json_response["msg"] = "密码错误"
        return JsonResponse(json_response, json_dumps_params={"ensure_ascii": False})


class UserRegister(View):
    """
    用户注册
    """
    def get(self, request):
        """
        访问用户注册界面
        :param request:
        :return:
        """
        return render(request, "register.html")

    def post(self, request):
        """
        提交注册信息(账户名，密码)
        :param request:
        :return:
        """
        # 从request.POST字典中取数据, 参数分别为 username、password
        # 未实现
        json_response = {
            "success": False,
            "msg": "",
            "redirect": ""
        }
        username = request.POST.get("username")
        password = request.POST.get("password")
        if username is None or password is None:
            json_response["msg"] = "用户名或密码为空！"
            return JsonResponse(json_response, json_dumps_params={"ensure_ascii": False})
        user = UserProfile.objects.filter(username=username)
        if len(user) > 0:
            json_response["msg"] = "用户已注册"
            return JsonResponse(json_response, json_dumps_params={"ensure_ascii": False})
        new_user = UserProfile()
        new_user.username = username
        new_user.password = password
        init_d, init_p = tool.initial_d_p_vector(5)
        new_user.D_vector = json.dumps(init_d)
        new_user.P_vector = json.dumps(init_p)
        new_user.save()
        json_response["success"] = True
        # json_response["redirect"] = "/user/login/"
        return JsonResponse(json_response, json_dumps_params={"ensure_ascii": False})


class UserPreference(View):
    def get(self, request):
        user_id = request.path.split("preference_customize")[1].replace("/", "")
        if len(user_id) < 1:
            return render(request, "login.html")
        user_id = int(user_id)
        user = UserProfile.objects.filter(id=user_id)
        if len(user) < 1:
            return render(request, "login.html")
        user = user[0]
        classification = [{
            "category_name": "recommender systems and personalization",
            "category_code": 0,
        }, {
            "category_name": "summarization and combination",
            "category_code": 1,
        }, {
            "category_name": "enterprise search and document structure",
            "category_code": 2,
        }, {
            "category_name": "sentiment analysis and combination",
            "category_code": 3,
        }, {
            "category_name": "question answering and document structure",
            "category_code": 4,
        }]
        return render(request, "preference_customize.html", {
            "user": user,
            "classification": classification
        })

    def post(self, request):
        user_preference = request.POST.get("user_preference")
        user_preference = json.loads(user_preference)
        user_id = request.POST.get("user_id")
        if len(user_id) < 1:
            return render(request, "login.html")
        user_id = int(user_id)
        user = UserProfile.objects.filter(id=user_id)
        if len(user) < 1:
            return render(request, "login.html")
        user = user[0]
        print(user_preference)
        if user_preference is not None and sum(user_preference) > 0:
            user.D_vector = json.dumps(user_preference)
            user.P_vector = json.dumps(tool.update_p_value(user.get_P_vector(), user_preference, 0.5))
            user.save()
        return JsonResponse({"success": True, "user_id": user_id}, json_dumps_params={"ensure_ascii": False})


class PreferenceAssess(View):
    def get(self, request):
        session_id = request.path.split("assess")[1].replace("/", "")
        if session_id is None or len(session_id) < 1:
            return render(request, "login.html")
        session = Session.objects.filter(id=session_id)
        if len(session) < 1:
            return render(request, "login.html")
        session = session[0]
        session_documents = Document.objects.filter(session__documents__session__in=[session])
        user = session.user
        return render(request, "preference_assess.html", {
            "session": session,
            "documents": session_documents,
            "user": user
        })

    def post(self, request):
        json_response = {
            "success": False,
            "msg": "",
            "user_id": None,
            "redirect": None
        }
        session_id = request.POST.get("session_id")
        session = Session.objects.filter(id=session_id)
        user_preference = request.POST.get("user_preference")
        user_preference = json.loads(user_preference)
        """
        计算Precision并存储
        需beornut实现
        user_preference结构
        {'56': False, '53': False, '41': False, '52': False, '44': False, '43': False, '54': False, '55': False, '47': False, '57': False, '48': False, '51': False, '46': False, '49': False, '58': False, '42': False, '60': True, '50': False, '45': False, '59': True}
        """
        json_response["success"] = True
        return JsonResponse(json_response, json_dumps_params={"ensure_ascii": False})

