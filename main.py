
# Import Libraries
import requests
import time
import smtplib
import androidhelper

# Define Constants
PINCODE = "<ENTER YOUR PINCODE>"  # Example 600040
MY_EMAIL = "<ENTER YOUR EMAIL ID>"  # From this mail id, the alerts will be sent
MY_PASSWORD = "<ENTER YOUR PASSWORD>"  # Enter the email id's password
# For multiple recipients,put a comma and add email
TO_EMAIL = ["<ENTER EMAIL OF THE RECIPIENT>"]


def alertDiag(message):
    title = 'Vaccines are available !'
    droid.dialogCreateAlert(title, message)
    droid.dialogSetPositiveButtonText('Continue')
    droid.dialogShow()
    response = droid.dialogGetResponse().result
    return response['which'] == 'positive'


requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS = "TLS13-CHACHA20-POLY1305-SHA256:TLS13-AES-128-GCM-SHA256:TLS13-AES-256-GCM-SHA384:ECDHE:!COMPLEMENTOFDEFAULT"

# Derive the date and url
# url source is Cowin API - https://apisetu.gov.in/public/api/cowin
today = time.strftime("%d/%m/%Y")
url = f"https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin?pincode={PINCODE}&date={today}"

# Write a loop which checks for every 60 seconds
print("Script is up and running. Don't close this terminal")
while True:
    # Start a session
    with requests.session() as session:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'}
        response = session.get(url, headers=headers)

        # Receive the response
        response = response.json()
        # print(response)
        for center in response['centers']:
            for session in center['sessions']:

                # For Age not equal to 45 and capacity is above zero
                if (session['min_age_limit'] != 45) & (session['available_capacity'] > 0):
                    message_string = f"Subject: {today}'s Alert'!! \n\n Available - {session['available_capacity']} in {center['name']} on {session['date']} for the age {session['min_age_limit']}"

                    # Configure GMAIL settings
                    with smtplib.SMTP("smtp.gmail.com") as connection:
                        connection.starttls()
                        connection.login(MY_EMAIL, MY_PASSWORD)
                        connection.sendmail(
                            from_addr=MY_EMAIL,

                            to_addrs=TO_EMAIL,
                            msg=message_string
                        )

                    # Alerting locally on the phone
                    droid = androidhelper.Android()
                    droid.setMediaVolume(100)
                    droid.vibrate(5000)  # 5 sec = 5000 millisec
                    for i in range(5):
                        droid.ttsSpeak(
                            "ALERT ! ALERT ! Vaccines are available")
                    alertDiag(message_string)
                    break

        time.sleep(60)
