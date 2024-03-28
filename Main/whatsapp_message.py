import mimetypes
import requests
import json

# ! Refreshes every 24 hours
bearer_token = "EABU7YlckmlkBO6kaOe9QqjGoHyL5lfpUNlRk0Yf2pQWvldnS22oMjEmss9yKolDsXBcHDKYZAgGpmLE6nQ8ma4XauuKIw5rxmnAUuSUxZAN1VE6mSzeZAuIvmfavTUjvhpssYzC2iXYsIbLEvGTRHXd90IYucVYmenc81fSdGDk2HcAJOL2lWtIrvO23D5XF80kJ4mOAB5MG940tCMN2KlsxNcZD"

# ! Set to True if you want to refresh the token
refreshed = False


def UploadImage(path, timestamp):
    target = path
    mime_type = mimetypes.guess_type(target)[0]

    files = {
        "file": (target, open(target, "rb"), mime_type)
    }

    headers = {
        "Authorization": f"Bearer {bearer_token}"
    }

    params = {
        "messaging_product": "whatsapp",
        "type": mime_type
    }

    response = requests.post(
        "https://graph.facebook.com/v13.0/113814568315440/media",
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
        'Authorization': f'Bearer {bearer_token}',
        'Content-Type': 'application/json'
    }

    hardik = "9845072575"
    karan = "7348911401"
    abhishek = "6360848034"

    data = {
        "messaging_product": "whatsapp",
        "preview_url": False,
        "recipient_type": "individual",
        "to": f"91{karan}",  # Start with 91 for Indian numbers
    }
    if refreshed:  # If token is refreshed, send a template message
        data["type"] = "template"
        data["template"] = {
            "name": "hello_world",
            "language": {
                "code": "en_US"}
        }
    else:
        data["type"] = "image"
        data["image"] = {
            "id": object_id,
            "caption": f"Face detected {timestamp}"
        }

    response = requests.post(url, headers=headers, data=json.dumps(data))

    print(response.content)