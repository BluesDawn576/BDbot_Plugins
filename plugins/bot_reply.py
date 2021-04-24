import const

from botoy import Action, GroupMsg
from botoy.collection import MsgTypes
from botoy.decorators import ignore_botself, in_content, these_msgtypes
from botoy.refine import refine_pic_group_msg
from botoy.sugar import Text

@ignore_botself
@these_msgtypes(MsgTypes.TextMsg, MsgTypes.PicMsg)
@in_content(const.PREFIX + "复读")
def receive_group_msg(ctx: GroupMsg):
    if ctx.MsgType == MsgTypes.TextMsg:
        if ctx.Content.startswith(const.PREFIX + "复读"):
            text = ctx.Content[3:]
            while text.startswith(const.PREFIX + "复读"):
                text = text[3:]
            if text:
                Text(text)
    elif ctx.MsgType == MsgTypes.PicMsg:
        pic_ctx = refine_pic_group_msg(ctx)
        Action(ctx.CurrentQQ).sendGroupPic(
            ctx.FromGroupId, picMd5s=[pic.FileMd5 for pic in pic_ctx.GroupPic]
        )