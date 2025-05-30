import asyncio
import os
from dotenv import load_dotenv
from password_api import PasswordAPI
from url_api import UrlAPI

load_dotenv()

async def run_services(pwd_service, url_service):
    try:
        passwords = await asyncio.gather(
            pwd_service.make_password(8),
            pwd_service.make_password(12),
            pwd_service.make_password(16)
        )
        
        print("\nРандомные пароли:")
        for pwd in passwords:
            print(f"→ {pwd['random_password']} (длина: {len(pwd['random_password'])})")
        
        urls = await asyncio.gather(
            url_service.inspect_url("https://google.com"),
            url_service.inspect_url("https://ya.ru"),
            url_service.inspect_url("https://github.com"),      
            url_service.inspect_url("https://stackoverflow.com"),
            url_service.inspect_url("https://wikipedia.org"),
            url_service.inspect_url("https://youtube.com")
        )
        
        print("\nДетальная информация о сайтах:")
        for site in urls:
            print(f"\nURL: {site['url']}")
            print(f"  Страна: {site.get('country', 'неизвестна')}")
            print(f"  Регион: {site.get('region', 'неизвестен')}")
            print(f"  Город: {site.get('city', 'неизвестен')}")
            print(f"  Провайдер: {site.get('isp', 'неизвестен')}")
    
    except Exception as e:
        print(f"\nОшибка: {str(e)}")

async def main_loop():
    API_KEY = os.getenv('API_KEY')
    if not API_KEY:
        raise ValueError("API_KEY не найден в .env файле")
    
    pwd_service = PasswordAPI(API_KEY)
    url_service = UrlAPI(API_KEY)
    
    print("Нажмите Enter для остановки")
    
    while True:
        task = asyncio.create_task(run_services(pwd_service, url_service))
        
        done, pending = await asyncio.wait(
            {task, asyncio.get_event_loop().run_in_executor(None, input)},
            return_when=asyncio.FIRST_COMPLETED
        )
        
        if any(t for t in done if not t == task):
            print("\nЗавершение работы...")
            if not task.done():
                task.cancel()
            break
            
        await task
        print("\nПовторение запросов...")
        await asyncio.sleep(2)

if __name__ == "__main__":
    try:
        asyncio.run(main_loop())
    except KeyboardInterrupt:
        print("\nПрограмма завершена")