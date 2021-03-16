from rest_framework.test import APITestCase
from .models import AudioFile,Participant
from rest_framework import status
import random,string

class SongFileTypeTests(APITestCase):
    
    def setUp(self):
        AudioFile.objects.create(name='Testing',duration=150,file_type=1)
        AudioFile.objects.create(name='Testing-2',duration=1150,file_type=1)
        AudioFile.objects.create(name='Testing-3',duration=550,file_type=1)

    def test_get(self):
        url_patterns_pass = ['/api/get/SONG_FILE/1','/api/get/SONG_FILE/3','/api/get/SONG_FILE','/api/get/SONG_FILE/4']
        url_patterns_not_found = ['/api/get/SONG_FILE/','/api/get/Song_File/','/api/get']
        
        for url in url_patterns_pass:
            response = self.client.get(url,format='json')
            self.assertEqual(response.status_code,status.HTTP_200_OK)
        
        for url in url_patterns_not_found:
            response = self.client.get(url,format='json')
            self.assertEqual(response.status_code,status.HTTP_404_NOT_FOUND)

    def test_create(self):
        data_pass=[{"audioFileType":"SONG_FILE","audioFileMetadata":str({
                    "name_of_the_song":"Test Name",
                    "duration_in_number_of_seconds":100
                })}]
        data_fail=[{"audioFileType":"SONGFILE","audioFileMetadata":str({
                    "name_of_the_song":"Test Name",
                    "duration_in_number_of_seconds":100
                })},
                {"audioFileType":"SONG_FILE","audioFileMetadata":str({
                    "name_of_the_song":"Test Name"
                })}]
        
        for data in data_pass: 
            response=self.client.post('/api/audiofile/create-api',data,format='json')
            self.assertEqual(response.status_code, status.HTTP_200_OK)

        for data in data_fail:
            response=self.client.post('/api/audiofile/create-api',data,format='json')
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_update(self):
        instance=AudioFile.objects.create(name='Testing-5',duration=1550,file_type=1)
        
        data_pass=[{"audioFileMetadata":str({
                    "name_of_the_song":"TestName",
                })},
                {"audioFileMetadata":str({
                    "name_of_the_song":"TestName",
                    "duration_in_number_of_seconds":100
                })},
                {"audioFileMetadata":str({
                    "duration_in_number_of_seconds":1001
                })}]
        
        data_fail=[{str({
                    "name_of_the_song":"Test Name",
                    "duration_in_number_of_seconds":3400
                })}]
                
        for data in data_pass:
            response=self.client.put(f'/api/update/SONG_FILE/{instance.id}',data,format='json')
            self.assertEqual(response.status_code, status.HTTP_200_OK)

        for data in data_fail:
            response=self.client.put(f'/api/update/SONG_FILE/{instance.id}',data,format='json')
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete(self):
        instance1=AudioFile.objects.create(name='Testing-5',duration=1550,file_type=1)
        instance2=AudioFile.objects.create(name='Testing-6',duration=1850,file_type=1)
        
        url_patterns_pass = [f'/api/delete/SONG_FILE/{instance1.id}',f'/api/delete/SONG_FILE/{instance2.id}']
        url_patterns_fail = ['/api/delete/SONG_FILE/700','/api/delete/Song_File/55']
        
        for url in url_patterns_pass:
            response = self.client.delete(url,format='json')
            self.assertEqual(response.status_code,status.HTTP_200_OK)
        
        for url in url_patterns_fail:
            response = self.client.delete(url,format='json')
            self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)

