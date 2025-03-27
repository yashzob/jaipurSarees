class MessageHandler:
    def __init__(self, phone_number, otp):
        self.phone_number = phone_number
        self.otp = otp

    def send_otp_via_whatsapp(self):
        # Logic to send OTP via WhatsApp
        print(f"Sending OTP {self.otp} to {self.phone_number} via WhatsApp.")

    def send_otp_via_message(self):
        # Logic to send OTP via SMS
        print(f"Sending OTP {self.otp} to {self.phone_number} via SMS.")
