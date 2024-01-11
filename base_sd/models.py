import os

from django.db import models
from django.utils.functional import cached_property

from caidao_tools.django.abstract import AbstractModel
from tool_ffmpeg import to_seconds, merge_mp4_wav


REMOTE_BASE_DIR = ''

BASE_DIR = r''

class Actor(AbstractModel):
    name = models.CharField(max_length=20)
    description = models.TextField(verbose_name='人物描述')
    mugshot = models.FileField(upload_to=r'V:\static\media\uploaded', null=True, blank=True)

    class Meta:
        verbose_name_plural = "演员"
        
    @property
    def url_mugshot(self):
        return f'/static/{self.mugshot.name}'
# upload_to=r'V:\static\media\uploaded'
class Audio(AbstractModel):
    sound_name = models.CharField(max_length=255, null=True, blank=True, verbose_name='声音名称')
    audio = models.FileField(upload_to=r'V:\static\media\uploaded', null=True, blank=True, verbose_name='原声')
    url = models.URLField(null=True,blank=True, verbose_name='来源网址')
    subtitles = models.TextField(null=True, blank=True)
    
    voice = models.FileField(upload_to=r'V:\static\media\uploaded', null=True, blank=True, verbose_name='人声')
    srt = models.FileField(upload_to=r'V:\static\media\uploaded', null=True, blank=True, verbose_name='字幕')

    class Meta:
        verbose_name_plural = "音频"
    
    def __str__(self):
        return self.sound_name
    
    @property
    def url_sound(self):
        return f'/static/{self.audio.name}'
    
    @property
    def fpath(self):
        if self.voice.name:
            return self.voice.path
        elif self.audio.name:
            return self.audio.path
    
    
class ShootingScript(AbstractModel):
    name = models.CharField(max_length=20, null=True, blank=True, verbose_name='剧本名')
    audio = models.ForeignKey(Audio, verbose_name='人声', related_name='audio_voice', null=True, blank=True, on_delete=models.DO_NOTHING)
    music = models.ForeignKey(Audio, verbose_name='音乐', related_name='audio_music', null=True, blank=True, on_delete=models.DO_NOTHING)
    remark = models.TextField(null=True, blank=True, verbose_name='备注')
    finished = models.BooleanField(default=False)
    
    timestr_start = models.CharField(max_length=20, null=True, blank=True, verbose_name='起始：hh:mm:ss,xxx')
    timestr_end = models.CharField(max_length=20, null=True, blank=True, verbose_name='结束：hh:mm:ss,xxx')
    
    class Meta:
        verbose_name_plural = "拍摄脚本"

    def __str__(self):
        return self.name
    
    @property
    def fpath_auido_trimed(self):
        return os.path.join(os.path.dirname(self.audio.fpath),
                            f'trimed_{os.path.basename(self.audio.fpath)}',                            
                            )
    
    def has_audio_trimed(self):
        audio = self.audio.audio
        if not audio or not audio.name:
            return False
        if not os.path.lexists(audio.path):
            return False
        return os.path.lexists(self.fpath_auido_trimed)
    
    @property
    def start_time(self):
        return self.shootingscene_set.order_by('num').first().start
        
    @property
    def end_time(self):
        return self.shootingscene_set.order_by('num').last().end



class ShootingScene(AbstractModel):
    script = models.ForeignKey(ShootingScript, verbose_name='拍摄脚本', null=True, blank=True, on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=20, null=True, blank=True)
    num = models.PositiveSmallIntegerField(verbose_name='编号')
    description = models.TextField(verbose_name='场景描述',null=True, blank=True)
    
    subtitle = models.CharField(max_length=255, null=True, blank=True, verbose_name='字幕')
    
    audio = models.FileField(upload_to=BASE_DIR, null=True, blank=True, verbose_name='音频')
    
    scene = models.FileField(upload_to=BASE_DIR, null=True, blank=True)
    
    actor1 = models.ForeignKey(Actor, verbose_name='演员左1', related_name='actor1', null=True, blank=True, on_delete=models.DO_NOTHING)
    actor2 = models.ForeignKey(Actor, verbose_name='演员左2', related_name='actor2', null=True, blank=True, on_delete=models.DO_NOTHING)
    actor3 = models.ForeignKey(Actor, verbose_name='演员左3', related_name='actor3', null=True, blank=True, on_delete=models.DO_NOTHING)
    start = models.CharField(max_length=12, null=True, blank=True, verbose_name='起始时间')
    end = models.CharField(max_length=12, null=True, blank=True, verbose_name='结束时间')
    
    start_clip_id = models.PositiveBigIntegerField(null=True, blank=True, verbose_name='开始片段id')
    
    finished = models.BooleanField(default=False)
    
    no_face = models.BooleanField(default=False)
    
    flag_need_retrim_audio = models.BooleanField(default=False, verbose_name='需重切分音频')
    flag_need_retrim_video = models.BooleanField(default=False, verbose_name='需重切分视频')
    flag_need_retalk_video = models.BooleanField(default=False, verbose_name='需合成说话视频')
    
    result = models.FileField(upload_to=BASE_DIR, null=True, blank=True, verbose_name='结果视频')
    
    class Meta:
        verbose_name_plural = "场景"

    @cached_property
    def fpath_audio_4080(self):
        return 
        # return f'{REMOTE_BASE_DIR}/{self.script.id}_{self.num}_{self.id}_{os.path.basename(self.script.fpath_auido_trimed)}'
    
    @cached_property
    def fpath_img(self):
        return self.scene.path#.replace('\\', '/')
        # return f'{REMOTE_BASE_DIR}/{os.path.basename(self.scene.name)}'
    
    @property
    def fpath_input(self):
        return self.fpath_img 
    
    @cached_property
    def fpath_video(self):
        return f'''{REMOTE_BASE_DIR}/output_{os.path.basename(self.scene.name).rsplit('.',1)[-2]}.mp4'''
    
    def has_video(self):
        return os.path.lexists(self.fpath_video)
                                    
        
    def is_following(self):
        return not self.scene.name

    @property
    def next(self):
        return ShootingScene.objects.filter(script=self.script, num__gt=self.num).order_by('num').first()

    @property
    def last_following(self):
        assert not self.is_following()
        one = self
        while 1:
            n = one.next
            if n is None or not n.is_following():
                return one
            one = n
    
    @property
    def duration_seconds(self):
        return to_seconds(self.last_following.end) - to_seconds(self.start)
    
    def merge_video_directly(self):
        merge_mp4_wav(self.fpath_input, 
                      self.fpath_audio_4080, 
                      self.fpath_video,
                      self.duration_seconds,
                      )
    
  
        
