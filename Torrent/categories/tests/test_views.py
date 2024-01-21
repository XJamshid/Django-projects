
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase,Client
from django.urls import reverse
from categories.views import CategoryDetailView,CategoryCreateView,CategoryUpdateView,CategoryDeleteView
from categories.models import Category
from games.models import Game , Screenshots
from accounts.models import CustomUser
from io import BytesIO, StringIO
from PIL import Image
import datetime
class TestViews(TestCase):
    def setUp(self):
        #RequestFactory classidan foydalanib test yozish mumkin
        self.category=Category.objects.create(name='Action')
        self.client=Client()
        self.superuser=CustomUser.objects.create_superuser(
            username='jamshid',
            email='xudoyberdiyevjamshid8@gmail.com',
            password='jamshid1234!@#$',
            is_staff=True
        )#superuser yaratish oddiy user yaratishda create_user metodi qo'llanadi
        self.client.force_login(self.superuser)
    def test_category_detail_view(self):
        file_obj = BytesIO() # file yaratdik
        image_file = Image.new('RGB', size=(100, 100), color=(256, 0, 0))#image_file yaratdik
        image_file.save(file_obj, 'png') #Yratgan file imizga rasmni saqladik binary ko'rinishida
        torrent_file =StringIO()
        torrent_file.write('Test torrent file')
        image = SimpleUploadedFile('image.png', file_obj.read(), content_type='image/png')#Image file ni yukladik
        torrent=SimpleUploadedFile('torrent_file.torrent',torrent_file.read(),content_type='file/torrent')
        response=self.client.get(reverse('category',args=[str(self.category.pk)]))
        screenshot=Screenshots.objects.create(
            game_name='Test',
            screenshots=image
        )
        game=Game.objects.create(
            name='Test',
            release_date=datetime.date(2022, 12, 25),
            poster=image,
            trailer='https://www.youtube.com/watch?v=o3V-GvvzjE4',
            developer='developer',
            platform='platform',
            os='os',
            processor='processor',
            ram='ram',
            video_card='video_card',
            disk_space='disk_space',
            file=torrent,
            about='about',
        )
        game.category.add(self.category)
        game.screenshots.add(screenshot)
        game=Game.objects.filter(category__name='Action')
        self.assertTemplateUsed(response,'category.html')
        self.assertEqual(response.status_code,200)
        self.assertTrue(game.exists())
    def test_category_create_view(self):
        response=self.client.post(
            reverse('category_create'),
            data={'name':'Adventure'},)
        adventure=Category.objects.get(name='Adventure')
        self.assertTemplateUsed("category_create.html")
        self.assertEqual(response.status_code,302)
        self.assertEqual(adventure.pk,2)
    def test_category_update_view(self):
        response=self.client.post(reverse('category_update',args=[str(1)]),data={'name':'Horror'})
        horror=Category.objects.get(pk=1)
        self.assertEqual(horror.name, 'Horror')
        self.assertTemplateUsed("category_update.html")
        self.assertEqual(response.status_code,302)
    def test_category_delete_view(self):
        response=self.client.post(reverse('category_delete',args=[str(1)]))
        category=Category.objects.all()
        self.assertFalse(category.exists())
        self.assertTemplateUsed("category_delete.html")
        self.assertEqual(response.status_code,302)



#Image va File ni yaratishga misollar
"""def test_valid_receipt_pdf(self):
#Checks form is valid with SimpleUploadeFile extension pdf
    # Use StringIO to create files
    pdf_file = StringIO.StringIO('portable docuement format file')
    # Use PIL Image to create new png and pdf files
    Image.new('RGB', size=(50, 50), color=(256, 0, 0)).save(pdf_file, 'pdf')
    pdf_file.seek(0)
    file = SimpleUploadedFile('test_file.pdf', pdf_file.read())
    # Data for the form
    data_pdf = {'description': 'description pdf',
                'amount': 1,
                }
    files = {'receipt_image': file}
    form_pdf = ReceiptForm(data_pdf, files, instance=Receipt(application=self.application))

    self.assertTrue(form_pdf.is_valid(), msg=form_pdf.errors)
    form_pdf.save()"""


"""
small_gif = (
   # b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x00\x00\x00\x21\xf9\x04'
    #b'\x01\x0a\x00\x01\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02'
    #b'\x02\x4c\x01\x00\x3b'
)
uploaded = SimpleUploadedFile('small.gif', small_gif, content_type='image/gif')"""


"""def get_image_file(name, ext='png', size=(50, 50), color=(256, 0, 0)):
    file_obj = BytesIO()
    image = Image.new("RGBA", size=size, color=color)
    image.save(file_obj, ext)
    file_obj.seek(0)
    return File(file_obj, name=name)


def test_upload_image(self):
    c = APIClient()
    image1 = self.get_image('image.png')
    image2 = self.get_image('image2.png')
    data =
    {
        "image1": iamge1,
        "image2": image2,
    }


response = c.post('/api_address/', data)
self.assertEqual(response.status_code, 201) 
"""

"""
file_obj=BytesIO()
image_file=Image.new('RGB',size=(100, 100),color=(256, 0, 0))
image_file.save(file_obj,'png')
#file_obj.seek(0)
image = SimpleUploadedFile('image.png', file_obj.getvalue(), content_type='image/png')
"""

"""
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.core.urlresolvers import reverse
from django.core.files import File
from django.utils.six import BytesIO

from .forms import UploadImageForm

from PIL import Image
from io import StringIO


def create_image(storage, filename, size=(100, 100), image_mode='RGB', image_format='PNG'):
   data = BytesIO()
   Image.new(image_mode, size).save(data, image_format)
   data.seek(0)
   if not storage:
       return data
   image_file = ContentFile(data.read())
   return storage.save(filename, image_file)


class UploadImageTests(TestCase):
   def setUp(self):
       super(UploadImageTests, self).setUp()


   def test_valid_form(self):
       '''
       valid post data should redirect
       The expected behavior is to show the image
       '''
       url = reverse('image')
       avatar = create_image(None, 'avatar.png')
       avatar_file = SimpleUploadedFile('front.png', avatar.getvalue())
       data = {'image': avatar_file}
       response = self.client.post(url, data, follow=True)
       image_src = response.context.get('image_src')

       self.assertEquals(response.status_code, 200)
       self.assertTrue(image_src)
       self.assertTemplateUsed('content_upload/result_image.html')
"""

"""def test_upload_video(self):
    video = SimpleUploadedFile("file.mp4", "file_content", content_type="video/mp4")
    self.client.post(reverse('app:some_view'), {'video': video})"""


#upload = SimpleUploadedFile("file.txt", b"file_content")