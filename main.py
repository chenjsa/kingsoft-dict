# -*- coding:utf-8 -*-

from __future__ import print_function

from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.HideWindowAction import HideWindowAction
from ulauncher.api.shared.action.DoNothingAction import DoNothingAction
from ulauncher.api.shared.event import KeywordQueryEvent
import json
import sys


try:
    from urllib2 import Request, urlopen
    reload(sys)
    sys.setdefaultencoding("utf-8")
except ModuleNotFoundError:
    from urllib.request import Request, urlopen
    from urllib.parse import quote

class KingsoftDictExtension(Extension):

    def __init__(self):
        super(KingsoftDictExtension, self).__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())


class KeywordQueryEventListener(EventListener):

    def get_action_to_render(self, name, description, on_enter=None):
        item = ExtensionResultItem(name=name,
                                   description=description,
                                   icon='images/icon.png',
                                   on_enter=on_enter or DoNothingAction())
        return RenderResultListAction([item])

    def on_event(self, event, extension):
        query = event.get_argument()
        if query:
            req = Request('http://dict-co.iciba.com/api/dictionary.php?type=json&key=F1D7870B690CBC2442A527DCB771E852&w={}'.format(quote(query)))
            response = urlopen(req)
            rsp_data = response.read()
            obj = json.loads(rsp_data)

            parts = []
            if "parts" in obj["symbols"][0].keys():
                parts = obj["symbols"][0]["parts"]
                print(parts)

            items = []
            for part in parts:
                means = ''
                desc = ''
                if isinstance(part["means"][0], str):
                    means = '; '.join(part["means"])
                    desc = part["part"] + ' ' + means
                else:
                    for word in part["means"]:
                        means = means + word["word_mean"] + '; '
                    desc = means

                # 替换'<'、'>'字符，否则字符串无法正常显示
                desc = desc.replace('<', '[')
                desc = desc.replace('>', ']')

                items.append(ExtensionResultItem(icon='images/icon.png', name=desc, on_enter=HideWindowAction()))

            if items:
                return RenderResultListAction(items)
            else:
                return self.get_action_to_render(name="Type in your query",
                                                 description="Example: word ")
        else:
            return self.get_action_to_render(name="Type in your query",
                                             description="Example: word ")


if __name__ == '__main__':
    KingsoftDictExtension().run()
