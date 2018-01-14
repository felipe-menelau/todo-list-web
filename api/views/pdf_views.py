from api.models import TODOList
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.template.loader import render_to_string
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from weasyprint import HTML
from datetime import datetime

class PdfExport(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk, format='json'):
        try:
            todolist = TODOList.objects.get(owner=request.user.id, id=pk)
        except(TypeError, ValueError, OverflowError, TODOList.DoesNotExist):
            return Response('', status.HTTP_403_FORBIDDEN)

        paragraphs = []

        for task in todolist.task_set.all().order_by('deadline'):
            paragraphs.append(f'{task.title}, done: {task.done}, deadline: {task.deadline}')

        html_string = render_to_string('todo_list_report.html', {'paragraphs': paragraphs})

        html = HTML(string=html_string)
        html.write_pdf(target=f'/tmp/{todolist.title}.pdf')

        fs = FileSystemStorage('/tmp')
        with fs.open(f'{todolist.title}.pdf') as pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="{todolist.title}-{str(datetime.now())}.pdf"'
            return response

        return response
