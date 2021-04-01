# -*- coding:utf-8 -*-
from django.shortcuts import render
from django.http import JsonResponse
from django.forms import model_to_dict

from web.forms.file import FolderModelForm
from web import models
from utils.tencent.cos import delete_file
from utils.tencent.cos import delete_file_list


# http://127.0.0.1:8000/manage/1/file/
# http://127.0.0.1:8000/manage/1/file/?folder=1
def file(request, project_id):
    """文件列表 && 添加文件夹"""

    parent_object = None
    folder_id = request.GET.get('folder', "")
    if folder_id.isdecimal():
        parent_object = models.FileRepository.objects.filter(id=int(folder_id), file_type=2,
                                                             project=request.tracer.project).first()

    # 如果是get请求，则为请求页面内容
    if request.method == "GET":

        breadcrumb_list = []
        parent = parent_object
        while parent:
            # breadcrumb_list.insert(0, {'id': parent.id, 'name': parent.name})
            breadcrumb_list.insert(0, model_to_dict(parent, ['id', 'name']))
            parent = parent.parent

        # 获取当前目录下所有的文件和文件夹
        queryset = models.FileRepository.objects.filter(project=request.tracer.project)
        if parent_object:
            # 进入了某个目录
            file_object_list = queryset.filter(parent=parent_object).order_by('-file_type')
        else:
            # 根目录
            file_object_list = queryset.filter(parent__isnull=True).order_by('-file_type')

        form = FolderModelForm(request, parent_object)
        context = {
            'form': form,
            'file_object_list': file_object_list,
            'breadcrumb_list': breadcrumb_list,
        }
        return render(request, 'file.html', context)

    # 如果是POST请求，则为添加文件夹 && 文件夹的修改
    fid = request.POST.get('fid', '')
    edit_object = None
    if fid.isdecimal():
        # 修改文件夹
        edit_object = models.FileRepository.objects.filter(id=int(fid), file_type=2,
                                                           project=request.tracer.project).first()
    if edit_object:
        form = FolderModelForm(request, parent_object, request.POST, instance=edit_object)
    else:
        # 添加文件夹
        form = FolderModelForm(request, parent_object, request.POST)

    if form.is_valid():
        # 在数据库添加数据
        form.instance.project = request.tracer.project
        form.instance.file_type = 2
        form.instance.update_user = request.tracer.user
        form.instance.parent = parent_object
        form.save()
        return JsonResponse({'status': True})

    return JsonResponse({'status': False, 'error': form.errors})


# http://127.0.0.1:8000/manage/1/file/delete/?fid=1
def file_delete(request, project_id):
    """删除文件"""
    fid = request.GET.get('fid')
    # 删除文件或者文件夹，仅仅在数据库中删除了
    delete_object = models.FileRepository.objects.filter(id=fid, project=request.tracer.project).first()
    if delete_object.file_type == 1:
        # 删除文件(数据库中删除, COS中文件删除， 项目已使用空间容量还回去)
        # 删除文件，将容量还给当前项目的已使用空间
        request.tracer.project.user_space -= delete_object.file_size
        request.tracer.project.save()
        # COS中删除文件
        delete_file(request.tracer.project.bucket, request.traver.project.region, delete_object.key)
        # 在数据库中删除当前文件
        delete_object.delete()
        return JsonResponse({'status': True})

    # 删除文件夹（找到文件夹下所有的文件->数据库中删除, COS中文件删除， 项目已使用空间容量还回去)
    # delete_object
    # 找他下面的所有文件和文件夹
    total_size = 0
    key_list = []
    folder_list = [delete_object, ]
    for folder in folder_list:
        child_list = models.FileRepository.objects.filter(project=request.tracer.project, parent=folder).order_by(
            '-file_type')
        for child in child_list:
            if child.file_type == 2:
                folder_list.append(child)
            else:
                # 文件大小汇总
                total_size += child.file_size
                # 先删除文件
                key_list.append({"Key": child.key})

    # COS批量删除文件
    if key_list:
        delete_file_list(request.tracer.project.bucket, request.tracer.project.region, key_list)
    # 归还容量
    if total_size:
        request.tracer.project.user_space -= total_size
        request.tracer.project.save()

    # 删除数据库中的文件, Django ORM 的 delete()函数
    delete_object.delete()
    return JsonResponse({'status': True})
