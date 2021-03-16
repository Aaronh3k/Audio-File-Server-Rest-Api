from django.shortcuts import render
from rest_framework.views import APIView,status
from .serializers import (CreateSongTypeSerializer,UpdateSongTypeSerializer,GetSongTypeSerializer,
    CreatePodcastTypeSerializer,CreateAudioBookTypeSerializer,UpdatePodcastTypeSerializer,UpdateAudioBookTypeSerializer,
    GetAudioBookTypeSerializer,GetPodcastTypeSerializer)
from .utils import audio_type_str_to_int
from rest_framework.response import Response
import ast
from .models import AudioFile

class CreateAPIView(APIView):
    def post(self, request):
        data = request.data
        try:
            metadata = ast.literal_eval(data['audioFileMetadata'])
            audio_type=audio_type_str_to_int(data['audioFileType'])
        except:
            return Response({"status": False, "message": "INVALID"}, status=status.HTTP_400_BAD_REQUEST)
        
        if audio_type==1:
            serializer = CreateSongTypeSerializer(data=metadata)
        elif audio_type==2:
            serializer = CreatePodcastTypeSerializer(data=metadata)
        elif audio_type==3:
            serializer = CreateAudioBookTypeSerializer(data=metadata)
        else:
            return Response({"status": False, "message": "INVALID"}, status=status.HTTP_400_BAD_REQUEST)

        if not serializer.is_valid():
            return Response({"status": False, "message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer.save()
            return Response({"status": True, "message": "SUCCESSFULLY CREATED"}, status=status.HTTP_200_OK)

class UpdateAPIView(APIView):
    def put(self,request,audioFileType,audioFileID):
        data = request.data
        try:
            metadata = ast.literal_eval(data['audioFileMetadata'])
            audio_type=audio_type_str_to_int(audioFileType)
            instance = AudioFile.objects.get(id=audioFileID,file_type=audio_type)
        except:
            return Response({"status":False,"message":'INVALID'}, status=status.HTTP_400_BAD_REQUEST)
    
        if audio_type==1:
            serializer = UpdateSongTypeSerializer(instance,data=metadata)
        elif audio_type==2:
            serializer = UpdatePodcastTypeSerializer(instance,data=metadata)
        elif audio_type==3:
            serializer = UpdateAudioBookTypeSerializer(instance,data=metadata)
   
        if not serializer.is_valid():
            return Response({"status": False, "message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer.save()
            return Response({"status": True, "message": "SUCCESSFULLY UPDATED"}, status=status.HTTP_200_OK)

class GetAPIView(APIView):
    def get(self,request,audioFileType,audioFileID=None):
        audio_type=audio_type_str_to_int(audioFileType)
        if audio_type and not audioFileID:
            audiofile_objs = AudioFile.objects.filter(file_type=audio_type)
        elif audioFileType and audioFileID:
            audiofile_objs = AudioFile.objects.filter(file_type=audio_type,id=audioFileID)
        
        if not audiofile_objs:
            return Response({"status":False,"message":'NO DATA FOUND'}, status=status.HTTP_200_OK)
        
        if audio_type==1:
            serializer = GetSongTypeSerializer(audiofile_objs,many=True)
        elif audio_type==2:
            serializer = GetPodcastTypeSerializer(audiofile_objs,many=True)
        elif audio_type==3:
            serializer = GetAudioBookTypeSerializer(audiofile_objs,many=True)

        return Response(serializer.data,status=status.HTTP_200_OK)

class DeleteAPIView(APIView):
    def delete(self,request,audioFileType,audioFileID):
        data = request.data
        audio_type=audio_type_str_to_int(audioFileType)
        try:
            AudioFile.objects.get(id=audioFileID,file_type=audio_type).delete()
            return Response({"status": True, "message": "SUCCESSFULLY DELETED"}, status=status.HTTP_200_OK)
        except:
            return Response({"status":False,"message":'INVALID'}, status=status.HTTP_400_BAD_REQUEST)