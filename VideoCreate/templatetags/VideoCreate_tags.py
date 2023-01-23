import json, os

from django import template

from VideoCreate.models import Workspace
from VideoCreate.base_config import SCRIPT_DIR, WORKSPACE_DIR

register = template.Library()


@register.simple_tag()
def get_workspace(filter=None):
    if not filter:
        return 'Выбрать проект'
    else:
        return Workspace.title.filter(title=filter)


@register.inclusion_tag('VideoCreate/list_workspaces.html')
def show_workspaces():
    workspaces = Workspace.objects.all()
    return {'workspaces': workspaces}


@register.inclusion_tag('VideoCreate/progress_bar.html')
def show_progress_bar():
    try:
        with open(f'{SCRIPT_DIR}/progr_bar.json', 'r') as file:
            context = json.load(file)
        return context
    except:
        return

@register.inclusion_tag('VideoCreate/info_bar.html')
def show_info_bar(path_url):
    context = {}
    try:
        with open(f'/{WORKSPACE_DIR}/{path_url}/model/{path_url}_SAEHD_summary.txt', 'r') as file:
            for line in file:
                if 'Current iteration' in line:
                    context['iteration'] = line.strip().strip('==').split(':')[1].strip()
    except FileNotFoundError:
        pass
    try:
        files_video = os.listdir(f'{WORKSPACE_DIR}/{path_url}')
        for filename in files_video:
            if 'data_src.' in filename:
                context['data_src_file'] = 'ДА'
            elif 'data_dst.' in filename:
                context['data_dst_file'] = 'ДА'
    except FileNotFoundError:
        context['data_src_file'] = 'НЕТ'
        context['data_dst_file'] = 'НЕТ'

    if os.path.exists(f'{WORKSPACE_DIR}/{path_url}/data_src'):
        files_src_frames = os.listdir(f'{WORKSPACE_DIR}/{path_url}/data_src')
        context['src_frames'] = len(files_src_frames)
    else:
        context['src_frames'] = 0

    if os.path.exists(f'{WORKSPACE_DIR}/{path_url}/data_dst'):
        files_dst_frames = os.listdir(f'{WORKSPACE_DIR}/{path_url}/data_dst')
        context['dst_frames'] = len(files_dst_frames)
    else:
        context['dst_frames'] = 0

    if os.path.exists(f'{WORKSPACE_DIR}/{path_url}/data_src/aligned'):
        files_src_faces = os.listdir(f'{WORKSPACE_DIR}/{path_url}/data_src/aligned')
        context['src_faces'] = len(files_src_faces)
    else:
        context['src_faces'] = 0

    if os.path.exists(f'{WORKSPACE_DIR}/{path_url}/data_dst/aligned'):
        files_dst_faces = os.listdir(f'{WORKSPACE_DIR}/{path_url}/data_dst/aligned')
        context['dst_faces'] = len(files_dst_faces)
    else:
        context['dst_faces'] = 0
    return context


@register.inclusion_tag('VideoCreate/nav_bar.html')
def show_nav_bar(path_url):
    context = {'path_url': path_url}
    return context
