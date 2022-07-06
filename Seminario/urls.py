from django.contrib import admin
from django.urls import path
from Quiz.views import *
from django.conf import settings
from django.conf.urls.static import static
 
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('details/<int:quiz_id>', quizDetails, name='quizDetails'),
    path('start/<int:quiz_id>', start, name='start'),
    path('attempt/<int:attempt_id>', attempt,name='attempt'),
    path('answer/<int:attempt_id>', answer,name='attempt'),
]

urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
