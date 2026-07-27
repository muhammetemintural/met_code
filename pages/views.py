from django.shortcuts import render

def index(request):
    return render(request, 'index.html')

def project_detail(request, project_id):
    return render(request, 'project_detail.html', {'project_id': project_id})