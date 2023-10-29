import os
from twilio.rest import Client
from flask import Flask, render_template, request, redirect

app = Flask(__name__, template_folder='templets/')

# Set environment variables for your credentials
# Read more at http://twil.io/secure

account_sid = ""  # Twilio account SID
auth_token = ""  # Twilio auth token
verify_sid = ""  # SID of the Twilio verification service

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        user_number = request.form['number']
        verified_number = "+254" + user_number

        client = Client(account_sid, auth_token)  # Create a Twilio client object

        # Initiate the verification process by sending an OTP code via SMS
        verification = client.verify.v2.services(verify_sid) \
            .verifications \
            .create(to=verified_number, channel="sms")
        print(verification.status)  # Print the status of the verification process

        return render_template('otp.html')
    return render_template('index.html')


@app.route('/verify', methods=['POST'])
def verify():
    otp_code = request.form['otp']
    verified_number = "+254" + request.form['number']

    client = Client(account_sid, auth_token)  # Create a Twilio client object

    # Complete the verification process by checking the entered OTP code
    verification_check = client.verify.v2.services(verify_sid) \
        .verification_checks \
        .create(to=verified_number, code=otp_code)
    print(verification_check.status)  # Print the status of the verification check

    if verification_check.status == 'approved':
        return render_template('get.html')  # Redirect to the get.html page
    else:
        return "Verification status: " + verification_check.status


if __name__ == '__main__':
    app.run(port=8004)
