# encoding: utf-8
'''
Created on 2015年8月14日

@author: root
'''

from django.core.management.base import BaseCommand
import torch

from base_sd.models import ShootingScript
from my_talker.settings import ROOT_DIR


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('--test', action='store_true', default=False)
        parser.add_argument('--name', nargs = "?", default='', type=str)




        # if torch.cuda.is_available() and not args.cpu:
        #     args.device = "cuda"
        # else:
        #     args.device = "cpu"


    def handle(self, *args, **options):
        if options.get('test'):
            # print('testing..')
            ss = ShootingScript.objects.filter(finished=0).first()
            if ss is None:
                return
            
            print(ss)
            
            
            
            return
