from django.shortcuts import render
from django.views.generic.base import View
from RetrievalCore.models import Document, Session

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
