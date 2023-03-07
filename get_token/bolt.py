from uuid import uuid4

phone = input("Phone Number (e.g. +391235346): ")
uuid = str(uuid4())

headers = {"user-agent": "okhttp/4.9.1"}

params = {
    "phone": phone,
    "version": "CA.47.1",
    "deviceId": uuid,
    "device_name": "GenymobileGoogle Pixel 3",
    "device_os_version": 10,
    "deviceType": "android",
    "language": "en"
}

r = requests.get(f"{self.base_url}/user/user/getMobileNumberInInternationalFormat", params=params, headers=headers)
        
phone = r.json()["data"]["phone_number_in_international_format"]

params = {
    "preferred_verification_method": "sms",
    "device_name": "GenymobileGoogle Pixel 3",
    "device_os_version": 10,
    "deviceType": "android",
    "language": "en",
    "version": "CA.47.1",
    "deviceId": uuid
}

data = {
    "phone": phone,
    "phone_uuid": uuid
}

r = requests.post(f"{self.base_url}/user/user/register/phone", data=data, params=params, headers=headers)

print("Bolt sent you an SMS...")
code = str(int(input("Enter the 4-digit numeric code: ")))

params = {
    "preferred_verification_method": "sms",
    "device_name": "GenymobileGoogle Pixel 3",
    "device_os_version": 10,
    "deviceType": "android",
    "language": "en",
    "version": "CA.47.1",
    "deviceId": uuid
}

json = {
    "phone": phone,
    "phone_uuid": uuid,
    "verification": {
        "confirmation_data": {
            "code": code
         },
         "method": "sms"
     }
}

r = requests.post(f"{self.base_url}/user/user/v1/confirmVerification", json=json, params=params, headers=headers)


if r.json()["code"] == 0:
    print("UUID:", uuid)
    print("Phone Number:", phone)
    
else:
    print("Somethign went wrong.")
    print(r.json())
