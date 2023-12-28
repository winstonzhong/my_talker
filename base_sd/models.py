import os

from django.db import models

from caidao_tools.django.abstract import AbstractModel


# Create your models here.
class Audio(AbstractModel):
    sound_name = models.CharField(max_length=255, null=True, blank=True, verbose_name='声音名称')
    audio = models.FileField(upload_to=r'V:\static\media\uploaded', null=True, blank=True, verbose_name='原声')
    url = models.URLField(null=True,blank=True, verbose_name='来源网址')
    subtitles = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "音频"
    
    def __str__(self):
        return self.sound_name
    
    @property
    def url_sound(self):
        return f'/static/{self.audio.name}'

class Actor(AbstractModel):
    name = models.CharField(max_length=20)
    description = models.TextField(verbose_name='人物描述')
    mugshot = models.FileField(upload_to=r'V:\static\media\uploaded', null=True, blank=True)

    class Meta:
        verbose_name_plural = "演员"
        
    @property
    def url_mugshot(self):
        return f'/static/{self.mugshot.name}'
    
class ShootingScript(AbstractModel):
    name = models.CharField(max_length=20, null=True, blank=True, verbose_name='剧本名')
    audio = models.ForeignKey(Audio, verbose_name='音频', related_name='audio_origin', null=True, blank=True, on_delete=models.DO_NOTHING)
    subtitles = models.TextField(null=True, blank=True)
    
    # audio_trimed = models.ForeignKey(Audio, verbose_name='切分的音频', related_name='audio_trimed', null=True, blank=True, on_delete=models.DO_NOTHING)
    
    class Meta:
        verbose_name_plural = "拍摄脚本"

    def __str__(self):
        return self.name
    
    @property
    def fpath_auido_trimed(self):
        return os.path.join(os.path.dirname(self.audio.audio.path),
                            f'trimed_{os.path.basename(self.audio.audio.path)}',                            
                            )
    
         
    

class ShootingScene(AbstractModel):
    script = models.ForeignKey(ShootingScript, verbose_name='拍摄脚本', null=True, blank=True, on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=20, null=True, blank=True)
    num = models.PositiveSmallIntegerField(verbose_name='编号')
    description = models.TextField(verbose_name='场景描述',null=True, blank=True)
    
    subtitle = models.CharField(max_length=255, null=True, blank=True, verbose_name='字幕')
    
    scene = models.FileField(upload_to=r'V:\static\media\uploaded', null=True, blank=True)
    
    actor1 = models.ForeignKey(Actor, verbose_name='演员左1', related_name='actor1', null=True, blank=True, on_delete=models.DO_NOTHING)
    actor2 = models.ForeignKey(Actor, verbose_name='演员左2', related_name='actor2', null=True, blank=True, on_delete=models.DO_NOTHING)
    actor3 = models.ForeignKey(Actor, verbose_name='演员左3', related_name='actor3', null=True, blank=True, on_delete=models.DO_NOTHING)
    # actor4 = models.ForeignKey(Actor, verbose_name='演员左4', related_name='actor4', null=True, blank=True, on_delete=models.DO_NOTHING)
    # actor5 = models.ForeignKey(Actor, verbose_name='演员左5', related_name='actor5', null=True, blank=True, on_delete=models.DO_NOTHING)
    start = models.CharField(max_length=12, null=True, blank=True, verbose_name='起始时间')
    end = models.CharField(max_length=12, null=True, blank=True, verbose_name='结束时间')
    
    video = models.FileField(upload_to=r'V:\static\media\uploaded', null=True, blank=True, verbose_name='生成的视频')
    
    class Meta:
        verbose_name_plural = "场景"