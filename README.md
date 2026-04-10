# Twilio Repair Hotline Prototype

A Flask app that handles incoming phone calls via Twilio, collects customer input through an IVR menu, dispatches SMS alerts to a maintenance worker, and logs incidents to a SQLite database.

## How It Works

1. Customer calls your Twilio number
2. IVR menu plays: press 1 for emergency, press 2 for non-urgent
3. SMS sent to the worker with the caller's number and urgency level
4. Incident logged to SQLite with timestamp, category, and status
5. Dashboard at `/incidents` shows all logged incidents

## Setup

```bash
pip install flask twilio dotenv
```

Create a `.env` file with the following:

```
TWILIO_ACCOUNT_SID=your_sid
TWILIO_AUTH_TOKEN=your_token
TWILIO_PHONE_NUMBER=+1...    # Your Twilio number
WORKER_PHONE_NUMBER=+1...    # Technician's phone
```

## Run

```bash
python app.py
```

The server starts on `http://localhost:5000`.

## Expose to Twilio

Use ngrok to expose your local server:

```bash
ngrok http 5000
```

Copy the `https://` forwarding URL from the ngrok output, then configure the Twilio webhook:

1. Go to [console.twilio.com](https://console.twilio.com/us1/develop/phone-numbers/manage/incoming/)
2. Click your number
3. Under Voice Configuration, paste your URL:
   ```
   https://<your-ngrok-url>/incoming-call
   ```
4. Set the method to HTTP POST
5. Click Save

> Note: The free ngrok plan generates a new URL each time you restart it. You'll need to update the Twilio webhook each time. To avoid this, claim a free static domain in the ngrok dashboard and run:
> ```bash
> ngrok http --domain=yourname.ngrok-free.app 5000
> ```

## Routes

| Method | Path              | Description                        |
|--------|-------------------|------------------------------------|
| POST   | `/incoming-call`  | Twilio voice webhook (returns TwiML) |
| POST   | `/handle-input`   | Processes keypress, sends SMS, logs incident |
| GET    | `/incidents`      | HTML dashboard of all incidents    |
