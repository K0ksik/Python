from api_client import ApiClient

class UrlAPI(ApiClient):
    BASE_URL = "https://api.api-ninjas.com/v1/urllookup"
    
    async def inspect_url(self, url: str) -> dict:
        return await self.send_query(self.BASE_URL, {'url': url})