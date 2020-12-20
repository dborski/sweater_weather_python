from django.test import TestCase
from django.contrib.auth.models import User
from api.models import Profile


class RoadTripModelTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            username='user1@email.com', email='user1@email.com', password='password'
            )
        self.road_trip1 = self.user1.roadtrip_set.create(
            name='road trip 1',
            start_city='Denver,CO',
            end_city='Taos,NM',
            travel_time='4 hours 24 minutes',
            arrival_temp=76.54,
            arrival_conditions='mostly cloudy',
        )

    def test_string_representation(self):
        self.assertEqual(str(self.road_trip1), self.road_trip1.name)
