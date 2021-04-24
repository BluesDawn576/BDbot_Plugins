import const
import json
import requests

from botoy import Action, GroupMsg
from botoy.collection import MsgTypes
from botoy.decorators import ignore_botself, in_content, these_msgtypes
from botoy.refine import refine_pic_group_msg
from botoy.sugar import Text

@ignore_botself
@these_msgtypes(MsgTypes.TextMsg)
@in_content(const.PREFIX + "(mc|player)")
def receive_group_msg(ctx: GroupMsg):
    try:
        if ctx.Content.startswith(const.PREFIX + "mc"):
            text = ctx.Content[3:].lstrip()
            if text == "":
                Text(const.BOTNAME + "指令无效，{}mc <ip地址>".format(const.PREFIX))
                return

            msg_text, pic_base64 = get_server_info(text)
            if pic_base64 != 0:
                Action(ctx.CurrentQQ).sendGroupPic(
                    ctx.FromGroupId,
                    content = msg_text,
                    picBase64Buf = pic_base64
                )
            else:
                Text(msg_text)
        elif ctx.Content.startswith(const.PREFIX + "player"):
            text = ctx.Content[7:].lstrip()
            if text == "":
                Text(const.BOTNAME + "指令无效，{}player <ip地址>".format(const.PREFIX))
                return

            Text(const.BOTNAME + get_server_player(text))
    except BaseException as err:
        Text("执行指令时出错：\n{}\nline {}: {}".format(
        err.__traceback__.tb_frame.f_globals["__file__"],
        err.__traceback__.tb_lineno,
        err))

def get_response(msg_text):
    response = requests.get("https://api.bluesdawn.top/minecraft/server/api?host={}".format(msg_text))
    response.encoding = "utf-8"
    raw_json = json.loads(response.text)

    return raw_json

