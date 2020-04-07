from django.shortcuts import render
from django.views.generic.base import View
from django.http import JsonResponse

from RetrievalCore.models import Document, Session, UserProfile


# Create your views here.


class DocumentListView(View):
    def get(self, request):
        documents = Document.objects.all().filter(classification=-1)[:20]
        return render(request, "list.html", {
            "documents": documents
        })


class DocumentDetailView(View):
    def get(self, request, document_id):
        document = Document.objects.filter(id=document_id)[0]
        return render(request, "doc_detail.html", {
            "document": document
        })


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
            "msg": ""
        }
        username = request.POST.get("username")
        password = request.POST.get("password")
        if username is None or password is None:
            json_response["msg"] = "用户名或密码为空！"
            return JsonResponse(json_response)
        user = UserProfile.objects.filter(username=username)
        if len(user) < 1:
            json_response["msg"] = "未找到该用户"
            return JsonResponse(json_response)
        elif user.password == password:
            # 登录成功，未实现
            pass
        json_response["msg"] = "密码错误"
        return JsonResponse(json_response)


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
        pass

    def post(self, request):
        """
        提交注册信息(账户名，密码)
        :param request:
        :return:
        """
        # 从request.POST字典中取数据, 参数分别为 username、password
        # 未实现
        pass
