from django.db import models

# Create your models here.
class ImageUploadModel(models.Model):

    #사진 설명
    # blank=True : null이 들어와도 괜찮다.
    description = models.CharField(max_length=255, blank=True)

    #이미지(media 폴더에 저장한 URL 경로)
    #이미지 이름에 현재 날짜 추가 (media/image.jpg => images/2021/02/08/image.jpg)
    document = models.ImageField(upload_to='images/%Y/%m/%d')

    #이미지 입력 날짜
    #입력 당시 날짜와 시간 곧바로 추가
    uploaded_at = models.DateTimeField(auto_now_add=True)
