import requests
import os
import dateutil.parser


TOKEN = os.getenv("TODOIST_TOKEN")


class Todoist:
    def __init__(self):

        self.items = []

    def get_todoist_items(self):
        """Todoistにアクセスし、未完了のitem一覧を取得する"""

        self.items = []

        r = requests.get(
            "https://api.todoist.com/sync/v8/sync",
            {"token": TOKEN, "sync_token": "*", "resource_types": '["items"]'},
        )

        for i in [x for x in r.json()["items"] if x["checked"] == 0]:
            due = i["due"]["date"] if i["due"] else None
            self.items.append(Item(i["id"], i["content"], due=due))

    def gen_org(self):
        """未完了のitem一覧からorg-fileを生成する (予めget_todoist_items()は実行しておく)"""

        for i in self.items:
            print(i)


class Item:
    def __init__(self, id, content, due=None, priority=None):

        self.id = id
        self.content = content
        self.priority = priority
        self.due = dateutil.parser.parse(due) if due else None

    def __repr__(self):
        return "<TODO({})_{}>".format(self.id, self.content[:20])

    def __str__(self):
        ret = "** TODO {}".format(self.content)

        if self.due:
            ret += "\n   DEADLINE: <{}>".format(self.due.strftime("%Y-%m-%d"))

        return ret
