import const
import json
import requests

from botoy import Action, GroupMsg
from botoy.collection import MsgTypes
from botoy.decorators import ignore_botself, in_content, these_msgtypes
from botoy.sugar import Text

@ignore_botself
@these_msgtypes(MsgTypes.TextMsg)
@in_content(const.PREFIX + "一言")
def receive_group_msg(ctx: GroupMsg):
    try:
        if ctx.Content.startswith(const.PREFIX + "一言"):
            Text(get_response())
    except BaseException as err:
        Text("执行指令时出错：\n{}\nline {}: {}".format(
        err.__traceback__.tb_frame.f_globals["__file__"],
        err.__traceback__.tb_lineno,
        err))

def get_response():
    response = requests.get("https://v1.hitokoto.cn/")
    response.encoding = "utf-8"
    raw_json = json.loads(response.text)

    if raw_json["from_who"] == None:
        from_text = "「{}」".format(raw_json["from"])
    else:
        from_text = "{}「{}」".format(raw_json["from_who"], raw_json["from"])

    text = "『一言 hitokoto』\n{}\n——{}".format(raw_json["hitokoto"], from_text)

    return text