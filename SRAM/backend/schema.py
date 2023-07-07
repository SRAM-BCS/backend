class LoginRequest:
    email: str
    password: str

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