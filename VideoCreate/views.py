import os, subprocess, threading, json, random, shutil

from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from rest_framework.views import APIView
from rest_framework.response import Response

from .forms import *
from .base_config import WORKSPACE_DIR, START_DIR, SCRIPT_DIR


def index(request, path_url=None):
    context = {'path_url': path_url}

    if request.method == 'POST':
        if request.POST.get('stop_train') == 'True':
            stop_command = {'stop_train': True}
            try:
                with open(f'{WORKSPACE_DIR}/{path_url}/model/stop_command.json', 'w') as file:
                    file.write(json.dumps(stop_command))
            except:
                pass

        file_src = request.FILES.get('file_src')
        file_dst = request.FILES.get('file_dst')
        if file_src:
            with open(f'{WORKSPACE_DIR}/{path_url}/data_src.{file_src.name.split(".")[-1]}', 'wb+') as dest:
                for chunk in file_src.chunks():
                    dest.write(chunk)
        if file_dst:
            with open(f'{WORKSPACE_DIR}/{path_url}/data_dst.{file_dst.name.split(".")[-1]}', 'wb+') as dest:
                for chunk in file_dst.chunks():
                    dest.write(chunk)

        if request.POST.get('remove_project') == 'on':
            print(Workspace.objects.filter(path_url=path_url))
            Workspace.objects.filter(path_url=path_url).delete()
            shutil.rmtree(os.path.join(WORKSPACE_DIR, path_url))
            return redirect('index')

    if path_url:
        try:
            for file_name in os.listdir(f'{START_DIR}/DjangoFake/VideoCreate/static/VideoCreate/{path_url}/'):
                if 'result.' in file_name:
                    context['result_download'] = f'/VideoCreate/{path_url}/{file_name}'
        except:
            pass

    if path_url:
        return render(request, "VideoCreate/index.html", context=context)
    else:
        return render(request, "VideoCreate/start.html", context=context)



def video_extract(request, path_url=None):
    context = {'path_url': path_url}

    if request.method == 'POST':
        data_run = {}
        video_extract_sort = threading.Thread(target=run_create)

        with open(f'{SCRIPT_DIR}/data_run.json', 'w') as file:
            file.write(json.dumps(data_run))
        ################    DST    ###################
        if request.POST.get('videoed_extract_video_dst') == 'on':
            data_run['videoed_extract_video_dst'] = {
                'output_ext': request.POST.get('videoed_extract_video_dst-output_ext'),
                'input_file': f'{WORKSPACE_DIR}/{path_url}/data_dst.*',
                'output_dir': f'{WORKSPACE_DIR}/{path_url}/data_dst'
            }

        if request.POST.get('face_extract_dst') == 'on':
            data_run['face_extract_dst'] = {
                'detector': request.POST.get('face_extract_dst-detector'),
                'input_path': f'{WORKSPACE_DIR}/{path_url}/data_dst',
                'output_path': f'{WORKSPACE_DIR}/{path_url}/data_dst/aligned',
                'face_type': request.POST.get('face_extract_dst-face_type'),
                'image_size': int(request.POST.get('face_extract_dst-image_size'))
            }

        if request.POST.get('sort_images_dst') == 'on':
            data_run['sort_images_dst'] = {
                'sort_by_method': request.POST.get('sort_images_dst-sort_by_method'),
                'input_dir': f'{WORKSPACE_DIR}/{path_url}/data_dst/aligned'
            }

        if request.POST.get('rename_dst') == 'on':
            data_run['rename_dst'] = {
                'input_dir': f'{WORKSPACE_DIR}/{path_url}/data_dst/aligned',
                'recover_original_aligned_filename': True
            }

        ################    SRC    ###################
        if request.POST.get('videoed_extract_video_src') == 'on':
            data_run['videoed_extract_video_src'] = {}
            data_run['videoed_extract_video_src']['output_ext'] = request.POST.get('videoed_extract_video_src-output_ext')
            data_run['videoed_extract_video_src']['input_file'] = f'{WORKSPACE_DIR}/{path_url}/data_src.*'
            data_run['videoed_extract_video_src']['output_dir'] = f'{WORKSPACE_DIR}/{path_url}/data_src'

        if request.POST.get('face_extract_src') == 'on':
            data_run['face_extract_src'] = {}
            data_run['face_extract_src']['detector'] = request.POST.get('face_extract_dst-detector')
            data_run['face_extract_src']['input_path'] = f'{WORKSPACE_DIR}/{path_url}/data_src'
            data_run['face_extract_src']['output_path'] = f'{WORKSPACE_DIR}/{path_url}/data_src/aligned'
            data_run['face_extract_src']['face_type'] = request.POST.get('face_extract_src-face_type')
            data_run['face_extract_src']['image_size'] = int(request.POST.get('face_extract_src-image_size'))

        if request.POST.get('sort_images_src') == 'on':
            data_run['sort_images_src'] = {
                'sort_by_method': request.POST.get('sort_images_src-sort_by_method'),
                'input_dir': f'{WORKSPACE_DIR}/{path_url}/data_src/aligned'
            }

        if request.POST.get('rename_src') == 'on':
            data_run['rename_src'] = {
                'input_dir': f'{WORKSPACE_DIR}/{path_url}/data_src/aligned',
                'recover_original_aligned_filename': True
            }

        with open(f'{SCRIPT_DIR}/data_run.json', 'w') as file:
            file.write(json.dumps(data_run))

        if not video_extract_sort.is_alive():
            video_extract_sort.start()

    return render(request, "VideoCreate/video_extract.html", context=context)


