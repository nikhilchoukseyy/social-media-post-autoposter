import requests 
import json 

with open("token.txt","r") as f : 
  access_token = f.read().strip()

headers = {
  "Authorization": f"Bearer {access_token}", 
  "Content-Type" : "application/json",
  "X-Restli-Protocol-Version": "2.0.0"
}

def get_user_id():
  response = requests.get(
    "https://api.linkedin.com/v2/userinfo",
    headers=headers
  )
  return response.json().get("sub")


def register_image_upload(user_id): 
  register_data = {
    "registerUploadRequest": {
      "owner": f"urn:li:person:{user_id}",
      "recipes": ["urn:li:digitalmediaRecipe:feedshare-image"],
      "serviceRelationships": [
        {
          "identifier": "urn:li:userGeneratedContent",
          "relationshipType": "OWNER"
        }
      ]
    }
  }

  response = requests.post(
    "https://api.linkedin.com/v2/assets?action=registerUpload",
    headers=headers, 
    json = register_data
  )

  data = response.json()

  upload_url = data["value"]["uploadMechanism"]["com.linkedin.digitalmedia.uploading.MediaUploadHttpRequest"]["uploadUrl"]
  asset_id = data["value"]["asset"]

  return upload_url,asset_id


def upload_image(upload_url,image_path): 
  with open(image_path,"rb") as image_file :
    image_data = image_file.read()

    upload_headers = {
      "Authorization": f"Bearer {access_token}", 
      "Content-Type": "application/octet-stream"
    }


    response = requests.put(
      upload_url,
      headers=upload_headers,
      data = image_data
    )

    print(f"Uplaod status : {response.status_code}")
    return response.status_code == 201


def create_post(user_id , asset_id , caption): 
  post_data = {
    "author": f"urn:li:person:{user_id}",
    "lifecycleState": "PUBLISHED",
    "specificContent": {
      "com.linkedin.ugc.ShareContent": {
        "shareCommentary": {
          "text": caption
        },
        "shareMediaCategory": "IMAGE",
        "media": [
          {
            "status": "READY",
            "media": asset_id
          }
        ]
      }
    },
    "visibility": {
      "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
    }
  }

  response = requests.post(
      "https://api.linkedin.com/v2/ugcPosts",
      headers=headers,
      json=post_data
  )

  print("Post status:", response.status_code)
  print("Response:", response.json())
  return response.status_code == 201


def post_to_linkedin(caption,image_path): 
  print("Getting user ID...")
  user_id = get_user_id()
  print("User ID:", user_id)
  
  print("Registering image upload...")
  upload_url, asset_id = register_image_upload(user_id)
  print("Asset ID:", asset_id)

  print("Uploading image...")
  upload_image(upload_url,image_path)

  print("Creating post...")
  create_post(user_id,asset_id,caption)
