""" def get_all_cookies(request):
  cookies = request.COOKIES

  return cookies


def my_view(request):
  cookies = get_all_cookies(request)

  # Afficher tous les cookies
  for cookie in cookies:
    print(cookie) """
