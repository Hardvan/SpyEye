import mimetypes
import requests
import json


def UploadImage(path, timestamp):
    target = path
    mime_type = mimetypes.guess_type(target)[0]

    files = {
        "file": (target, open(target, "rb"), mime_type)
    }

    headers = {
        "Authorization": f"Bearer EABU7YlckmlkBALYtNCopBISMpNA51nZAGjxfzJmZAQ36BZCtDZChVhvgdAZAbf01e9sUqXiCK35XbbVg56DA7F4XmVx1CZBIlp2rYZCOj2rzJRnr4UCipZBO9u0wNHiZBi1QdYgtVqwY9UZBUbLffy0DnXQqAphCQSEbG0a6Jd5CDSEWA7plksDIkib2MLnthtyn4HKwvyACPhR2ndsMqq4QiZA"
    }

    params = {
        "messaging_product": "whatsapp",
        "type": mime_type
    }

    response = requests.post(
        f"https://graph.facebook.com/v13.0/113814568315440/media",
        headers=headers,
        params=params,
        files=files
    )

    result_whatsapp_media = response.json()
    http_code = response.status_code

    MEDIA_OBJECT_ID = result_whatsapp_media["id"]
    print(MEDIA_OBJECT_ID)
    SendMessage(MEDIA_OBJECT_ID, timestamp)


def SendMessage(object_id, timestamp):
    url = 'https://graph.facebook.com/v15.0/113814568315440/messages'
    headers = {
        'Authorization': 'Bearer EABU7YlckmlkBAE2S1RepUkns2E3Y64GPk2wOoOZAvom9SjBItNdfOQiBRmBW5tndWlKGdawX4zrPqP4PPclQicKQYwoVV92ZCZANrLErFGZCiDZAX5UYxxDOQJyfV0FaFNUK8bc20xAkdARWDMANyTVB09ZByaoPvZCIbP7UotIXyhWJJMYS35zYa5ZAmq41PSctZAS7GSCZC09exjIwcpNJvB',
        'Content-Type': 'application/json'
    }

    hardik = "9845072575"
    karan = "7348911401"

    data = {
        "messaging_product": "whatsapp",
        "preview_url": False,
        "recipient_type": "individual",
        "to": f"91{hardik}",  # Start with 91 for Indian numbers
        "type": "image",
        "image": {
            "id": object_id,
            "caption": timestamp
        }

        # For first time:
        # "type": "template",
        # "template": {
        #     "name": "hello_world",
        #     "language": {
        #         "code": "en_US" }

    }

    response = requests.post(url, headers=headers, data=json.dumps(data))

    print(response.content)