class PodcastFileTypeTests(APITestCase):
    
    def setUp(self):
        self.i1=AudioFile.objects.create(name='Testing',duration=150,file_type=2,host_author='Marl')
        [Participant.objects.create(audiofile=self.i1,participants=i) for i in ['AA','BB','CC','DD','EE','FF','GG','PP','QQ','YY']]
        self.i2=AudioFile.objects.create(name='Testing-2',duration=1150,file_type=2,host_author='Mary')
        Participant.objects.create(audiofile=self.i2,participants='AACC')
        self.i3=AudioFile.objects.create(name='Testing-3',duration=550,file_type=2,host_author='Mark')
        Participant.objects.create(audiofile=self.i3,participants='AALL')

    def test_get(self):
        url_patterns_pass = [f'/api/get/PODCAST_FILE/{self.i1.id}',f'/api/get/PODCAST_FILE/{self.i3.id}','/api/get/PODCAST_FILE','/api/get/PODCAST_FILE/48']
        url_patterns_not_found = ['/api/get/PODCAST_FILE/','/api/get/Podcast_File/','/api/get']
        
        for url in url_patterns_pass:
            response = self.client.get(url,format='json')
            self.assertEqual(response.status_code,status.HTTP_200_OK)
        
        for url in url_patterns_not_found:
            response = self.client.get(url,format='json')
            self.assertEqual(response.status_code,status.HTTP_404_NOT_FOUND)

    def test_create(self):
        data_pass=[{"audioFileType":"PODCAST_FILE","audioFileMetadata":str({
                    "name_of_the_podcast":"Test Name",
                    "duration_in_number_of_seconds":100,
                    "host":"Dark",
                    "participants":[str(i) for i in range(10)]
                })}]
        data_fail=[{"audioFileType":"PODCAST_FILE","audioFileMetadata":str({
                    "name_of_the_podcast":"Test Name",
                    "duration_in_number_of_seconds":100,
                    "host":"Dark",
                    "participants":[str(i) for i in range(11)]
                })},
                {"audioFileType":"PODCAST_FILE","audioFileMetadata":str({
                    "name_of_the_song":''.join(random.choices(string.ascii_lowercase,k=101)),
                    "duration_in_number_of_seconds":100,
                    "host":"Dark",
                    "participants":[str(i) for i in range(6)]
                })},
                {"audioFileType":"PODCAST_FILE","audioFileMetadata":str({
                    "name_of_the_podcast":''.join(random.choices(string.ascii_lowercase,k=19)),
                    "duration_in_number_of_seconds":100,
                    "host":"Dark",
                })}]
        
        for data in data_pass:
            response=self.client.post('/api/audiofile/create-api',data,format='json')
            self.assertEqual(response.status_code, status.HTTP_200_OK)

        for data in data_fail:
            response=self.client.post('/api/audiofile/create-api',data,format='json')
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_update(self):
        data_pass=[{"audioFileMetadata":str({
                    "name_of_the_podcast":"TestName",
                })},
                {"audioFileMetadata":str({
                    "name_of_the_podcast":"TestName",
                    "duration_in_number_of_seconds":111
                })},
                {"audioFileMetadata":str({
                    "duration_in_number_of_seconds":1001,
                    "host":"Dark House rt",
                    "participants":[str(i) for i in range(11,17)]
                })}]
        
        data_fail=[{str({
                    "name_of_the_song":"Test Name",
                    "duration_in_number_of_seconds":3400
                })}]
                
        for data in data_pass:
            response=self.client.put(f'/api/update/PODCAST_FILE/{self.i1.id}',data,format='json')
            self.assertEqual(response.status_code, status.HTTP_200_OK)

        for data in data_fail:
            response=self.client.put(f'/api/update/PODCAST_FILE/{self.i1.id}',data,format='json')
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class AudioBookFileTypeTests(APITestCase):
    def setUp(self):
        self.i1=AudioFile.objects.create(name='Testing',duration=150,file_type=3,host_author='Marl',narrator='VVV')
        self.i2=AudioFile.objects.create(name='Testing-2',duration=1150,file_type=3,host_author='Mary',narrator='WWW')
        self.i3=AudioFile.objects.create(name='Testing-3',duration=550,file_type=3,host_author='Mark',narrator='RRR')
 
    def test_get(self):
        url_patterns_pass = [f'/api/get/AUDIIOBOOK_FILE/{self.i1.id}',f'/api/get/AUDIOBOOK_FILE/{self.i3.id}','/api/get/AUDIOBOOK_FILE','/api/get/AUDIOBOOK_FILE/48']
        url_patterns_not_found = ['/api/get/AUDIOBOOK_FILE/','/api/get/AUDIOBOOK_File/','/api/get']
        
        for url in url_patterns_pass:
            response = self.client.get(url,format='json')
            self.assertEqual(response.status_code,status.HTTP_200_OK)
        
        for url in url_patterns_not_found:
            response = self.client.get(url,format='json')
            self.assertEqual(response.status_code,status.HTTP_404_NOT_FOUND)

    def test_create(self):
        data_pass=[{"audioFileType":"AUDIOBOOK_FILE","audioFileMetadata":str({
                    "title_of_the_audiobook":"Test Name",
                    "duration_in_number_of_seconds":100,
                    "author_of_the_title":"DarkXXX",
                    "narrator":'Cheng'
                })}]
        data_fail=[{"audioFileType":"AUDIOBOOK_FILE","audioFileMetadata":str({
                    "name_of_the_podcast":"TestccccName",
                    "author_of_the_title":"LLLL",
                    "narrator":'ChengUUUU'
                })},
                {"audioFileType":"AUDIOBOOK_FILE","audioFileMetadata":str({
                    "title_of_the_audiobook":"Test Name",
                })},
                {"audioFileType":"AUDIOBOOK_FILE","audioFileMetadata":str({
                    "title_of_the_audiobook":"Test Name",
                    "duration_in_number_of_seconds":100,
                    "author_of_the_title":''.join(random.choices(string.ascii_lowercase,k=101)),
                    "narrator":'Cheng'
                })}]
        
        for data in data_pass:
            response=self.client.post('/api/audiofile/create-api',data,format='json')
            self.assertEqual(response.status_code, status.HTTP_200_OK)

        for data in data_fail:
            response=self.client.post('/api/audiofile/create-api',data,format='json')
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_update(self):
        data_pass=[{"audioFileMetadata":str({
                    "title_of_the_audiobook":"TestName",
                })},
                {"audioFileMetadata":str({
                    "title_of_the_audiobook":"TestName",
                    "duration_in_number_of_seconds":111
                })},
                {"audioFileMetadata":str({
                    "duration_in_number_of_seconds":1001,
                    "author_of_the_title":"Dark House rt",
                    "narrator":'oooo'
                })}]
        
        data_fail=[{str({
                    "title_of_the_audiobook":"Test Name",
                    "duration_in_number_of_seconds":3400
                })}]
                
        for data in data_pass:
            response=self.client.put(f'/api/update/AUDIOBOOK_FILE/{self.i1.id}',data,format='json')
            self.assertEqual(response.status_code, status.HTTP_200_OK)

        for data in data_fail:
            response=self.client.put(f'/api/update/AUDIOBOOK_FILE/{self.i1.id}',data,format='json')
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)