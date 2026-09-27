from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import FileResponse
import os
from files.models import ProjectFile
from projects.models import Project
from notifications.utils import notify_file_uploaded
@login_required
def file_list(request):
    if request.user.role == 'super_admin':
        files = ProjectFile.objects.all().order_by('-uploaded_at')
    elif request.user.role == 'project_manager':
        projects = Project.objects.filter(created_by=request.user)
        files = ProjectFile.objects.filter(project__in=projects).order_by('-uploaded_at')
    else:
        projects = request.user.assigned_projects.all()
        files = ProjectFile.objects.filter(project__in=projects).order_by('-uploaded_at')

    return render(request, 'files/file_list.html', {'files': files})


@login_required
def file_upload(request):
    if request.method == 'POST':
        title = request.POST['title']
        project_id = request.POST['project']
        file_type = request.POST['file_type']
        uploaded_file = request.FILES.get('file')

        if not uploaded_file:
            messages.error(request, 'Please select a file!')
            return redirect('file_upload')

        project_file = ProjectFile.objects.create(
        title=title,
        file=uploaded_file,
        file_type=file_type,
        project_id=project_id,
        uploaded_by=request.user
            )
        notify_file_uploaded(project_file)
        messages.success(request, 'File uploaded successfully!')
        return redirect('file_list')

    if request.user.role == 'super_admin':
        projects = Project.objects.all()
    elif request.user.role == 'project_manager':
        projects = Project.objects.filter(created_by=request.user)
    else:
        projects = request.user.assigned_projects.all()

    return render(request, 'files/file_upload.html', {'projects': projects})


@login_required
def file_download(request, pk):
    file_obj = get_object_or_404(ProjectFile, pk=pk)
    response = FileResponse(file_obj.file.open('rb'))
    response['Content-Disposition'] = f'attachment; filename="{os.path.basename(file_obj.file.name)}"'
    return response


@login_required
def file_delete(request, pk):
    file_obj = get_object_or_404(ProjectFile, pk=pk)

    if request.user != file_obj.uploaded_by and request.user.role != 'super_admin':
        messages.error(request, 'You do not have permission!')
        return redirect('file_list')

    if request.method == 'POST':
        file_obj.file.delete()
        file_obj.delete()
        messages.success(request, 'File deleted!')
        return redirect('file_list')

    return render(request, 'files/file_confirm_delete.html', {'file': file_obj})