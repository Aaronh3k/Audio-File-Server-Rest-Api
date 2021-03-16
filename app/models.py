from django.db import models

class AudioFile(models.Model):
    FILE_TYPE =(('SONG_FILE',1),('PODCAST_FILE',2),('AUDIOBOOK_FILE',3))
    name = models.CharField(max_length=100)
    duration = models.PositiveIntegerField()
    uploaded_at = models.DateTimeField(auto_now_add=True)
    file_type = models.IntegerField(choices=FILE_TYPE)
    host_author = models.CharField(max_length=100,null=True,blank=True)
    narrator = models.CharField(max_length=100,null=True,blank=True)
    
    @property
    def participants(self):
        return self.participant_set.all()
    
    class Meta:

        db_table = 'audiofile_tb'

class Participant(models.Model):
    audiofile    = models.ForeignKey(AudioFile,on_delete=models.CASCADE)
    participants = models.CharField(max_length=100)

    class Meta:

        db_table = 'participant_tb'
