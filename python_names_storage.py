from bs4 import BeautifulSoup
from google.cloud import storage
from google.oauth2 import service_account
import requests
import csv

headers = {
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

credentials_dict = {
  "type": "service_account",
  "project_id": "eloquent-grail-304120",
  "private_key_id": "edc551a73b1f756f529218cdb1cfc0a8c00df3c0",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQCzFy19NxIQ95Z3\nD74CZhSBVmtHUOHLkaeUixfgANihEzBg/JXADmhxInuEKfhGwxkRfY8S5PzAtPX1\nYGiz/R+FvAIDhVNy+NARiQBNNOmuvuJIbubBFj9aZzE2Rax06LZuuPufgG+kspf5\n0M4DptbU6XHlyipm6YlOZjhNjlkVfodREaluslOd5LUvuZ6VavrM+/5Tt6pX7Hjt\nNNFVvLk966clseeTZo1HOtSrhZSOST6QcwMuTF5rISEPseoFHkQW6RUo7tMTmpdD\nTQuVra/QYG0Iwthulp0ocMx2M9KJ8nwBruUFnW8AMnb6yH97dSfR6O1vdfej/D7l\nLYlNhvY/AgMBAAECggEAU8lDMfLC1AdRcNB/n9WsQDpzJEFV8gxp75gHing64Vj9\n6FIjqV/UQyHT0ahlDI4YO1OXzUouaeX/sFXzhkmlJscn1gfZW8/GYH3NE1HvBh8t\n9J9V+/3xk9T1dCOypFt/hluq9Rt8n/wiF/E1gQXcOm4hKFWl8tHNuE0giEBRszjf\nYao/U1iwXioNBcHPkzesik9enqh6t4SsbeAAqZTcP81YZlVuV4VnW6j5FyDeSCsc\n+J7/Z5CEGxqVJqeKrqhg5ptNeAevM1HNJ/RvUvBC3OYJ0JmDeauCMWXlWY9nc8zW\ntGmKs6pr37fNSOsFkeLKI7Qov3evCMMZ5XBTMHGkkQKBgQDicI5l21Zas6YTs0Kf\nZpvGUSnTgkb0yy0A+MAPrx5XwhFmluBEHjrA/Yb3NFRFjb9/B4HH4Hg/STt7aPcY\nBUIkVoLWlQOs6fyeYR3ltsID3mL/deaHf4YPgGFikIrPBiSjkCLUA+eOPvg3d4k+\nIViyK5mMhxJPXi3gHT+6m7uOeQKBgQDKeD+52y4v0DdXGm+wNtsp0DVzP6jSeNb7\nGAd1btUJhIXHqWV3f6j24sb0LvIkZz+r4frxFxL4Vgh6f/DwJ9x2MVTNTre7UvJJ\n25VO+LthbQKoOQCAbo9F2koNqopWig4qMKukjhQ6yxDX8w8s8EWFhIaqD0kPdXRx\nKWoQ2TacdwKBgQChjVY621rnyUYSxhEhMo6u1dc2fLrtCUvpZo94YSMPz3ikrb4B\nO2QFrputINuC6BeYpJ12IfMIi9HxQTkRHSdMT6B3QcdmhWXjBTzUWChhpDcTNWWs\nhFH8G0bfkGpIO4TGYR5IDyUUOl7TC+iRuC7UpwCc3v00POgT/ioqk9MjWQKBgEiH\nnSSCLOB58Wklkj8I16f56zvW4S5MlY6rg/iAdJaNP7NProaJV8jhYi4VJy79QaTc\nNh3piyUlBLKFZJVTYjmA4IUPnuffBeaJX8pDdjSnbV0/1jsr3+1BDmgo4JexqvNY\nLhSrxPluxyDk9Fm/1NfIqsj+4shD5iunj1Rry5FvAoGBAKOeGGCSwCiSlHt+wh+B\nqEfMLciTqg+rdoCpdcTn8a09DHcLNgT7sodlvOAWE4HLALNUxO0rw0UDzyWiMFeF\nnimt4lbrxDsz0Tcd1GHUjtwIOKWHk5U9VdfY3t8JhXcmWTqQZpd1j1tRHhlCV7Al\nwJ0mIIjyX/dpHfPoxNYxy067\n-----END PRIVATE KEY-----\n",
  "client_email": "469268263526-compute@developer.gserviceaccount.com",
  "client_id": "104721145917169206897",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/469268263526-compute%40developer.gserviceaccount.com",
  "universe_domain": "googleapis.com"
}

try:

  """Uploads a file to the bucket."""
  credentials = service_account.Credentials.from_service_account_info(credentials_dict)
  storage_client = storage.Client(credentials=credentials)
  bucket = storage_client.get_bucket('artists_name') ### Nome do seu bucket
  blob = bucket.blob('artist-names.csv')

  pages = []
  names = "Name \n"

  for i in range(1, 5):
    url = 'https://web.archive.org/web/20121007172955/https://www.nga.gov/collection/anZ' + str(i) + '.htm'
    pages.append(url)

  for item in pages:
    page = requests.get(item)
    soup = BeautifulSoup(page.text, 'html.parser')

    last_links = soup.find(class_='AlphaNav')
    last_links.decompose()

    artist_name_list = soup.find(class_='BodyText')
    artist_name_list_items = artist_name_list.find_all('a')

    for artist_name in artist_name_list_items:
      names = names + artist_name.contents[0] + "\n"

    blob.upload_from_string(names, content_type="text/csv")

except Exception as ex:
  print(ex) 
