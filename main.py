from yu_pack import YuPack
import asyncio
import signal
from desktop_notifier import DesktopNotifier


async def init() -> None:
    stop_event = asyncio.Event()
    loop = asyncio.get_running_loop()

    loop.add_signal_handler(signal.SIGINT, stop_event.set)
    loop.add_signal_handler(signal.SIGTERM, stop_event.set)

    await stop_event.wait()

if __name__ == "__main__":
    yu_pack = YuPack("1234-1234-1234", DesktopNotifier(app_name="ゆうパック", notification_limit=10))
    asyncio.run(yu_pack.watch())
