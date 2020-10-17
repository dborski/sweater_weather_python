def _background_payload():
  return {
      "data": {
          "type": "image",
          "id": None,
          "image": {
              "location": None,
              "image_url": None,
              "credit": None
              }
          }
      }


class PhotoParser:
  def __init__(self, photo_data, location):
    self.image_url = photo_data['urls']['raw']
    self.user_data = photo_data['user']
    self.location = location

  def get_credit_info(self):
    return {
      "source": "unsplash.com",
      "author": self.user_data['username'],
      "logo": "https://unsplash-assets.imgix.net/marketing/press-logotype.svg?auto=format&fit=crop&q=60"
    }

  def get_photo_payload(self):
    payload = _background_payload()
    payload['data']['image']['location'] = self.location
    payload['data']['image']['image_url'] = self.image_url
    payload['data']['image']['credit'] = self.get_credit_info()

    return payload
