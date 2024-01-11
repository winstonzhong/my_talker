# encoding: utf-8
'''
Created on 2015年8月14日

@author: root
'''

import os
import subprocess

from django.core.management.base import BaseCommand
import torch

from base_sd.models import ShootingScript, ShootingScene
from my_talker.settings import ROOT_DIR


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('--test', action='store_true', default=False)
        parser.add_argument('--step', action='store_true', default=False)
        parser.add_argument('--name', nargs = "?", default='', type=str)
        parser.add_argument('--run', action='store_true', default=False)




        # if torch.cuda.is_available() and not args.cpu:
        #     args.device = "cuda"
        # else:
        #     args.device = "cpu"
    
    def get_shootingscene(self):
        # ss = ShootingScript.objects.filter(finished=0).first()
        # return ss.shootingscene_set.filter(finished=0).exclude(scene='').first() if ss is not None else None
        return ShootingScene.objects.filter(flag_need_retalk_video=1).first()
    
    def step(self):
        s = self.get_shootingscene()
        if s is not None:
            print(s)
            p = subprocess.Popen(
                f'''python3 /home/oem/workspace/video-retalking/inference_shell.py   --face {s.fpath_input}   --audio {s.fpath_audio_4080}   --outfile {s.fpath_video}''', 
                shell=True)
            p.wait()
            s.finished = s.has_video()
            s.save()
            print(s.finished)
            print('done!')
            return s
        

    def handle(self, *args, **options):
        if options.get('test'):
            s = self.get_shootingscene()
            print(s)
            print('path:', s.audio.path)

        if options.get('step'):
            self.step()
            return
        
        if options.get('run'):
            while self.step() is not None:
                pass
    
