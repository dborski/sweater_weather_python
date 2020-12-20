from .base_view import *
from api.popos.road_trip_creator import RoadTripCreator


def _road_trip_requirements_met(body):
    requirements = ['api_key', 'origin', 'destination']
    body_params = set(body)
    user = None
    success = False

    # check if there are any fields missing
    errors = [f'Must include {req}' for req in requirements if req not in body_params]

    if errors:
        return success, errors, user

    # check if a user with submitted API key exists
    try:
        user = User.objects.get(profile__api_key=body['api_key'])
    except ObjectDoesNotExist:
        errors.append('A user does not exist with this API key')
        pass
    else:
        success = True
    
    return success, errors, user


class RoadTripView(APIView):
    def post(self, request):
        body = request.data
        success, errors, user = _road_trip_requirements_met(body)

        if success:
            return RoadTripCreator(body['origin'], body['destination'], user).create_road_trip()
        else:
            return JsonResponse(error_payload(','.join(errors)), status=400)
