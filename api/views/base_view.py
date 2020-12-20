from django.http import JsonResponse
from rest_framework.views import APIView
from django.core.exceptions import ObjectDoesNotExist
import api.popos.services_helper as sh
from django.contrib.auth.models import User


def error_payload(error, code=400):
        return {
            'success': False,
            'error': code,
            'errors': error
        }