def model_train(request, path_url=None):
    context = {'path_url': path_url}

    try:
        shutil.copy2(f'{WORKSPACE_DIR}/{path_url}/model/preview_SAEHD.jpg',
                     f'{START_DIR}/DjangoFake/VideoCreate/static/VideoCreate/images/{path_url}_preview_SAEHD.jpg')
        context['preview'] = f'VideoCreate/images/{path_url}_preview_SAEHD.jpg'
    except:
        pass

    if request.method == 'POST':
        data_run = {}
        video_extract_sort = threading.Thread(target=run_create)

        with open(f'{SCRIPT_DIR}/data_run.json', 'w') as file:
            file.write(json.dumps(data_run))
        stop_command = {'stop_train': False}
        try:
            with open(f'{WORKSPACE_DIR}/{path_url}/model/stop_command.json', 'w') as file:
                file.write(json.dumps(stop_command))
        except:
            pass
        ################    DST    ###################
        if request.POST.get('xsegapply_dst') == 'on':
            data_run['xsegapply_dst'] = {
                'input_dir': f'{WORKSPACE_DIR}/{path_url}/data_dst/aligned',
                'model_dir': f'{SCRIPT_DIR}/model_generic_xseg'
            }

        ################    SRC    ###################
        if request.POST.get('xsegapply_src') == 'on':
            data_run['xsegapply_src'] = {
                'input_dir': f'{WORKSPACE_DIR}/{path_url}/data_src/aligned',
                'model_dir': f'{SCRIPT_DIR}/model_generic_xseg'
            }

        ################    XSEG TRAIN    ###################
        if request.POST.get('xseg_train') == 'on':
            data_run['xseg_train'] = {
                'model_name': 'XSeg',
                'training_data_src_dir': f'{WORKSPACE_DIR}/{path_url}/data_src/aligned',
                'training_data_dst_dir': f'{WORKSPACE_DIR}/{path_url}/data_dst/aligned',
                'model_dir': f'{WORKSPACE_DIR}/{path_url}/model',
                'face_type': 'wf',
                'batch_size': 4,
                'target_iter': int(request.POST.get('xseg_train-iter')),
                'no_preview': True,
                'pretrain': False
            }

        if request.POST.get('xseg_train_dst') == 'on':
            data_run['xseg_train_dst'] = {
                'input_dir': f'{WORKSPACE_DIR}/{path_url}/data_dst/aligned',
                'model_dir': f'{WORKSPACE_DIR}/{path_url}/model',
            }

        if request.POST.get('xseg_train_src') == 'on':
            data_run['xseg_train_src'] = {
                'input_dir': f'{WORKSPACE_DIR}/{path_url}/data_src/aligned',
                'model_dir': f'{WORKSPACE_DIR}/{path_url}/model',
            }

        ################    TOTAL TRAIN    ###################
        if request.POST.get('train_run') == 'on':
            data_run['train_run'] = {
                'change_set': True if request.POST.get('train_run-change_set') == 'on' else False,
                'model_name': request.POST.get('train_run-model_name'),
                'model_dir': f'{WORKSPACE_DIR}/{path_url}/model',
                'training_data_src_dir': f'{WORKSPACE_DIR}/{path_url}/data_src/aligned',
                'training_data_dst_dir': f'{WORKSPACE_DIR}/{path_url}/data_dst/aligned',
                'pretraining_data_dir': f'{SCRIPT_DIR}/pretrain_CelebA',
                'pretrained_model_dir': f'{SCRIPT_DIR}/pretrain_Quick96' if request.POST.get('train_run-model_name') == 'Quick96' else None,
                'no_preview': True,
                'force_model_name': path_url,
                'force_gpu_idxs': None,
                'cpu_only': False,
                'silent_start': False,
                'execute_programs': None,
                'autobackup_hour': int(request.POST.get('train_run-autobackup_hour')),
                'write_preview_history': True,
                'target_iter': int(request.POST.get('train_run-target_iter')),
                'random_flip': True,
                'random_src_flip': True if request.POST.get('train_run-random_flip_src') == 'ДА' else False,
                'random_dst_flip': True if request.POST.get('train_run-random_flip_dst') == 'ДА' else False,
                'batch_size': 4,
                'resolution': 256,

                'ae_dims': 256,
                'e_dims': 64,
                'd_dims': 64,
                'd_mask_dims': 22,

                'face_type': request.POST.get('train_run-face_type'),
                'masked_training': True if request.POST.get('train_run-masked_training') == 'ДА' else False,
                'eyes_mouth_prio': True if request.POST.get('train_run-eyes_mouth_prio') == 'ДА' else False,
                'uniform_yaw': True if request.POST.get('train_run-uniform_yaw') == 'ДА' else False,
                'blur_out_mask': True if request.POST.get('train_run-blur_out_mask') == 'ДА' else False,

                'models_opt_on_gpu': True,
                'adabelief': True,
                'random_warp': True if request.POST.get('train_run-random_warp') == 'ДА' else False,
                'lr_dropout': True if request.POST.get('train_run-lr_dropout') == 'ДА' else False,
                'random_hsv_power': 0.0,
                'gan_power': float(request.POST.get('train_run-gan_power')),
                'face_style_power': 0.0,
                'bg_style_power': 0.0,
                'ct_mode': None,
                'clipgrad': False,
                'pretrain': False
            }

        with open(f'{SCRIPT_DIR}/data_run.json', 'w') as file:
            file.write(json.dumps(data_run))

        if not video_extract_sort.is_alive():
            video_extract_sort.start()

    return render(request, "VideoCreate/model_train.html", context=context)


