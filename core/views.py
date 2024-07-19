from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.urls import reverse
from .models import User, TableModel
from .forms import UserForm, CameraForm, TableModelForm
from .models import MaterialEvidence

from .forms import MaterialEvidenceForm
from .models import Case
from .forms import CaseForm
from .models import Camera
from .models import Session
from .models import AuditEntry

from rest_framework import viewsets
from .models import AuditEntry
from .serializers import AuditEntrySerializer

from .models import Camera
from .serializers import CameraSerializer

from .models import Case
from .serializers import CaseSerializer

from .serializers import MaterialEvidenceSerializer

from django.http import HttpResponse
from .utils import generate_qr_code


from .forms import MaterialEvidenceGroupForm


from django.core.files.base import ContentFile
import base64



def user_list(request):
    users = User.objects.all()
    return render(request, 'core/user_list.html', {'users': users})


def user_create(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            photo_data = request.POST.get('photo_data')
            if photo_data:
                format, imgstr = photo_data.split(';base64,')
                ext = format.split('/')[-1]
                user.photo = ContentFile(base64.b64decode(imgstr), name=f'{user.username}.{ext}')
            user.save()
            return redirect(reverse('user_list'))
    else:
        form = UserForm()
    return render(request, 'core/user_form.html', {'form': form})

# def user_create(request):
#     if request.method == 'POST':
#         form = UserForm(request.POST)
#         if form.is_valid():
#             user = form.save(commit=False)
#             user.photo_data = form.cleaned_data['photo_data']
#             user.save()
#             return redirect(reverse('user_list'))
#     else:
#         form = UserForm()
#     return render(request, 'core/user_form.html', {'form': form})


def user_edit(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect(reverse('user_list'))
    else:
        form = UserForm(instance=user)
    return render(request, 'core/user_form.html', {'form': form})


def material_evidence_list(request):
    materials = MaterialEvidence.objects.all()
    return render(request, 'core/material_evidence_list.html', {'materials': materials})


def material_evidence_create(request):
    if request.method == 'POST':
        form = MaterialEvidenceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('material_evidence_list'))
    else:
        form = MaterialEvidenceForm()
    return render(request, 'core/material_evidence_form.html', {'form': form})


def material_evidence_edit(request, material_id):
    material = get_object_or_404(MaterialEvidence, id=material_id)
    if request.method == 'POST':
        form = MaterialEvidenceForm(request.POST, instance=material)
        if form.is_valid():
            form.save()
            return redirect(reverse('material_evidence_list'))
    else:
        form = MaterialEvidenceForm(instance=material)
    return render(request, 'core/material_evidence_form.html', {'form': form})


def case_list(request):
    cases = Case.objects.all()
    return render(request, 'core/case_list.html', {'cases': cases})


def case_create(request):
    if request.method == 'POST':
        form = CaseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('case_list'))
    else:
        form = CaseForm()
    return render(request, 'core/case_form.html', {'form': form})


def case_edit(request, case_id):
    case = get_object_or_404(Case, id=case_id)
    if request.method == 'POST':
        form = CaseForm(request.POST, instance=case)
        if form.is_valid():
            form.save()
            return redirect(reverse('case_list'))
    else:
        form = CaseForm(instance=case)
    return render(request, 'core/case_form.html', {'form': form})


def camera_list(request):
    return render(request, 'core/camera_list.html')


def camera_edit(request, camera_id):
    camera = get_object_or_404(Camera, id=camera_id)
    if request.method == 'POST':
        form = CameraForm(request.POST, instance=camera)
        if form.is_valid():
            form.save()
            return redirect(reverse('camera_list'))
    else:
        form = CameraForm(instance=camera)
    return render(request, 'core/camera_form.html', {'form': form})


def camera_view(request, camera_id):
    camera = get_object_or_404(Camera, id=camera_id)
    return render(request, 'core/camera_view.html', {'camera': camera})


def face_auth(request):
    # Заглушка для аутентификации по лицу
    return render(request, 'core/face_auth.html')


def session_list(request):
    sessions = Session.objects.all()
    return render(request, 'core/session_list.html', {'sessions': sessions})


def audit_list(request):
    audit_entries = AuditEntry.objects.all()
    return render(request, 'core/audit_list.html', {'audit_entries': audit_entries})


def table_model_list(request):
    table_models = TableModel.objects.all()
    return render(request, 'core/table_model_list.html', {'table_models': table_models})


def table_model_create(request):
    if request.method == 'POST':
        form = TableModelForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('table_model_list')
    else:
        form = TableModelForm()
    return render(request, 'core/table_model_form.html', {'form': form})


def table_model_edit(request, model_id):
    table_model = get_object_or_404(TableModel, id=model_id)
    if request.method == 'POST':
        form = TableModelForm(request.POST, instance=table_model)
        if form.is_valid():
            form.save()
            return redirect('table_model_list')
    else:
        form = TableModelForm(instance=table_model)
    return render(request, 'core/table_model_form.html', {'form': form})


class AuditEntryViewSet(viewsets.ModelViewSet):
    queryset = AuditEntry.objects.all()
    serializer_class = AuditEntrySerializer


class CameraViewSet(viewsets.ModelViewSet):
    queryset = Camera.objects.all()
    serializer_class = CameraSerializer


class CaseViewSet(viewsets.ModelViewSet):
    queryset = Case.objects.all()
    serializer_class = CaseSerializer


class MaterialEvidenceViewSet(viewsets.ModelViewSet):
    queryset = MaterialEvidence.objects.all()
    serializer_class = MaterialEvidenceSerializer


def qr_code_view(request):
    data = "Some data to encode in QR code"
    img = generate_qr_code(data)
    response = HttpResponse(content_type="image/png")
    img.save(response, "PNG")
    return response


def generate_material_evidence_qr_code(request, evidence_id):
    material_evidence = get_object_or_404(MaterialEvidence, id=evidence_id)
    qr_image = generate_qr_code(material_evidence.barcode)
    response = HttpResponse(content_type="image/png")
    qr_image.save(response, "PNG")
    return response


def create_evidence_group(request):
    if request.method == 'POST':
        form = MaterialEvidenceGroupForm(request.POST)
        if form.is_valid():
            evidence_ids = form.cleaned_data['evidence_ids']
            data = ','.join(str(e.id) for e in evidence_ids)
            qr_image = generate_qr_code(data)
            response = HttpResponse(content_type="image/png")
            qr_image.save(response, "PNG")
            return response
    else:
        form = MaterialEvidenceGroupForm()
    return render(request, 'core/create_evidence_group.html', {'form': form})

# def filtered_list_view(request):
#     filters = {
#         'field1': request.GET.get('field1'),
#         'field2': request.GET.get('field2')
#     }
#     queryset = SomeModel.objects.all()
#     filtered_queryset = apply_filters(queryset, filters)
#     return render(request, 'core/filtered_list.html', {'objects': filtered_queryset})