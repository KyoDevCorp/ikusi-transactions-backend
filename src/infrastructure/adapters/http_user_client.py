import httpx
from domain.services.user_service import UserServiceClient
from typing import Dict

class UserServiceHTTPClient(UserServiceClient):
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip("/")
        self.client = httpx.Client(timeout=10.0)

    def get_user_by_token(self, token: str) -> Dict:
        try:
            response = self.client.get(
                f"{self.base_url}/validate-token",
                params={"token": token}
            )

            if response.status_code == 200:
                return response.json()
            else:
                raise ValueError(f"Token validation failed: {response.text}")

        except Exception as e:
            raise ValueError(f"Error calling usuarios-service: {str(e)}")