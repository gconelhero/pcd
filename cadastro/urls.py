from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.signup_view, name='signup'),
    path('cadastro_associado/', views.cadastro_associado, name='cadastro_associado'),
    path('associado/', views.associado, name='associado'),
    path('card/', views.card, name='card'), 
    path('documents/<int:pk>', views.document_view, name='documents'),
    path('pdf_view/<int:pk>/<str:file_name>', views.pdf_view, name='pdf_view'),

]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
