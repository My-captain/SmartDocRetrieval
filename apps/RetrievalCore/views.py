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
                "session": user_session
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
                "session": new_session
            })

    def post(self, request):
        """
        {
           "1":{
              "classification":3,
              "relevance":0.8
           },
           "4":{
              "classification":0,
              "relevance":0.3
           },
           "8":{
              "classification":0,
              "relevance":0.8
           },
           "16":{
              "classification":1,
              "relevance":0.4
           },
           "20":{
              "classification":0,
              "relevance":0.4
           }
        }
        :param request:
        :return:
        """
        user_relevance = json.loads(request.POST.get("session_relevance"))
        # 未实现，需beornut实现
        # 计算并更新D、P
        # user_relevance结构如以上注释, key为document id，classification为文献类别、relevance为用户分值
        # 计算并更新完成后
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
            user_session = user_sessions[0]
            d = user.get_D_vector()
            user_d = [0 for i in range(len(d))]
            num_d = [0 for i in range(len(d))]
            for k, v in user_relevance:
                user_d[v['classification']] += v['relevance']
                num_d[v['classification']] += 1
            for k, v in enumerate(user_d):
                if v > 0:
                    v /= num_d[k]
            new_d = tool.update_d_value(d, user_d, 300)
            new_p = tool.update_p_value(user.get_P_vector(), new_d, 0.5)
            user_session.D_vector = new_d
            user_session.P_vector = new_p
            user.D_vector = new_d
            user.P_vector = new_p
            user_session.save()
            user.save()
            # 返回准确率评估页面，其中documents和session应从request或session中获取
            # return render(request, "list.html", {
            #     "documents": documents,
            #     "session": session
            # })


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
            "user_id": None
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
            # 登录成功，未实现
            json_response["success"] = True
            json_response["user_id"] = user.id
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
        # 未实现
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
        new_user.save()
        json_response["success"] = True
        # json_response["redirect"] = "/user/login/"
        return JsonResponse(json_response, json_dumps_params={"ensure_ascii": False})
