import json
from .. import define
from .. import interface
from .. import mm_pb2
from .. import Util
from . import verify_friend
from . import handle_appmsg
from . import tuling_robot
from .logger_wrapper import logger

# 测试命令
state = lambda i: '已开启' if i else '已关闭'
TEST_KEY_WORD = ('测试分享链接', '测试好友列表','图灵机器人','自动通过好友申请','自动抢红包','测试扔骰子')
# 测试开关
TEST_STATE    = [1,1,1,1,1,1]

# 插件黑名单(不处理该wxid的消息)
plugin_blacklist = ['weixin', ]

# 测试接口
def test(msg):
    global TEST_STATE
    # 来自群聊的消息不处理
    if '测试' == msg.raw.content:                                                                                                   # help
        send_text = '当前支持的测试指令:\n'
        for i in range(len(TEST_KEY_WORD)):
            send_text += '[{}]{}({})\n'.format(i, TEST_KEY_WORD[i],state(TEST_STATE[i]))
        interface.new_send_msg(msg.from_id.id, send_text.encode(encoding="utf-8"))
        return False
    elif TEST_KEY_WORD[0] == msg.raw.content or '0' == msg.raw.content:                                                             # 测试分享链接
        interface.send_app_msg(msg.from_id.id, '贪玩蓝月', '大渣好,我系咕天乐,我是渣渣辉,贪挽懒月,介系一个你没有挽过的船新版本', 'http://www.gov.cn/','https://ss0.bdstatic.com/-0U0bnSm1A5BphGlnYG/tam-ogel/f1d67c57e00fea1dc0f90210d7add1ad_121_121.jpg')
        return False
    elif TEST_KEY_WORD[1] == msg.raw.content or '1' == msg.raw.content:                                                             # 测试获取好友列表
        interface.new_send_msg(msg.from_id.id, Util.str2bytes('我有好友{}人,加入群聊{}个,已关注公众号{}个,黑名单中好友{}位,已删除好友{}名'.format(len(interface.get_contact_list(Util.CONTACT_TYPE_FRIEND)), len(interface.get_contact_list(
            Util.CONTACT_TYPE_CHATROOM)), len(interface.get_contact_list(Util.CONTACT_TYPE_OFFICAL)), len(interface.get_contact_list(Util.CONTACT_TYPE_BLACKLIST)), len(interface.get_contact_list(Util.CONTACT_TYPE_DELETED)))))
        return False
    elif TEST_KEY_WORD[2] == msg.raw.content or '2' == msg.raw.content:                                                             # 图灵机器人开关
        TEST_STATE[2] =  not TEST_STATE[2]
        interface.new_send_msg(msg.from_id.id, '{}({})'.format(TEST_KEY_WORD[2],state(TEST_STATE[2])).encode(encoding="utf-8"))
        return False
    elif TEST_KEY_WORD[3] == msg.raw.content or '3' == msg.raw.content:                                                             # 自动通过好友申请开关
        TEST_STATE[3] =  not TEST_STATE[3]
        interface.new_send_msg(msg.from_id.id, '{}({})'.format(TEST_KEY_WORD[3],state(TEST_STATE[3])).encode(encoding="utf-8"))
        return False
    elif TEST_KEY_WORD[4] == msg.raw.content or '4' == msg.raw.content:                                                             # 自动抢红包开关
        TEST_STATE[4] =  not TEST_STATE[4]
        interface.new_send_msg(msg.from_id.id, '{}({})'.format(TEST_KEY_WORD[4],state(TEST_STATE[4])).encode(encoding="utf-8"))
        return False
    elif TEST_KEY_WORD[5] == msg.raw.content or '5' == msg.raw.content:                                                             # 测试发送骰子表情
        interface.new_send_msg(msg.from_id.id, '送你一波666'.encode(encoding="utf-8"))
        interface.send_emoji(msg.from_id.id,'68f9864ca5c0a5d823ed7184e113a4aa','1','9')
        interface.send_emoji(msg.from_id.id,'514914788fc461e7205bf0b6ba496c49','2','9')
        interface.send_emoji(msg.from_id.id,'9a21c57defc4974ab5b7c842e3232671','1','9')
        return False     
    return True

# 处理消息
def dispatch(msg):
    # 过滤wxid
    if msg.from_id.id in plugin_blacklist:
        return

    # 文字消息
    if 1 == msg.type:
        # 测试接口
        if test(msg):
            if TEST_STATE[2]:
                # 机器人回复消息
                tuling_robot.tuling_robot(msg)
    # 好友请求消息
    elif 37 == msg.type:
        if TEST_STATE[3]:
            # 自动通过好友申请
            verify_friend.auto_verify_friend(msg)
    # appmsg
    elif 49 == msg.type:
            handle_appmsg.appmsg_handler(msg)
    else:
        pass
    return
