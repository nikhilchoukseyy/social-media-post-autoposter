import os 
import requests
from dotenv import load_dotenv
from flask import Flask, request

load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI")

app = Flask(__name__)

@app.route("/")
def login(): 
  
  auth_url = (
    "https://www.linkedin.com/oauth/v2/authorization?"
    "response_type=code"
    f"&client_id={CLIENT_ID}"
    f"&redirect_uri={REDIRECT_URI}"
    "&scope=openid%20profile%20w_member_social"
  )
  
  return f'<a href="{auth_url}">Click here to login with Linkedin</a>'

@app.route("/callback")
def callback(): 
  code = request.args.get("code")
  response = requests.post(
    "https://www.linkedin.com/oauth/v2/accessToken",
    data={
      "grant_type":"authorization_code", 
      "code":code,
      "client_id":CLIENT_ID,
      "client_secret":CLIENT_SECRET,
      "redirect_uri": REDIRECT_URI,
    }
  )

  token_data = response.json()
  access_token = token_data.get("access_token")

  with open("token.txt","w") as f : 
    f.write(access_token)

  return "Token saved successfully"

if __name__ == "__main__": 
  app.run(port=8000)