def video_merge(request, path_url=None):
    context = {'path_url': path_url}
    if request.POST.get('merge_run') == 'on':
        merge_run = {}
        video_extract_sort = threading.Thread(target=run_create)

        merge_run['merge_run'] = {
            'model_name': request.POST.get('merge_run-model_name'),
            'model_dir': f'{WORKSPACE_DIR}/{path_url}/model',
            'force_model_name': path_url,
            'input_dir': f'{WORKSPACE_DIR}/{path_url}/data_dst',
            'output_dir': f'{WORKSPACE_DIR}/{path_url}/data_dst/merged',
            'output_mask_dir': f'{WORKSPACE_DIR}/{path_url}/data_dst/merged_mask',
            'aligned_dir': f'{WORKSPACE_DIR}/{path_url}/data_dst/aligned',
            'force_gpu_idxs': None,
            'cpu_only': False,
            'mode': int(request.POST.get('merge_run-mode')),
            'mask_mode': int(request.POST.get('merge_run-mask_mode')),
            'erode_mask_modifier': int(request.POST.get('merge_run-erode_mask_modifier')),
            'blur_mask_modifier': int(request.POST.get('merge_run-blur_mask_modifier')),
            'motion_blur_power': int(request.POST.get('merge_run-motion_blur_power')),
            'output_face_scale': int(request.POST.get('merge_run-output_face_scale')),
            'color_transfer_mode': request.POST.get('merge_run-color_transfer_mode'),
            'sharpen_mode': int(request.POST.get('merge_run-sharpen_mode')),
            'super_resolution_power': int(request.POST.get('merge_run-super_resolution_power')),
            'image_denoise_power': int(request.POST.get('merge_run-image_denoise_power')),
            'bicubic_degrade_power': int(request.POST.get('merge_run-bicubic_degrade_power')),
            'color_degrade_power': int(request.POST.get('merge_run-color_degrade_power'))
        }

        with open(f'{SCRIPT_DIR}/data_run.json', 'w') as file:
            file.write(json.dumps(merge_run))
        if not video_extract_sort.is_alive():
            video_extract_sort.start()

    if request.POST.get('video-from-sequence') == 'on':
        video_run = {}
        video_extract_sort = threading.Thread(target=run_create)

        with open(f'{SCRIPT_DIR}/data_run.json', 'w') as file:
            file.write(json.dumps(video_run))

        video_run['video_run'] = {
            'input_dir': f'{WORKSPACE_DIR}/{path_url}/data_dst/merged',
            'output_file': f'{START_DIR}/DjangoFake/VideoCreate/static/VideoCreate/{path_url}/result.mp4',
            'reference_file': f'{WORKSPACE_DIR}/{path_url}/data_dst.*',
        }
        with open(f'{SCRIPT_DIR}/data_run.json', 'w') as file:
            file.write(json.dumps(video_run))
        if not video_extract_sort.is_alive():
            video_extract_sort.start()

    if os.path.exists(f'{WORKSPACE_DIR}/{path_url}/data_dst/merged/'):
        url_merged = f'{WORKSPACE_DIR}/{path_url}/data_dst/merged/'
    else:
        os.mkdir(f'{WORKSPACE_DIR}/{path_url}/data_dst/merged')
        url_merged = f'{WORKSPACE_DIR}/{path_url}/data_dst/merged/'

    files_merge = os.listdir(url_merged)

    url_merged_img = f'{START_DIR}/DjangoFake/VideoCreate/static/VideoCreate/{path_url}/'
    image_list = []


    try:
        os.mkdir(url_merged_img)
    except FileExistsError:
        if os.listdir(url_merged_img):
            for url_img in os.listdir(url_merged_img):
                if '.jpg' in url_img or '.png' in url_img:
                    os.remove(url_merged_img + url_img)

    if len(files_merge) != 0:
        for img in random.choices(files_merge, k=6):
            shutil.copy2(f'{url_merged}/{img}', url_merged_img)
            image_list.append(f'VideoCreate/{path_url}/{img}')

    context['files'] = image_list
    return render(request, "VideoCreate/video_merge.html", context=context)


