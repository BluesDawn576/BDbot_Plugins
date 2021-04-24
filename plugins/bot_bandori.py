import const
import json
import time
import requests

from botoy import Action, GroupMsg
from botoy.collection import MsgTypes
from botoy.decorators import ignore_botself, in_content, these_msgtypes
from botoy.sugar import Text

@ignore_botself
@these_msgtypes(MsgTypes.TextMsg)
@in_content("(ycm|有车吗)")
def receive_group_msg(ctx: GroupMsg):
    try:
        if ctx.Content.startswith("ycm") or ctx.Content.startswith("有车吗"):
            Text(get_response())
    except BaseException as err:
        Text("执行指令时出错：\n{}\nline {}: {}".format(
        err.__traceback__.tb_frame.f_globals["__file__"],
        err.__traceback__.tb_lineno,
        err))

def get_response():
    response = requests.get("https://api.bandoristation.com/?function=query_room_number")
    response.encoding = "utf-8"
    raw_json = json.loads(response.text)

    if raw_json["status"] == "success":
        count = len(raw_json["response"])
        room = ""
        for i in raw_json["response"]:
            room += "[{}秒前] {}".format(time.time() - (i["time"] * 0.001), i["raw_message"])
        
        if count != 0:
            text = const.BOTNAME + "\n当前邦邦车站有{}辆车\n{}".format(count, room)
        else:
            text = "myc"

    return text