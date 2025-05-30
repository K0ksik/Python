import aiohttp

class ApiClient:
    def __init__(self, auth_token: str):
        self.auth_token = auth_token
        self.headers = {'X-Api-Key': auth_token}
    
    async def send_query(self, service_url: str, params: dict = None) -> dict:
        async with aiohttp.ClientSession() as session:
            async with session.get(service_url, headers=self.headers, params=params) as response:
                response.raise_for_status()
                return await response.json()