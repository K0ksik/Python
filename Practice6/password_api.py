from api_client import ApiClient

class PasswordAPI(ApiClient):
    BASE_URL = "https://api.api-ninjas.com/v1/passwordgenerator"
    
    async def make_password(self, length: int = 16) -> dict:
        return await self.send_query(self.BASE_URL, {'length': length})