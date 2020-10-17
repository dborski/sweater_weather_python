class PhotoParser:
  def __init__(self, photo_data, location):
    self.image_url = photo_data['urls']['raw']
    self.user_data = photo_data['user']
    self.location = location
