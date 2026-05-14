import secrets
from fastapi import HTTPException, Depends, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

# In production, store these in a hashed/secured database
ALLOWED_SENSORS = {
    "sensor_id_1": "secret_key_a",
    "sensor_id_2": "secret_key_b"
}

security = HTTPBearer()

def verify_sensor_api_key(credentials: HTTPAuthorizationCredentials = Depends(security)):
    api_key = credentials.credentials

    #Simplified validation: Check if API key matches a known sensor
    if api_key not in ALLOWED_SENSORS.values():
        raise HTTPException(status_code = 401, detail = "Invalid API Key or Trusted Sensor")
    return api_key


