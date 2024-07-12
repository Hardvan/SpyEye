import mimetypes
import requests
import json

# ! Refreshes every 24 hours
bearer_token = "EABU7YlckmlkBOZBBgdw0CdhN11FE8yysjPAXZCGTFrYqq3HgjTzAglAs6CotyT4kIAZCpan99vOn66KLti6d0N6zZAveBWCcjC4oD9CZBxryCDdfIOOiDiBoJx56fg75oJCpAb1hNeRFvndmZCNMfGOXCwOfK4oQYRBb4VZCZA5YNHoSYJnMJjpOYD6pB2NiOgitTol2tCrZA5CRxV3ABRWtto6ZAdZAWEZD"

# ! Set to True if you have refreshed the token
refreshed = False


def UploadImage(target, timestamp):
    """Uploads the image to Facebook and returns the media object ID.

    Args
    ----
    - target: Path to the image file
    - timestamp: Timestamp of the image capture

    Calls
    -------
    - SendMessage: Sends the message to the WhatsApp number
    """

    # Get the MIME type of the image
    mime_type = mimetypes.guess_type(target)[0]

    # Prepare the image file to be uploaded
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
    print(f"MEDIA_OBJECT_ID: {MEDIA_OBJECT_ID}")
    SendMessage(MEDIA_OBJECT_ID, timestamp)


def SendMessage(object_id, timestamp):
    """Sends the message to the WhatsApp number.

    Args
    ----
    - object_id: Media object ID of the image
    - timestamp: Timestamp of the image capture
    """

    url = 'https://graph.facebook.com/v15.0/113814568315440/messages'
    headers = {
        'Authorization': f'Bearer {bearer_token}',
        'Content-Type': 'application/json'
    }

    hardik = "9845072575"
    karan = "7348911401"
    abhishek = "6360848034"
    harshit = "8058076999"

    number_name_map = {
        "9845072575": "Hardik",
        "7348911401": "Karan",
        "6360848034": "Abhishek",
        "8058076999": "Harshit"
    }

    # List of recipients
    phone_list = [hardik, karan]
    for phone_number in phone_list:

        send_to = f"91{phone_number}"  # Start with 91 for Indian numbers

        # Prepare the data to be sent
        data = {
            "messaging_product": "whatsapp",
            "preview_url": False,
            "recipient_type": "individual",
            "to": send_to,
        }
        if refreshed:  # If token is refreshed, send a template message
            data["type"] = "template"
            data["template"] = {
                "name": "hello_world",
                "language": {
                    "code": "en_US"}
            }
        # If token is not refreshed, send an image message (normal message)
        else:
            data["type"] = "image"
            data["image"] = {
                "id": object_id,
                "caption": f"Face detected {timestamp}. Please check the image."
            }

        person_name = number_name_map[phone_number]
        print(f"Sending WhatsApp message to: {send_to} ({person_name})...")
        response = requests.post(url, headers=headers, data=json.dumps(data))
        print(f"Response content: {response.content}")
        print(f"✅ WhatsApp message sent to: {send_to} ({person_name})\n")
