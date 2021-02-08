from django.shortcuts import render
from .forms import SimpleUploadForm, ImageUploadForm
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from .cv_functions import cv_detect_face

# Create your views here.

def first_view(request):
    return render(request, 'opencv_webapp/first_view.html', {})

def simple_upload(request):

    if request.method == 'POST':
        # print(request.POST)
        # print(request.FILES) : <MultiValueDict: {'image': [<InMemoryUploadedFile: oasis.jpeg (image/jpeg)>]}>
        # print(request.FILES['image'])
        form = SimpleUploadForm(request.POST, request.FILES) #데이터를 나눠 받는다

        if form.is_valid(): #파일 검증
            myfile = request.FILES['image']

            fs = FileSystemStorage() #파일 저장 관련 기능 -> media 폴더로 업로드해준다
            filename = fs.save(myfile.name, myfile) #파일 이름, 얻어낸 이미지 파일
            uploaded_file_url = fs.url(filename) #받아낸 파일의 url

            context = {"form":form, "uploaded_file_url":uploaded_file_url}
            return render(request, 'opencv_webapp/simple_upload.html', context)

    else:
        form = SimpleUploadForm()
        context = {"form":form}
        return render(request, 'opencv_webapp/simple_upload.html', context)

def detect_face(request):

    if request.method == "POST":
        form = ImageUploadForm(request.POST, request.FILES)

        if form.is_valid():
            #commit=False : 이용자에게 받은 정보를 DB에 저장하기 전에 무언가 작업을 하기 위해
            post = form.save(commit=False)
            post.save()

            # imageURL 만들어주기 : /media/oasis.jpeg
            # settings.py의 미디어 폴더 URL(media) + POST로 얻어낸 파일(DB의 documnet) 이름 str(oasis.jpeg)
            imageURL = settings.MEDIA_URL + form.instance.document.name

            #cv_detect_face('./media/oasis.jpeg')
            cv_detect_face(settings.MEDIA_ROOT_URL + imageURL)

            context = {'form':form, 'post':post}
            return render(request, 'opencv_webapp/detect_face.html', context)

    else:
        form = ImageUploadForm()
        return render(request, 'opencv_webapp/detect_face.html', {'form':form})
