from rest_framework import serializers,status
from .models import AudioFile,Participant

class CreateSongTypeSerializer(serializers.Serializer):
    name_of_the_song = serializers.CharField(max_length=100)
    duration_in_number_of_seconds = serializers.IntegerField()

    def create(self,validated_data):
        song_type_obj = AudioFile.objects.create(name=validated_data['name_of_the_song'],duration=validated_data['duration_in_number_of_seconds'],
                                file_type=1)

        return song_type_obj

class CreatePodcastTypeSerializer(serializers.Serializer):
    name_of_the_podcast = serializers.CharField(max_length=100)
    duration_in_number_of_seconds = serializers.IntegerField()
    host = serializers.CharField(max_length=100)
    participants = serializers.ListField(child=serializers.CharField(max_length=100,required=False),max_length=10)

    def create(self,validated_data):
        podcast_type_obj = AudioFile.objects.create(name=validated_data['name_of_the_podcast'],duration=validated_data['duration_in_number_of_seconds'],
                                file_type=2,host_author=validated_data['host'])

        for participant in validated_data['participants']:
            Participant.objects.create(audiofile=podcast_type_obj,participants=participant)

        return podcast_type_obj

class CreateAudioBookTypeSerializer(serializers.Serializer):
    title_of_the_audiobook = serializers.CharField(max_length=100)
    duration_in_number_of_seconds = serializers.IntegerField()
    author_of_the_title = serializers.CharField(max_length=100)
    narrator = serializers.CharField(max_length=100)

    def create(self,validated_data):
        audiobook_type_obj = AudioFile.objects.create(name=validated_data['title_of_the_audiobook'],duration=validated_data['duration_in_number_of_seconds'],
                                file_type=3,host_author=validated_data['author_of_the_title'],narrator=validated_data['narrator'])
    
        return audiobook_type_obj

class UpdateSongTypeSerializer(serializers.Serializer):
    name_of_the_song = serializers.CharField(required=False)
    duration_in_number_of_seconds = serializers.IntegerField(required=False)

    def update(self,instance,validated_data):
        instance.name=validated_data.get('name_of_the_song',instance.name)
        instance.duration=validated_data.get('duration_in_number_of_seconds',instance.duration)
        instance.save()
        return instance

class UpdatePodcastTypeSerializer(serializers.Serializer):
    name_of_the_podcast = serializers.CharField(max_length=100,required=False)
    duration_in_number_of_seconds = serializers.IntegerField(required=False)
    host = serializers.CharField(max_length=100,required=False)
    participants = serializers.ListField(child=serializers.CharField(max_length=100,required=False),max_length=10,required=False)

    def update(self,instance,validated_data):
        instance.name=validated_data.get('name_of_the_podcast',instance.name)
        instance.duration=validated_data.get('duration_in_number_of_seconds',instance.duration)
        instance.host_author = validated_data.get('host',instance.host_author)
        participants = validated_data.get('participants')
        
        if participants:
            Participant.objects.filter(audiofile=instance).delete()
            for participant in participants:
                Participant.objects.create(audiofile=instance,participants=participant)
        instance.save()
        return instance

class UpdateAudioBookTypeSerializer(serializers.Serializer):
    title_of_the_audiobook = serializers.CharField(max_length=100,required=False)
    duration_in_number_of_seconds = serializers.IntegerField(required=False)
    author_of_the_title = serializers.CharField(max_length=100,required=False)
    narrator = serializers.CharField(max_length=100,required=False)

    def update(self,instance,validated_data):
        instance.name=validated_data.get('title_of_the_audiobook',instance.name)
        instance.duration=validated_data.get('duration_in_number_of_seconds',instance.duration)
        instance.host_author = validated_data.get('author_of_the_title',instance.host_author)
        instance.narrator = validated_data.get('narrator',instance.narrator)
        instance.save()
        return instance

class GetSongTypeSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name_of_the_song = serializers.CharField(source='name')
    duration_in_number_of_seconds = serializers.IntegerField(source='duration')
    uploaded_time = serializers.DateTimeField(source='uploaded_at',format="%Y-%m-%d %H:%M:%S")

class GetPodcastTypeSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name_of_the_podcast = serializers.CharField(source='name')
    duration_in_number_of_seconds = serializers.IntegerField(source='duration')
    uploaded_time = serializers.DateTimeField(source='uploaded_at',format="%Y-%m-%d %H:%M:%S")
    host = serializers.CharField(source='host_author')
    participants = serializers.SerializerMethodField()

    # def to_representation(self,instance):
    #     representation = super().to_representation(instance)
    #     representation.update({
    #         'participants':[i.participants for i in Participant.objects.filter(audiofile=instance)]
    #     })
    #     return representation
    
    def get_participants(self,instance):
        return [i.participants for i in instance.participants]

class GetAudioBookTypeSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title_of_the_audiobook= serializers.CharField(source='name')
    duration_in_number_of_seconds = serializers.IntegerField(source='duration')
    author_of_the_title = serializers.CharField(source='host_author')
    narrator = serializers.CharField()
    uploaded_time = serializers.DateTimeField(source='uploaded_at',format="%Y-%m-%d %H:%M:%S")