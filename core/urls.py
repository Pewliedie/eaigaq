from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views, auth_views
from .views import AuditEntryViewSet, CameraViewSet, CaseViewSet, MaterialEvidenceViewSet
from .views import generate_material_evidence_qr_code, create_evidence_group
from django.contrib import admin
from django.views.generic import RedirectView


router = DefaultRouter()
router.register(r'audit', AuditEntryViewSet)
router.register(r'cameras', CameraViewSet)
router.register(r'cases', CaseViewSet)
router.register(r'material_evidences', MaterialEvidenceViewSet)

urlpatterns = [
    path('users/', views.user_list, name='user_list'),
    path('users/create/', views.user_create, name='user_create'),
    path('users/edit/<int:user_id>/', views.user_edit, name='user_edit'),
    path('materials/', views.material_evidence_list, name='material_evidence_list'),
    path('materials/create/', views.material_evidence_create, name='material_evidence_create'),
    path('materials/edit/<int:material_id>/', views.material_evidence_edit, name='material_evidence_edit'),
    path('cases/', views.case_list, name='case_list'),
    path('cases/create/', views.case_create, name='case_create'),
    path('cases/edit/<int:case_id>/', views.case_edit, name='case_edit'),
    path('cameras/', views.camera_list, name='camera_list'),
    path('face_auth/', views.face_auth, name='face_auth'),
    path('sessions/', views.session_list, name='session_list'),
    path('audit/', views.audit_list, name='audit_list'),
    path('login/', auth_views.login_view, name='login'),
    path('logout/', auth_views.logout_view, name='logout'),
    path('register/', views.user_create, name='register'),  # Маршрут для регистрации
    path('table_model/', views.table_model_list, name='table_model_list'),
    path('table_model/create/', views.table_model_create, name='table_model_create'),
    path('table_model/edit/<int:model_id>/', views.table_model_edit, name='table_model_edit'),
    path('materials/<int:evidence_id>/qr/', views.generate_material_evidence_qr_code, name='generate_material_evidence_qr_code'),
    path('materials/group/create/', views.create_evidence_group, name='create_evidence_group'),
]

urlpatterns += router.urls



# from django.urls import path, include
# from rest_framework.routers import DefaultRouter
# from . import views, auth_views
# from .views import AuditEntryViewSet, CameraViewSet, CaseViewSet, MaterialEvidenceViewSet
# from .views import generate_material_evidence_qr_code, create_evidence_group
#
#
# router = DefaultRouter()
# router.register(r'audit', AuditEntryViewSet)
# router.register(r'cameras', CameraViewSet)
# router.register(r'cases', CaseViewSet)
# router.register(r'material_evidences', MaterialEvidenceViewSet)
#
# urlpatterns = [
#     path('users/', views.user_list, name='user_list'),
#     path('users/create/', views.user_create, name='user_create'),
#     path('users/edit/<int:user_id>/', views.user_edit, name='user_edit'),
#     path('materials/', views.material_evidence_list, name='material_evidence_list'),
#     path('materials/create/', views.material_evidence_create, name='material_evidence_create'),
#     path('materials/edit/<int:material_id>/', views.material_evidence_edit, name='material_evidence_edit'),
#     path('cases/', views.case_list, name='case_list'),
#     path('cases/create/', views.case_create, name='case_create'),
#     path('cases/edit/<int:case_id>/', views.case_edit, name='case_edit'),
#     path('cameras/', views.camera_list, name='camera_list'),
#     path('face_auth/', views.face_auth, name='face_auth'),
#     path('sessions/', views.session_list, name='session_list'),
#     path('audit/', views.audit_list, name='audit_list'),
#     path('login/', auth_views.login_view, name='login'),
#     path('logout/', auth_views.logout_view, name='logout'),
#     path('table_model/', views.table_model_list, name='table_model_list'),
#     path('table_model/create/', views.table_model_create, name='table_model_create'),
#     path('table_model/edit/<int:model_id>/', views.table_model_edit, name='table_model_edit'),
#     path('materials/<int:evidence_id>/qr/', generate_material_evidence_qr_code, name='generate_material_evidence_qr_code'),
#     path('materials/group/create/', create_evidence_group, name='create_evidence_group'),
#
# ]
#
# # Добавляем маршруты, зарегистрированные через роутер
# urlpatterns += router.urls
#
