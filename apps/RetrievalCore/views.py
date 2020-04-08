from django.shortcuts import render
from django.views.generic.base import View
from django.http import JsonResponse

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
        documents = Document.objects.all().filter(classification=-1)[:20]
        return render(request, "list.html", {
            "documents": documents
        })


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
        document = Document.objects.filter(id=document_id)[0]
        return render(request, "doc_detail.html", {
            "document": document
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
