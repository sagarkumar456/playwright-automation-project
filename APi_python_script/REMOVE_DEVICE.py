import requests

BASE_URL = "https://web.onelap.in/api/utils/remove-device"

HEADERS = {
    "Authorization": "MTgwMDEwMzAyNzQ6YXNkcXNhZDEyIzEyMy4uMTIzMjIx",
    "Content-Type": "application/json"
}


IMEI_LIST = [
    "869689044681898"
]

COMMON_PARAMS = {
    "isDeleteInventory": "false",
    "updateDeviceCache": "false",
    "isRefershed": "true",
    "origin": "https://r.onelap.in",
    "key": "[[]]pooikloijm232456ytrfdsawq.;'.,;'.l"
}

for imei in IMEI_LIST:
    params = COMMON_PARAMS.copy()
    params["imei"] = imei   #IMPORTANT: Query IMEI change

    payload = [
        {
            "imei": imei,   #Body IMEI same as query
            "validity": "2022-05-02"
        }
    ]

    response = requests.delete(
        BASE_URL,
        headers=HEADERS,
        params=params,
        json=payload
    )

    if response.status_code == 200:
        print("Response:", response.text)
    else:
        print(f"Failed to remove device: {imei}")
        print("Status:", response.status_code)
        print("Response:", response.text)
