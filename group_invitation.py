# encoding:utf-8

import plugins
from bridge.context import ContextType
from bridge.reply import Reply, ReplyType
from common.log import logger
from plugins import *
from config import conf


@plugins.register(
    name="GroupInvitation",
    desire_priority=100,
    hidden=True,
    desc="关键词邀请好友入群",
    version="1.0",
    author="dfldylan",
)
class GroupInvitation(Plugin):
    def __init__(self):
        super().__init__()
        try:
            self.conf = super().load_config()
            if not self.conf:
                # 配置文件路径
                config_path = os.path.join(os.path.dirname(__file__), "config.json")

                # 加载或创建配置文件
                if os.path.exists(config_path):
                    with open(config_path, "r") as f:
                        self.conf = json.load(f)
                else:
                    self.conf = {}
                    with open(config_path, "w") as f:
                        json.dump(self.conf, f, indent=4)

            self.handlers[Event.ON_HANDLE_CONTEXT] = self.on_handle_context
            self.handlers[Event.ON_DECORATE_REPLY] = self.on_decorate_reply
            logger.info("[GroupInvitation] inited")
        except Exception as e:
            logger.warn("[GroupInvitation] init failed, ignore.")
            raise e

    def on_handle_context(self, e_context: EventContext):
        if e_context["context"].type != ContextType.TEXT or conf().get("channel_type") != "wx":
            return

        content = e_context["context"].content
        logger.debug(f"[GroupInvitation] Handling context. Content: {content}")

        group_name = self.conf.get(content)
        if group_name:
            reply = Reply(ReplyType.INVITE_ROOM, group_name)
            e_context["reply"] = reply
            e_context.action = EventAction.BREAK_PASS
            logger.info(f"[GroupInvitation] Inviting to group: {group_name} for content: {content}")

    def on_decorate_reply(self, e_context: EventContext):
        reply = e_context["reply"]
        if reply.type == ReplyType.INVITE_ROOM:
            e_context.action = EventAction.BREAK_PASS

    def get_help_text(self, **kwargs):
        help_text = "根据关键字邀请入群\n"
        return help_text
