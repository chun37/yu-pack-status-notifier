from desktop_notifier import DesktopNotifier
import requests
from bs4 import BeautifulSoup
from more_itertools import chunked, flatten
from dataclasses import dataclass
import asyncio


@dataclass(frozen=True)
class Status:
    datetime: str
    status: str
    details: str
    office: str
    zip_code: str
    prefecture: str


class YuPack:
    def __init__(self, tracking_number: str, notifier: DesktopNotifier):
        self.tracking_number = tracking_number
        self.notifier = notifier
        self.latest = None

    def get_latest_status(self) -> Status:
        url = f"https://trackings.post.japanpost.jp/services/srv/search/direct?reqCodeNo1={self.tracking_number}&locale=ja"
        response = requests.get(url)
        parsed = BeautifulSoup(response.text, 'html.parser')
        history_table = parsed.find("table", attrs={"summary": "履歴情報"})
        history_table_rows = chunked(history_table.find_all("tr"), 2)
        body_rows = list(history_table_rows)[1:]
        latest = body_rows[-1]
        td_list = [td for td in flatten(latest) if td.name == "td"]
        status = Status(
            datetime=td_list[0].text,
            status=td_list[1].text,
            details=td_list[2].text,
            office=td_list[3].text,
            zip_code=td_list[4].text,
            prefecture=td_list[5].text
        )
        return status

    async def watch(self):
        while True:
            latest = self.get_latest_status()
            if latest != self.latest:
                await self.notifier.send(
                    title="配達状況更新通知",
                    message="お届け予定の荷物の配達状況が更新されました。",
                )
                self.latest = latest
            await asyncio.sleep(60)
