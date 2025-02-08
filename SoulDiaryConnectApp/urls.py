from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),  # Home page
    path('login/', views.login_view, name='login'),  # Login page
    path('register/', views.register_view, name='register'),  # Registration page
    path('logout/', views.logout_view, name='logout'),
    path('medico/home/', views.medico_home, name='medico_home'),
    path('paziente/home/', views.paziente_home, name='paziente_home'),
    path('medico/note/<int:nota_id>/modifica/', views.modifica_testo_medico, name='modifica_testo_medico'),
    path('medico/personalizza/', views.personalizza_generazione, name='personalizza_generazione'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