def get_server_info(msg_text):

    res_json = get_response(msg_text)

    res_status = res_json["status"]

    if res_status == "Online":

        res_favicon = res_json["favicon"]
        res_version = res_json["version"]["version"]
        res_motd = res_json["motd"]["clean"]
        res_mods = res_json["mods"]
        res_player = res_json["players"]
        res_ping = res_json["queryinfo"]["processed"]

        if res_version:
            ver = res_version
        else:
            ver = "未知"

        if "extra" in res_motd:
            motd = res_motd["extra"][0]["text"]
        elif "text" in res_motd:
            motd = res_motd["text"]
        else:
            motd = res_motd

        if res_mods["type"]:
            mods_text = "\n[{}服，包含{}个模组]".format(res_mods["type"], len(res_mods["modlist"]))
        else:
            mods_text = ""

        if res_favicon:
            pic_base64 = res_favicon.replace("data:image/png;base64,","")
        else:
            pic_base64 = "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAIAAACQkWg2AAAACXBIWXMAAA7EAAAOxAGVKw4bAAAFyGlUWHRYTUw6Y29tLmFkb2JlLnhtcAAAAAAAPD94cGFja2V0IGJlZ2luPSLvu78iIGlkPSJXNU0wTXBDZWhpSHpyZVN6TlRjemtjOWQiPz4gPHg6eG1wbWV0YSB4bWxuczp4PSJhZG9iZTpuczptZXRhLyIgeDp4bXB0az0iQWRvYmUgWE1QIENvcmUgNS42LWMxNDggNzkuMTY0MDM2LCAyMDE5LzA4LzEzLTAxOjA2OjU3ICAgICAgICAiPiA8cmRmOlJERiB4bWxuczpyZGY9Imh0dHA6Ly93d3cudzMub3JnLzE5OTkvMDIvMjItcmRmLXN5bnRheC1ucyMiPiA8cmRmOkRlc2NyaXB0aW9uIHJkZjphYm91dD0iIiB4bWxuczp4bXA9Imh0dHA6Ly9ucy5hZG9iZS5jb20veGFwLzEuMC8iIHhtbG5zOnhtcE1NPSJodHRwOi8vbnMuYWRvYmUuY29tL3hhcC8xLjAvbW0vIiB4bWxuczpzdEV2dD0iaHR0cDovL25zLmFkb2JlLmNvbS94YXAvMS4wL3NUeXBlL1Jlc291cmNlRXZlbnQjIiB4bWxuczpkYz0iaHR0cDovL3B1cmwub3JnL2RjL2VsZW1lbnRzLzEuMS8iIHhtbG5zOnBob3Rvc2hvcD0iaHR0cDovL25zLmFkb2JlLmNvbS9waG90b3Nob3AvMS4wLyIgeG1wOkNyZWF0b3JUb29sPSJBZG9iZSBQaG90b3Nob3AgMjEuMCAoV2luZG93cykiIHhtcDpDcmVhdGVEYXRlPSIyMDIxLTA0LTIzVDE5OjAxOjU3KzA4OjAwIiB4bXA6TWV0YWRhdGFEYXRlPSIyMDIxLTA0LTIzVDE5OjAxOjU3KzA4OjAwIiB4bXA6TW9kaWZ5RGF0ZT0iMjAyMS0wNC0yM1QxOTowMTo1NyswODowMCIgeG1wTU06SW5zdGFuY2VJRD0ieG1wLmlpZDoyOTdmMjE4Ni01Mjc0LTIzNDMtOGZiOC04NTEwNjRkMTgyMWYiIHhtcE1NOkRvY3VtZW50SUQ9ImFkb2JlOmRvY2lkOnBob3Rvc2hvcDo3NTBmZGM1ZS00MzNiLTkzNDEtYTgzNC0zNWE3OWRkNzZhMjIiIHhtcE1NOk9yaWdpbmFsRG9jdW1lbnRJRD0ieG1wLmRpZDo1ODJiYWFkZi0xMzM1LTQxNGItYjc0Yy0xNzIxNDNmMGVjNjMiIGRjOmZvcm1hdD0iaW1hZ2UvcG5nIiBwaG90b3Nob3A6Q29sb3JNb2RlPSIzIj4gPHhtcE1NOkhpc3Rvcnk+IDxyZGY6U2VxPiA8cmRmOmxpIHN0RXZ0OmFjdGlvbj0iY3JlYXRlZCIgc3RFdnQ6aW5zdGFuY2VJRD0ieG1wLmlpZDo1ODJiYWFkZi0xMzM1LTQxNGItYjc0Yy0xNzIxNDNmMGVjNjMiIHN0RXZ0OndoZW49IjIwMjEtMDQtMjNUMTk6MDE6NTcrMDg6MDAiIHN0RXZ0OnNvZnR3YXJlQWdlbnQ9IkFkb2JlIFBob3Rvc2hvcCAyMS4wIChXaW5kb3dzKSIvPiA8cmRmOmxpIHN0RXZ0OmFjdGlvbj0ic2F2ZWQiIHN0RXZ0Omluc3RhbmNlSUQ9InhtcC5paWQ6Mjk3ZjIxODYtNTI3NC0yMzQzLThmYjgtODUxMDY0ZDE4MjFmIiBzdEV2dDp3aGVuPSIyMDIxLTA0LTIzVDE5OjAxOjU3KzA4OjAwIiBzdEV2dDpzb2Z0d2FyZUFnZW50PSJBZG9iZSBQaG90b3Nob3AgMjEuMCAoV2luZG93cykiIHN0RXZ0OmNoYW5nZWQ9Ii8iLz4gPC9yZGY6U2VxPiA8L3htcE1NOkhpc3Rvcnk+IDwvcmRmOkRlc2NyaXB0aW9uPiA8L3JkZjpSREY+IDwveDp4bXBtZXRhPiA8P3hwYWNrZXQgZW5kPSJyIj8+HpfG2wAAACtJREFUKJFj/G/8nwEbYDzLiFWcCasoHjCqgRiAPbAZGBhwxc8g9MNw0AAAa+IFUOu3r0oAAAAASUVORK5CYII="
        
        text = "状态：在线\n人数：{}/{}\nMOTD：{}\n版本：{}\nPing：{}{}".format(
            res_player["online"],
            res_player["max"],
            motd,
            ver,
            res_ping,
            mods_text
        )

        return [const.BOTNAME + text, pic_base64]
    else:
        text = "连接超时或离线"
        return [const.BOTNAME + text, 0]
    
    
    
def get_server_player(msg_text):

    res_json = get_response(msg_text)

    res_status = res_json["status"]

    if res_status == "Online":

        res_player = res_json["players"]

        count = res_player["online"]
        if count > 0:
            if "0" in res_player["list"]:
                player = "\n"
                for i in res_player["list"]:
                    player += i["name"] + "\n"
            else:
                player = "无法获取到玩家列表"
        else:
            player = "没有玩家在线"
        
        text = "状态：在线\n人数：{}/{}\n玩家：{}".format(
            res_player["online"],
            res_player["max"],
            player
        )
    else:
        text = "连接超时或离线"
    
    return text