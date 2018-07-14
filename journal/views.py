from django.core.paginator import Paginator
from django.http import JsonResponse
from django.utils import timezone
from .models import Kid, Journal
from django.shortcuts import render, redirect
from django.views import View

# Create your views here.

KID_DOES_NOT_EXIST = {
    'apiVersion': 1.0,
    'error': {
        'code': 500,
        'message': 'Kid does not exist'
    }
}

NO_RELATIVE = {**KID_DOES_NOT_EXIST, 'error': {
    'code': 500,
    'message': 'Kid cant go alone'
}}


class KidView(View):

    def post(self, request, kid_id):
        try:
            # fields = ['photo', 'name', 'birthday', 'grade', 'is_studying']
            kid = Kid.objects.get(id=kid_id)

            if request.POST.get('photo'):
                kid.photo = request.POST.get('photo')
            if request.POST.get('name'):
                kid.name = request.POST.get('name')
            if request.POST.get('birthday'):
                kid.birthday = request.POST.get('birthday')
            if request.POST.get('grade'):
                kid.grade = request.POST.get('grade')
            if request.POST.get('is_studying'):
                kid.is_studying = request.POST.get('is_studying')
            kid.save()
            return redirect(f'/kids/{kid_id}/')
        except Kid.DoesNotExist:
            return redirect(f'/kids/{kid_id}/')

    def get(self, request, kid_id):
        try:
            kid = Kid.objects.get(id=kid_id)
            return JsonResponse({
                'apiVersion': '1.0',
                'data': {
                    'items': [kid.json, ]
                }
            })
        except Kid.DoesNotExist:
            return JsonResponse(KID_DOES_NOT_EXIST)


class KidsView(View):

    def post(self, request):
        data = {
            'photo': request.POST.get('photo'),
            'name': request.POST.get('name'),
            'birthday': request.POST.get('birthday'),
            'grade': request.POST.get('grade'),
        }
        kid = Kid(**data)
        kid.save()
        return redirect(f'/kids/{kid.id}/')


class KidJournalView(View):

    def get(self, request, kid_id):
        try:
            kid = Kid.objects.get(id=kid_id)
        except Kid.DoesNotExist:
            return JsonResponse(KID_DOES_NOT_EXIST)

        queryset = Journal.objects.filter(kid=kid).order_by('-timestamp')
        paginator = Paginator(queryset, 10)
        offset = request.GET.get('offset', 0)
        return JsonResponse({
            'apiVersion': '1.0',
            'data': {
                'totalItems': paginator.count,
                'numPages': paginator.num_pages,
                'pageIndex': offset,
                'items': [entry.json for entry in paginator.get_page(offset)]
            }
        })

    def post(self, request, kid_id):
        try:
            kid = Kid.objects.get(id=kid_id)
        except Kid.DoesNotExist:
            response = KID_DOES_NOT_EXIST
            return JsonResponse(response)

        relative = request.POST.get('relative')
        if not relative:
            return JsonResponse(NO_RELATIVE)
        last_actions = Journal.objects.filter(kid=kid).order_by('-timestamp')
        if last_actions:
            direction = last_actions.first().direction
            if direction == 'IN':
                new_entry = Journal(kid=kid, timestamp=timezone.now(), direction='OUT', relative=relative)
                new_entry.save()
            if direction == 'OUT':
                new_entry = Journal(kid=kid, timestamp=timezone.now(), direction='IN', relative=relative)
                new_entry.save()
        else:
            new_entry = Journal(kid=kid, timestamp=timezone.now(), direction='IN', relative=relative)
            new_entry.save()

        return redirect(f'/journal/{kid_id}/')


class JournalView(View):

    def get(self, request):

        qs = Journal.objects.all().filter(kid__is_studying=True)
        return JsonResponse({
            'apiVersion': '1.0',
            'data': {
                'items': [entry.json for entry in qs]
            }
        })
