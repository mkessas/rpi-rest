import web
import json
import RPi.GPIO as GPIO

buttons = {
    "up": 17,
    "down": 18
}


class static:

    def GET(self):
        web.redirect('/static/index.html')


class api:

    def GET(self, button, state):

            # Canonicalise input
            state = state.lower()
            button = button.lower()

            # Verify button exists
            if not button in buttons:
                web.ctx.status = "422 Unprocessable Entity"
                return json.dumps({"status":"err", "message": "Button must be 'up' or 'down'"})

            # Validate requested state
            if state != "on" and state != "off":
                web.ctx.status = "422 Unprocessable Entity"
                return json.dumps({"status":"err", "message": "State must be 'on' or 'off'"})

            # Send "off" state to all buttons first
            for b in buttons:
                if b != button: GPIO.output(buttons[b], GPIO.LOW)

            # Send requested signal to our button
            GPIO.output(buttons[button], GPIO.LOW if state == "off" else GPIO.HIGH)
            return json.dumps({"status": "ok", "details": "Button state set"}, indent=4)


GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

for button in buttons:
    GPIO.setup(int(buttons[button]),GPIO.OUT)
    GPIO.output(int(buttons[button]),GPIO.LOW)

urls = (
    '/', static,
    '/api/button/(.*)/(.*)',api 
)

try:
    if __name__ == "__main__":
        app = web.application(urls, globals())
        app.run()

except KeyboardInterrupt:
    print("CTRL+C Detected, Exiting")
