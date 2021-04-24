import const
from botoy import Action, Botoy, EventMsg, FriendMsg, GroupMsg
from botoy import decorators as deco

qq = 12345678
bot = Botoy(qq=qq, use_plugins=True)
action = Action(qq)

@bot.group_context_use
def group_ctx_middleware(ctx):
    ctx.master = 123456  # 主人qq
    return ctx

@bot.on_group_msg
@deco.queued_up(name="manage_plugin")
def manage_plugin(ctx: GroupMsg):
    if ctx.FromUserId != ctx.master:
        return
    action = Action(ctx.CurrentQQ)
    c = ctx.Content
    if c == const.PREFIX + "插件管理":
        action.sendGroupText(
            ctx.FromGroupId,
            (
                const.PREFIX + "插件 => 发送启用插件列表\n" +
                const.PREFIX + "已停用插件 => 发送停用插件列表\n" +
                const.PREFIX + "刷新插件 => 刷新所有插件,包括新建文件\n" +
                const.PREFIX + "重载插件+插件名 => 重载指定插件\n" +
                const.PREFIX + "停用插件+插件名 => 停用指定插件\n" +
                const.PREFIX + "启用插件+插件名 => 启用指定插件\n"
            ),
        )
        return
    # 发送启用插件列表
    if c == const.PREFIX + "插件":
        action.sendGroupText(ctx.FromGroupId, "\n".join(bot.plugins))
        return
    # 发送停用插件列表
    if c == const.PREFIX + "已停用插件":
        action.sendGroupText(ctx.FromGroupId, "\n".join(bot.removed_plugins))
        return
    try:
        if c == const.PREFIX + "刷新插件":
            bot.reload_plugins()
            action.sendGroupText(ctx.FromGroupId, "操作完成")
        # 重载指定插件 /重载插件+[插件名]
        elif c.startswith(const.PREFIX + "重载插件"):
            plugin_name = c[5:]
            bot.reload_plugin(plugin_name)
            action.sendGroupText(ctx.FromGroupId, "操作完成")
        # 停用指定插件 /停用插件+[插件名]
        elif c.startswith(const.PREFIX + "停用插件"):
            plugin_name = c[5:]
            bot.remove_plugin(plugin_name)
            action.sendGroupText(ctx.FromGroupId, "操作完成")
        # 启用指定插件 /启用插件+[插件名]
        elif c.startswith(const.PREFIX + "启用插件"):
            plugin_name = c[5:]
            bot.recover_plugin(plugin_name)
            action.sendGroupText(ctx.FromGroupId, "操作完成")
    except Exception as e:
        action.sendGroupText(ctx.FromGroupId, "操作失败: %s" % e)
        

def on_group_msg(ctx: GroupMsg):
    # 不处理自身消息
    if ctx.FromUserId == ctx.CurrentQQ:
        return

@bot.on_event
def event(ctx: EventMsg):
    pass

if __name__ == "__main__":
    bot.run()