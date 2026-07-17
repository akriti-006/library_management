from auth import (
    create_access_token,
    verify_access_token,
)

token = create_access_token(
    {"sub": "1"}
)

print("Token:")
print(token)

print()

payload = verify_access_token(token)

print("Decoded Payload:")
print(payload)