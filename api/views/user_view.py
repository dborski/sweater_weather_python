from .base_view import *
from django.contrib.auth import authenticate, login
import uuid


def _user_payload(user):
    return {
        "data": {
            "type": "users",
            "id": user.id,
            "attributes": {
                "email": user.email,
                "api_key": user.profile.api_key
            }
        }
    }

def _registration_success(body):
    requirements = ['email', 'password', 'password_confirmation']
    body_params = set(body)
    success = False

    # check if there are any fields missing
    errors = [
        f'Missing {req}' for req in requirements if req not in body_params]

    if errors:
        return success, errors

    # check if email is unique
    try:
        user = User.objects.get(email=body['email'])
    except ObjectDoesNotExist:
        pass
    else:
        errors.append("This email already exists")
        return success, errors

    # check if passwords match
    if body['password'] == body['password_confirmation']:
        success = True
    else:
        errors.append("The passwords do not match")

    return success, errors

def _login_success(request, body):
    requirements = ['username', 'password']
    body_params = set(body)
    user = None

    # check if there are any fields missing
    errors = [
        f'Must include {req}' for req in requirements if req not in body_params]

    if not errors:
        user = authenticate(
            request, username=body['username'], password=body['password'])
        if user is not None:
            login(request, user)
            success = True
        else:
            errors.append('Credentials are invalid')
            success = False
    else:
        success = False

    return success, errors, user

class UserRegistrationView(APIView):
    def post(self, request):
        body = request.data
        success, errors = _registration_success(body)

        if success:
            new_user = User.objects.create_user(
                body['email'],
                body['email'],
                body['password']
            )
            return JsonResponse(_user_payload(new_user), status=201)
        else:
            return JsonResponse(error_payload(','.join(errors)), status=400)


class UserLoginView(APIView):
    def post(self, request):
        body = request.data
        success, errors, user = _login_success(request, body)

        if success:
            return JsonResponse(_user_payload(user), status=200)
        else:
            return JsonResponse(error_payload('.'.join(errors), 401), status=401)
