class LoginRequest:
    def __init__(self, email: str, password: str):
        self.email = email
        self.password = password

class GenerateOTPReqeuest:
    email: str

class VerifyOTPRequest(GenerateOTPReqeuest):
    otp: int

class RegisterRequest:
    email: str
    password: str
    roll: str
    name: str
    batch: str
    profileImage: str
    idImage: str

class ForgotPasswordRequest:
    email: str
    newPassword: str
    otp: str

class FaceVerificationRequest:
    image: str