def photo_src(request, path_url=None):
    context = {'path_url': path_url}
    return render(request, "VideoCreate/photo_src.html", context=context)


def create_workspace(request):
    if request.method == 'POST':
        form = CreateWorkspace(request.POST)
        if form.is_valid():
            form.save()
            os.mkdir(f'{WORKSPACE_DIR}/{form.cleaned_data.get("path_url")}')
            os.mkdir(f'{WORKSPACE_DIR}/{form.cleaned_data.get("path_url")}/model')
            threading.Thread(target=copy_pretrain_model, args=(form.cleaned_data.get("path_url"), )).start()
            return redirect('index')
    else:
        form = CreateWorkspace()
    data = {'form': form}
    return render(request, "VideoCreate/create_workspace.html", data)


def run_create():
    # answer = subprocess.check_call(['python', f'{SCRIPT_DIR}/deepfake_control.py'],)
    answer = subprocess.Popen(['python', f'{SCRIPT_DIR}/deepfake_control.py'], )
    print(answer)


def copy_pretrain_model(path_url):
    for file in os.listdir(os.path.join(WORKSPACE_DIR, 'pretrain.LIAE-UD.WF.224res.64-64-256-16 (1M iters)')):
        shutil.copy2(
            os.path.join(WORKSPACE_DIR, 'pretrain.LIAE-UD.WF.224res.64-64-256-16 (1M iters)', file),
            os.path.join(WORKSPACE_DIR, path_url, 'model', f"{path_url}_{file.split('_', 1)[1]}")
        )


############## API ##################
class StatisticApi(APIView):
    def get(self, requestst):
        with open(f'{SCRIPT_DIR}/progr_bar.json', 'r') as file:
            context = json.load(file)
        return Response(context)
