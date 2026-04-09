import os
from flask import Flask, request, render_template
from twilio.twiml.voice_response import VoiceResponse, Gather
from twilio.rest import Client
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

account_sid = os.getenv("TWILIO_ACCOUNT_SID")
auth_token = os.getenv("TWILIO_AUTH_TOKEN")
twilio_number = os.getenv("TWILIO_PHONE_NUMBER")
worker_number = os.getenv("WORKER_PHONE_NUMBER")

twilio_client = Client(account_sid, auth_token)


@app.route("/incoming-call", methods=["POST"])
def incoming_call():
    # Webhook Twilio hits when a call comes in, returns TwiML with IVR menu
    response = VoiceResponse()
    gather = Gather(num_digits=1, action="/handle-input", method="POST")
    gather.say(
        "Hello, you've reached the maintenance hotline. "
        "Press 1 for an emergency. "
        "Press 2 for a non-urgent request."
    )
    response.append(gather)
    response.say("We didn't receive any input. Goodbye.")
    return str(response), 200, {"Content-Type": "text/xml"}


@app.route("/handle-input", methods=["POST"])
def handle_input():
    # Processes the keypress, fires an SMS to the worker, and logs the incident
    digit = request.form.get("Digits")
    caller = request.form.get("From", "Unknown")

    response = VoiceResponse()

    if digit == "1":
        category = "Emergency"
        message = f"New EMERGENCY reported by {caller}. Call tenant back ASAP."
        response.say("We've logged your emergency. A technician will contact you shortly.")
    elif digit == "2":
        category = "Non-Urgent"
        message = f"New non-urgent request from {caller}. Follow up when available."
        response.say("We've logged your request. Someone will follow up soon.")
    else:
        response.say("Invalid selection. Goodbye.")
        return str(response), 200, {"Content-Type": "text/xml"}

    # Send SMS to the worker
    twilio_client.messages.create(
        body = message,
        from_ = twilio_number,
        to = worker_number,
    )

    return str(response), 200, {"Content-Type": "text/xml"}


if __name__ == "__main__":
    app.run(debug=True, port=5000)
