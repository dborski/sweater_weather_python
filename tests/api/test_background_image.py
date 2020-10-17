import json
from django.test import TestCase


class GetBackgroundImageTest(TestCase):
  def test_get_background_image_for_city(self):
    response = self.client.get('/api/v1/backgrounds?location=san diego,ca')

    # json_response = response.json()

    self.assertEqual(response.status_code, 200)
    self.assertEqual(json_response['data']['type'], 'image')
    self.assertIsNone(json_response['data']['id'])
    self.assertIsNotNone(json_response['data']['image']['location'])
    self.assertIsNotNone(json_response['data']['image']['image_url'])
    self.assertIsNotNone(json_response['data']['image']['credit']['source'])
    self.assertIsNotNone(json_response['data']['image']['credit']['author'])
    self.assertIsNotNone(json_response['data']['image']['credit']['logo'])


# {
#     "data": {
#         "type": "image",
#         "id": null,
#         "image": {
#             "location": "denver,co",
#             "image_url": "https://pixabay.com/get/54e6d4444f50a814f1dc8460962930761c38d6ed534c704c7c2878dd954dc451_640.jpg",
#             "credit": {
#                 "source": "pixabay.com",
#                 "author": "quinntheislander",
#                 "logo": "https://pixabay.com/static/img/logo_square.png"
#             }
#         }
#     }
# }
