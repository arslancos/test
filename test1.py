import requests
import json

host = "http://192.168.50.1"
# 1. API Login
login_url = host+"/api/login"
login_data = {
    "username": "admin",
    "password": "Vitel12345"
}
headers = {"Content-Type": "application/json"}

print("1. Giriş yapılıyor...")
login_response = requests.post(login_url, headers=headers, json=login_data)
if login_response.status_code == 200:
    print("Giriş başarılı!")
else:
    print(f"Giriş başarısız! Hata: {login_response.status_code} - {login_response.text}")
    exit()

# Çerezleri sakla
cookies = login_response.cookies

# 2. Client2 oluştur
client_url = host+"/api/auth.client"
client_data = {
    "action": "add",
    "name": "Client2",
    "scope": "api"
}

print("\n2. Client2 oluşturuluyor...")
client_response = requests.post(client_url, headers=headers, json=client_data, cookies=cookies)
if client_response.status_code == 200:
    client_json = client_response.json()
    print("Client2 başarıyla oluşturuldu!")
    print("Yanıt:", json.dumps(client_json, indent=4))
else:
    print(f"Client2 oluşturma başarısız! Hata: {client_response.status_code} - {client_response.text}")
    exit()

# clientId ve clientSecret değerlerini al
client_id = client_json["response"]["clientId"]
client_secret = client_json["response"]["clientSecret"]

if not client_id or not client_secret:
    print("clientId veya clientSecret alınamadı!")
    exit()

# 3. AccessToken oluştur
token_url = host+"/api/auth.token.grant"
token_data = {
    "clientId": client_id,
    "clientSecret": client_secret,
    "scope": "api"
}

print("\n3. AccessToken alınıyor...")
token_response = requests.post(token_url, headers=headers, json=token_data, cookies=cookies)
if token_response.status_code == 200:
    token_json = token_response.json()
    print("AccessToken başarıyla alındı!")
    print("Yanıt:", json.dumps(token_json, indent=4))
else:
    print(f"AccessToken alma başarısız! Hata: {token_response.status_code} - {token_response.text}")
    exit()

# AccessToken'i yazdır
access_token = token_json["response"]["accessToken"]
if access_token:
    print("\nAlınan AccessToken:", access_token)
else:
    print("AccessToken alınamadı!")



# 5. GPIO analog giriş durumu
gpio_status_url = host+"/api/status.gpio.input"
params = {"infoType": "analog"}

print("\n5. GPIO analog giriş durumu sorgulanıyor...")
gpio_status_response = requests.get(gpio_status_url, headers=headers, params=params, cookies=cookies)
if gpio_status_response.status_code == 200:
    gpio_status_json = gpio_status_response.json()
    print("GPIO analog giriş durumu başarıyla alındı!")
    print("Yanıt:", json.dumps(gpio_status_json, indent=4))
