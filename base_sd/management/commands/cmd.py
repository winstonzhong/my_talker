# encoding: utf-8
'''
Created on 2015年8月14日

@author: root
'''

from django.core.management.base import BaseCommand
import torch

from base_sd.models import ShootingScene, ShootingScript
from helper_talker import run_args
from my_talker.settings import ROOT_DIR


class DummyArg(object):
    def __init__(self, d):
        self.d = d
        
    def __getattr__(self, name):
        return self.d.get(name)
    

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('--test', action='store_true', default=False)
        parser.add_argument('--name', nargs = "?", default='', type=str)


        parser.add_argument("--driven_audio", default=f'{ROOT_DIR}/examples/driven_audio/bus_chinese.wav', help="path to driven audio")
        parser.add_argument("--source_image", default=f'{ROOT_DIR}/examples/source_image/full_body_1.png', help="path to source image")
        parser.add_argument("--ref_eyeblink", default=None, help="path to reference video providing eye blinking")
        parser.add_argument("--ref_pose", default=None, help="path to reference video providing pose")
        parser.add_argument("--checkpoint_dir", default=f'{ROOT_DIR}/checkpoints', help="path to output")
        parser.add_argument("--result_dir", default=f'{ROOT_DIR}/results', help="path to output")
        parser.add_argument("--pose_style", type=int, default=0,  help="input pose style from [0, 46)")
        parser.add_argument("--batch_size", type=int, default=2,  help="the batch size of facerender")
        parser.add_argument("--size", type=int, default=256,  help="the image size of the facerender")
        parser.add_argument("--expression_scale", type=float, default=1.,  help="the batch size of facerender")
        parser.add_argument('--input_yaw', nargs='+', type=int, default=None, help="the input yaw degree of the user ")
        parser.add_argument('--input_pitch', nargs='+', type=int, default=None, help="the input pitch degree of the user")
        parser.add_argument('--input_roll', nargs='+', type=int, default=None, help="the input roll degree of the user")
        parser.add_argument('--enhancer',  type=str, default=None, help="Face enhancer, [gfpgan, RestoreFormer]")
        parser.add_argument('--background_enhancer',  type=str, default=None, help="background enhancer, [realesrgan]")
        parser.add_argument("--cpu", dest="cpu", action="store_true") 
        parser.add_argument("--face3dvis", action="store_true", help="generate 3d face and 3d landmarks") 
        parser.add_argument("--still", action="store_true", help="can crop back to the original videos for the full body aniamtion") 
        parser.add_argument("--preprocess", default='crop', choices=['crop', 'extcrop', 'resize', 'full', 'extfull'], help="how to preprocess the images" ) 
        parser.add_argument("--verbose",action="store_true", help="saving the intermedia output or not" ) 
        parser.add_argument("--old_version",action="store_true", help="use the pth other than safetensor version" ) 
        
        
        # net structure and parameters
        parser.add_argument('--net_recon', type=str, default='resnet50', choices=['resnet18', 'resnet34', 'resnet50'], help='useless')
        parser.add_argument('--init_path', type=str, default=None, help='Useless')
        parser.add_argument('--use_last_fc',default=False, help='zero initialize the last fc')
        parser.add_argument('--bfm_folder', type=str, default=f'{ROOT_DIR}/checkpoints/BFM_Fitting/')
        parser.add_argument('--bfm_model', type=str, default='BFM_model_front.mat', help='bfm model')
        
        # default renderer parameters
        parser.add_argument('--focal', type=float, default=1015.)
        parser.add_argument('--center', type=float, default=112.)
        parser.add_argument('--camera_d', type=float, default=10.)
        parser.add_argument('--z_near', type=float, default=5.)
        parser.add_argument('--z_far', type=float, default=15.)
        
        parser.add_argument('--device', type=str, default='cuda' if torch.cuda.is_available() else 'cpu')
        
        
        parser.add_argument('--script_id', nargs='?', type=int, default=None, help="the input script id")

        # if torch.cuda.is_available() and not args.cpu:
        #     args.device = "cuda"
        # else:
        #     args.device = "cpu"


    def handle(self, *args, **options):
        # print(args)
        # print(options)
        # print(self)
        # print(dir(self))
        # print(dir(options))

        options['preprocess'] = 'full'
        options['still'] = True
        options['enhancer'] = 'gfpgan'
        options['result_dir'] = 'output'


        if options.get('test'):
            # print('testing..')
            ss = ShootingScript.objects.get(id=options.get('script_id'))
            for s in ss.shootingscene_set.filter():
                if s.is_following():
                    continue
                
                if s.has_video():
                    continue
                
                options['driven_audio'] = s.fpath_audio_4080
                options['source_image'] = s.fpath_img
                options['fpath_video'] = s.fpath_video
            
                args = DummyArg(options)
                run_args(args)
            return
