import base64
import requests


class Bolt:
    def __init__(self, phone=None, uuid=None, server_url=""):
        """Initializes a Bolt class.
        
        :param phone: Optional, can be set later: the phone number your account is linked to. (International format)
        :param uuid: Optional, can be set later: a randomly generated UUID. Must stay the same for every call over your account.
        """
        self.base_url = "https://node.bolt.eu"
        self.search_url = "https://rental-search.bolt.eu"
        self.server_url = server_url

        self.latitude = 0
        self.longitude = 0

        self.uuid = uuid
        self.phone = phone

        self.headers = {
            "user-agent": "okhttp/4.9.1"
        }


    def _check(self):
        if not self.phone and not self.uuid:
            raise Exception("You need to authenticate first")

        if not self.phone:
            raise Exception("No phone number linked")

        if not self.uuid:
            raise Exception("No uuid linked")


    def _auth_headers(self):
        self._check()

        auth_token = base64.b64encode(f"{self.phone}:{self.uuid}".encode("utf-8")).decode("utf-8")

        headers = {
            "user-agent": "okhttp/4.9.1",
            "Authorization": f"Basic {auth_token}"
        }

        return headers


    def login(self, phone: str, uuid: str) -> bool:
        """Set phone and uuid.
        
        :param phone: The phone number your account is linked to. (International format)
        :param uuid: A randomly generated UUID. Must stay the same for every call over your account.

        :return: ``True``, won't get validated.
        """

        self.uuid = uuid
        self.phone = phone

        return True


    def set_location(self, latitude: int, longitude: int) -> bool:
        """Set latitude and longitude.
        
        :param latitude: Latitude of the location you want to set.
        :param longitude: Longitude of the location you want to set.

        :return: ``True``, won't get validated.
        """
        self.latitude = latitude
        self.longitude = longitude

        return True


    def get_number_international_format(self):
        """Get phone number in international format.

        Phone number and UUID must be set via .login() or during intializing.

        :return: dict with phone number in international format and status code.
        """
        self._check()

        params = {
            "phone": self.phone,
            "version": "CA.47.1",
            "deviceId": self.uuid,
            "device_name": "GenymobileGoogle Pixel 3",
            "device_os_version": 10,
            "deviceType": "android",
            "language": "en"
        }

        r = requests.get(f"{self.base_url}/user/user/getMobileNumberInInternationalFormat", params=params, headers=self.headers)
        
        return r.json()


    def request_sms(self):
        """Sends an SMS with a code to your phone.
        
        Phone number and UUID must be set via .login() or during intializing.

        :return: dict with status code.
        """
        self._check()

        params = {
            "preferred_verification_method": "sms",
            "device_name": "GenymobileGoogle Pixel 3",
            "device_os_version": 10,
            "deviceType": "android",
            "language": "en",
            "version": "CA.47.1",
            "deviceId": self.uuid
        }

        data = {
            "phone": self.phone,
            "phone_uuid": self.uuid
        }

        r = requests.post(f"{self.base_url}/user/user/register/phone", data=data, params=params, headers=self.headers)

        return r.json()


    def submit_sms_code(self, code: str):
        """Submit the sms code, request one with request_sms().
        
        Phone number and UUID must be set via .login() or during intializing.

        :param code: The code you received via SMS.
        """
        self._check()

        params = {
            "preferred_verification_method": "sms",
            "device_name": "GenymobileGoogle Pixel 3",
            "device_os_version": 10,
            "deviceType": "android",
            "language": "en",
            "version": "CA.47.1",
            "deviceId": self.uuid
        }

        json = {
            "phone": self.phone,
            "phone_uuid": self.uuid,
            "verification": {
                "confirmation_data": {
                    "code": code
                },
                "method": "sms"
            }
        }

        r = requests.post(f"{self.base_url}/user/user/v1/confirmVerification", json=json, params=params, headers=self.headers)


        return r.json()



    def get_scooters(self, latitude, longitude):
        """Get all scooters in area.
        
        Phone number and UUID must be set via .login() or during intializing.
        """
        self._check()

        params = {
            "version": "CA.47.1",
            "deviceId": self.uuid,
            "deviceType": "android",
            "device_name": "GenymobileGoogle Pixel 3",
            "device_os_version": 10,
            "language": "en",
            "lat": latitude,
            "lng": longitude,
        }


        r = requests.get(f"{self.search_url}/categoriesOverview", params=params, headers=self._auth_headers())

        result = r.json()

        if result["code"] == 0:
            self.server_url = result["data"]["server_url"]

        return result


    def get_scooter(self, code):
        """Get scooter information by code, includes vehicle_id.
        
        Phone number and UUID must be set via .login() or during intializing.
        """
        self._check()
        
        if not self.server_url:
            raise Exception("You need to get scooters first or set server_url manually")

        params = {
            "vehicle_uuid": code,
            "version": "CA.47.1",
            "deviceId": self.uuid,
            "gps_lat": self.latitude,
            "gps_lng": self.longitude,
        }


        r = requests.get(f"{self.server_url}/client/getVehicleDetails", params=params, headers=self._auth_headers())

        return r.json()




    def get_scooter_info(self, code, type="uuid"):
        """Get detailed scooter information, including batery percentage.
        
        Phone number and UUID must be set via .login() or during intializing.
        """
        self._check()

        params = {
            "version": "CA.47.1",
            "deviceId": self.uuid,
            "gps_lat": self.latitude,
            "gps_lng": self.longitude,
            "deviceType": "android",
            "language": "en",
            "device_name": "GenymobileGoogle Pixel 3",
            "device_os_version": 10,
            "channel": "googleplay",
            "country": "de"
        }

        json = {
            "vehicle_handle": {
                "type": type,
                "value": code
            }
        }

        r = requests.post(f"{self.server_url}/micromobility/user/ui/vehicle/card", params=params, json=json, headers=self._auth_headers())

        return r.json()


    def ring_scooter(self, vehicle_id):
        """Ring scooter by vehicle_id.
        
        Phone number and UUID must be set via .login() or during intializing.
        """
        self._check()

        params = {
            "version": "CA.47.1",
            "deviceId": self.uuid,
            "gps_lat": self.latitude,
            "gps_lng": self.longitude,
            "deviceType": "android",
            "language": "en",
            "device_name": "GenymobileGoogle Pixel 3",
            "device_os_version": 10,
        }

        data = {
            "vehicle_id": vehicle_id,
        }

        r = requests.post(f"{self.server_url}/client/ringVehicle", data=data, params=params, headers=self._auth_headers())

        return r.json()

    
    def start_rent(self, code, payment_id):
        """Start rent by scooter code.
        
        Phone number and UUID must be set via .login() or during intializing.
        """
        self._check()

        params = {
            "version": "CA.47.1",
            "deviceId": self.uuid,
            "gps_lat": self.latitude,
            "gps_lng": self.longitude,
            "deviceType": "android",
            "language": "en",
            "device_name": "GenymobileGoogle Pixel 3",
            "device_os_version": 10,
            "channel": "googleplay",
            "country": "de"
        }

        json = {
            "vehicle": {
                "type": "uuid",
                "value": code
            },
            "payment_method_type": "adyen",
            "payment_method_id": payment_id
        }

        r = requests.post(f"{self.server_url}/client/v2/createAndStartOrder", json=json, params=params, headers=self._auth_headers())

        return r.json()


    def get_order(self, order_id):
        """Get order information by order_id.
        
        Phone number and UUID must be set via .login() or during intializing.
        """
        self._check()

        params = {
            "order_id": order_id,
            "version": "CA.47.1",
            "deviceId": self.uuid,
            "gps_lat": self.latitude,
            "gps_lng": self.longitude,
            "deviceType": "android",
            "language": "en",
            "device_name": "GenymobileGoogle Pixel 3",
            "device_os_version": 10,
            "channel": "googleplay",
            "country": "de"
        }

        r = requests.get(f"{self.server_url}/client/getActiveOrder", params=params, headers=self._auth_headers())

        return r.json()


    def check_location(self, action, vehicle_id):
        """Check if scooter is in a non-parking area.
        
        Phone number and UUID must be set via .login() or during intializing.
        """
        self._check()

        params = {
            "order_action": action,
            "vehicle_id": vehicle_id,
            "version": "CA.47.1",
            "deviceId": self.uuid,
            "gps_lat": self.latitude,
            "gps_lng": self.longitude,
            "deviceType": "android",
            "language": "en",
            "device_name": "GenymobileGoogle Pixel 3",
            "device_os_version": 10,
        }

        r = requests.get(f"{self.server_url}/client/checkLocation", params=params, headers=self._auth_headers())

        return r.json()

    
    def stop_rent(self, order_id):
        """Stop rent by order_id.
        
        Phone number and UUID must be set via .login() or during intializing.
        """
        self._check()
        
        params = {
            "version": "CA.47.1",
            "deviceId": self.uuid,
            "gps_lat": self.latitude,
            "gps_lng": self.longitude,
            "deviceType": "android",
            "language": "en",
            "device_name": "GenymobileGoogle Pixel 3",
            "device_os_version": 10,
            "channel": "googleplay",
            "country": "de"
        }

        json = {
            "order_id": order_id,
            "confirmed_view_keys": []
        }

        r = requests.post(f"{self.server_url}/micromobility/user/order/finish", json=json, params=params, headers=self._auth_headers())

        result = r.json()

        if result["code"] != 0:
            print("Note: Stopping rent may have failed.")

        json = {
            "order_id": order_id,
            "confirmed_view_keys": [
                "photo_capture_key"
            ]
        }

        r = requests.post(f"{self.server_url}/micromobility/user/order/finish", json=json, params=params, headers=self._auth_headers())

        return r.json()