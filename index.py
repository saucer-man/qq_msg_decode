import struct
import binascii
import sqlite3
faceMap = {
	14:  "微笑",
	1:   "撇嘴",
	2:   "色",
	3:   "发呆",
	4:   "得意",
	6:   "害羞",
	7:   "闭嘴",
	8:   "睡",
	9:   "大哭",
	5:   "流泪",
	10:  "尴尬",
	11:  "发怒",
	12:  "调皮",
	13:  "呲牙",
	0:   "惊讶",
	15:  "难过",
	16:  "酷",
	96:  "冷汗",
	18:  "抓狂",
	19:  "吐",
	20:  "偷笑",
	21:  "可爱",
	22:  "白眼",
	23:  "傲慢",
	24:  "饥饿",
	25:  "困",
	26:  "惊恐",
	27:  "流汗",
	28:  "憨笑",
	29:  "悠闲",
	30:  "奋斗",
	31:  "咒骂",
	32:  "疑问",
	33:  "嘘",
	34:  "晕",
	35:  "折磨",
	36:  "衰",
	37:  "骷髅",
	38:  "敲打",
	39:  "再见",
	97:  "擦汗",
	98:  "抠鼻",
	99:  "鼓掌",
	100: "糗大了",
	101: "坏笑",
	102: "左哼哼",
	103: "右哼哼",
	104: "哈欠",
	105: "鄙视",
	106: "委屈",
	107: "快哭了",
	108: "阴险",
	305: "右亲亲",
	109: "左亲亲",
	110: "吓",
	111: "可怜",
	172: "眨眼睛",
	182: "笑哭",
	179: "doge",
	173: "泪奔",
	174: "无奈",
	212: "托腮",
	175: "卖萌",
	178: "斜眼笑",
	177: "喷血",
	180: "惊喜",
	181: "骚扰",
	176: "小纠结",
	183: "我最美",
	245: "加油必胜",
	246: "加油抱抱",
	247: "口罩护体",
	260: "搬砖中",
	261: "忙到飞起",
	262: "脑阔疼",
	263: "沧桑",
	264: "捂脸",
	265: "辣眼睛",
	266: "哦哟",
	267: "头秃",
	268: "问号脸",
	269: "暗中观察",
	270: "emm",
	271: "吃瓜",
	272: "呵呵哒",
	277: "汪汪",
	307: "喵喵",
	306: "牛气冲天",
	281: "无眼笑",
	282: "敬礼",
	283: "狂笑",
	284: "面无表情",
	285: "摸鱼",
	293: "摸锦鲤",
	286: "魔鬼笑",
	287: "哦",
	288: "请",
	289: "睁眼",
	294: "期待",
	295: "拿到红包",
	296: "真好",
	297: "拜谢",
	298: "元宝",
	299: "牛啊",
	300: "胖三斤",
	301: "好闪",
	303: "右拜年",
	302: "左拜年",
	304: "红包包",
	322: "拒绝",
	323: "嫌弃",
	311: "打call",
	312: "变形",
	313: "嗑到了",
	314: "仔细分析",
	315: "加油",
	316: "我没事",
	317: "菜汪",
	318: "崇拜",
	319: "比心",
	320: "庆祝",
	321: "老色痞",
	324: "吃糖",
	325: "惊吓",
	326: "生气",
	53:  "蛋糕",
	114: "篮球",
	327: "加一",
	328: "错号",
	329: "对号",
	330: "完成",
	331: "明白",
	49:  "拥抱",
	66:  "爱心",
	63:  "玫瑰",
	64:  "凋谢",
	187: "幽灵",
	146: "爆筋",
	116: "示爱",
	67:  "心碎",
	60:  "咖啡",
	185: "羊驼",
	192: "红包",
	137: "鞭炮",
	138: "灯笼",
	136: "双喜",
	76:  "赞",
	124: "OK",
	118: "抱拳",
	78:  "握手",
	119: "勾引",
	79:  "胜利",
	120: "拳头",
	121: "差劲",
	77:  "踩",
	122: "爱你",
	123: "NO",
	201: "点赞",
	203: "托脸",
	204: "吃",
	202: "无聊",
	200: "拜托",
	194: "不开心",
	193: "大笑",
	197: "冷漠",
	211: "我不看",
	210: "飙泪",
	198: "呃",
	199: "好棒",
	207: "花痴",
	205: "送花",
	206: "害怕",
	208: "小样儿",
	308: "求红包",
	309: "谢红包",
	310: "新年烟花",
	290: "敲开心",
	291: "震惊",
	292: "让我康康",
	226: "拍桌",
	215: "糊脸",
	237: "偷看",
	214: "啵啵",
	235: "颤抖",
	222: "抱抱",
	217: "扯一扯",
	221: "顶呱呱",
	225: "撩一撩",
	241: "生日快乐",
	227: "拍手",
	238: "扇脸",
	240: "喷脸",
	229: "干杯",
	216: "拍头",
	218: "舔一舔",
	233: "掐一掐",
	219: "蹭一蹭",
	244: "扔狗",
	232: "佛系",
	243: "甩头",
	223: "暴击",
	279: "打脸",
	280: "击掌",
	231: "哼",
	224: "开枪",
	278: "汗",
	236: "啃头",
	228: "恭喜",
	220: "拽炸天",
	239: "原谅",
	242: "头撞击",
	230: "嘲讽",
	234: "惊呆",
	273: "我酸了",
	75:  "月亮",
	74:  "太阳",
	46:  "猪头",
	112: "菜刀",
	56:  "刀",
	169: "手枪",
	171: "茶",
	59:  "便便",
	144: "喝彩",
	147: "棒棒糖",
	89:  "西瓜",
	61:  "饭",
	148: "喝奶",
	274: "太南了",
	113: "啤酒",
	140: "K歌",
	188: "蛋",
	55:  "炸弹",
	184: "河蟹",
	158: "钞票",
	54:  "闪电",
	69:  "礼物",
	190: "菊花",
	151: "飞机",
	145: "祈祷",
	117: "瓢虫",
	168: "药",
	115: "乒乓",
	57:  "足球",
	41:  "发抖",
	125: "转圈",
	42:  "爱情",
	43:  "跳跳",
	86:  "怄火",
	129: "挥手",
	85:  "飞吻",
	126: "磕头",
	128: "跳绳",
	130: "激动",
	127: "回头",
	132: "献吻",
	134: "右太极",
	133: "左太极",
	131: "街舞",
	276: "辣椒酱",
}
MsgText = 1
MsgFace = 2
MsgGroupImage = 3
MsgPrivateImage = 6
MsgVoice = 7
MsgNickName = 18
MsgVideo = 26
class Buffer:
    def __init__(self, buf: bytes):
        self.buf = buf
        self.off = 0

    def empty(self):
        return len(self.buf) <= self.off

    # 读取n个字节
    def read(self, n)->bytes:
        if self.empty():
            return None
        r = self.buf[self.off:self.off+n]
        self.off += n
        return r

    # 跳过n个字节
    def skip(self, n):
        self.off += n

    # 获取4个字节，转化为小端int
    def uint32(self)->int:
        u, = struct.unpack_from("<I", self.buf, self.off)
        # 等同于
        # u = int.from_bytes(self.buf[self.off:self.off+4], byteorder='little')
        self.off += 4
        return u
     # 获取2个字节，转化为小端int
    def uint16(self):
        u, = struct.unpack_from("<H", self.buf, self.off)
        self.off += 2
        return u
    
    # 获取1个字节
    def byte(self)->int:
        by = self.buf[self.off]
        self.off += 1
        return by

    # 获取一个字节
    def t(self)->int:
        return self.byte()

    # 获取2个字节
    def l(self)->int:
        return self.uint16()

    def tlv(self):
        t = self.t()
        l = self.l()
        v = self.read(l)
        return t, l, v

class MsgElem:
    def Type(self):
        pass

class Header:
    def __init__(self):
        self.Time = 0
        self.Rand = 0
        self.Color = 0
        self.FontSize = 0
        self.FontStyle = 0
        self.Charset = 0
        self.FontFamily = 0
        self.FontName = ""
    def __str__(self):  # 定义打印对象时打印的字符串
        return ','.join([f'{k}:{v}' for k,v in self.__dict__.items()])

def DecodeNickname(b:bytes)->str:
    # print(f"进入DecodeNickname,len(b):{len(b)}")
    buf = Buffer(b)
    while not buf.empty():
        t, _, v = buf.tlv()
        # print(f"DecodeNickname内部,t:{t}, v:{v}")
        if t in (1,2):
            return v.decode("utf-16")
        return ""

class Msg:
    def __init__(self):
        self.Header = Header()
        self.Elements = []
        self.SenderNickname = ""
    def __str__(self):  # 定义打印对象时打印的字符串
        return '\n'.join([f'{k}:{v}' for k,v in self.__dict__.items()])

MsgText = 1
MsgFace = 2
MsgGroupImage = 3
MsgPrivateImage = 6
MsgVoice = 7
MsgNickName = 18
MsgVideo = 26

class TextElement:
    def __init__(self, content):
        self.Content = content

    def Type(self):
        return MsgText

    def __str__(self):
        return self.Content

class ImageElement:
    def __init__(self):
        self.Path = ""
        self.Hash = bytes()

    def Type(self):
        return MsgGroupImage

class FaceElement:
    def __init__(self, id, name):
        self.Id = id
        self.Name = name

    def Type(self):
        return MsgFace

class VoiceElement:
    def __init__(self, hash):
        self.Hash = hash

    def Type(self):
        return MsgVoice

class VideoElement:
    def __init__(self, hash):
        self.Hash = hash

    def Type(self):
        return MsgVideo

def DecodeTextMsg(b):
    buf = Buffer(b)
    while not buf.empty():
        t, _, v = buf.tlv()
        # print(f"DecodeTextMsg内部:t:{t}, v:{v.decode('utf-16')}")
        if t == 1:
            return TextElement(content=v.decode("utf-16"))
    return None

def DecodeFace(b):
    buf = Buffer(b)
    while not buf.empty():
        t, _, v = buf.tlv()
        if t == 1:
            id = 0
            for byte in v:
                id = (id << 8) | byte
            if id not in faceMap:
                return FaceElement(id=id, name="未知")
            return FaceElement(id=id, name=faceMap[id])
    return None

def DecodeImage(b):
    elem = ImageElement()
    buf = Buffer(b)
    while not buf.empty():
        t, _, v = buf.tlv()
        if t == 1:
            elem.Hash = v
        elif t == 2:
            elem.Path = v.decode("utf-16")
    return elem

def DecodeVoice(b):
    buf = Buffer(b)
    while not buf.empty():
        t, _, v = buf.tlv()
        if t == 1:
            return VoiceElement(hash=v)
    return None

def DecodeVideo(b):
    buf = Buffer(b)
    while not buf.empty():
        t, _, v = buf.tlv()
        if t == 1:
            h = bytearray(v[244:244+16])
            for i in range(len(h)):
                h[i] ^= 0xEF
            return VideoElement(hash=h)
    return None
MsgDecoders = {
    MsgText:         DecodeTextMsg,
    MsgFace:         DecodeFace,
    MsgGroupImage:   DecodeImage,
    MsgPrivateImage: DecodeImage,
    MsgVoice:        DecodeVoice,
    MsgVideo:        DecodeVideo,
}



def encode_msg(msg)->str:
    # print(f"进入encode_msg")
    def encode_elem(elems):
        ok = ""
       
        for elem in elems:
            # print(type(elem))
            if isinstance(elem, TextElement):
                # print(f"encode_elem命中了TextElement")
                ok += elem.Content
            elif isinstance(elem, ImageElement):
                # print(f"encode_elem命中了ImageElement")
                # print(f"[t:img,path={elem.Path},hash={binascii.hexlify(elem.Hash).decode('utf-8')}]")
                ok += f"[t:img,path={elem.Path},hash={binascii.hexlify(elem.Hash).decode('utf-8')}]"
            elif isinstance(elem, VoiceElement):
                # print(f"encode_elem命中了VoiceElement")
                # todo:这里需要对elem.Hash进行base48编码,就是file了
                ok += f"[t:voice,file="",hash={binascii.hexlify(elem.Hash).decode('utf-8')}.amr]"
            elif isinstance(elem, VideoElement):
                # print(f"encode_elem命中了VideoElement")
                ok += f"[t:video,hash={binascii.hexlify(elem.Hash).decode('utf-8')}]"
            elif isinstance(elem, FaceElement):
                # print(f"encode_elem命中了FaceElement")
                ok += f"[t:face,id={elem.Id},name={elem.Name}]"
            elif isinstance(elem, str):
                # print(f"encode_elem命中了str")
                ok += elem
            else:
                print(f"没有命中任何类型")

        return ok

    return encode_elem(msg.Elements)
def Unpack(b:bytes)->Msg:
    msg = Msg()
    header = Header()
    buf = Buffer(b)
    buf.skip(8)
    header.Time = buf.uint32()
    # print(f"header.Time:{header.Time}")
    header.Rand = buf.uint32()
    header.Color = buf.uint32()
    header.FontSize = buf.byte()
    header.FontStyle = buf.byte()
    header.Charset = buf.byte()
    header.FontFamily = buf.byte()
    fontName = buf.read(int(buf.uint16()))
    header.FontName = fontName.decode("utf-16")
    msg.Header = header
    buf.skip(2)

    while not buf.empty():
        t, _, v = buf.tlv()
        if t == MsgNickName:

            msg.SenderNickname = DecodeNickname(v)
        else:
            
            if t in MsgDecoders:
                msg.Elements.append(MsgDecoders[t](v))

    return msg

# 连接数据库
conn = sqlite3.connect('Msg3.0.db_0_aaaa.db')
cur = conn.cursor()
# 获取表名
cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
for table in cur.fetchall():
    table_name = table[0]
    print(f"下面开始解码 table_name: {table_name}")
    # 获取表的列名
    cur.execute("SELECT * FROM {} limit 1".format(table_name))
    # print(f"cur.description:{cur.description}")
    col_name_list = [tuple[0] for tuple in cur.description]
    if "MsgContent" not in col_name_list: # 如果这个表不包含MsgContent,则不做处理
        continue
    # print(col_name_list)
    if "DecodedMsg" in col_name_list:
        print(f"{table_name}已经解码过, 跳过")
        continue
    # 尝试增加一列
    try:
		#添加新列到数据库
        add_column=f'ALTER TABLE {table_name} ADD DecodedMsg text'
        cur.execute(add_column)
        conn.commit()
    except Exception as e:
        print(f"添加新列到数据库失败:{e}")
        pass
    # 遍历每一列并且更新DecodedMsg字段
    # 获取查询结果
    cur.execute(f"SELECT TIME, MsgContent FROM {table_name}")
    rows = cur.fetchall()
    for row in rows:
        time,msg_content = row
        msg = Unpack(msg_content)
        sql = f"UPDATE {table_name} SET `DecodedMsg` = ? WHERE TIME = ?"
        cur.execute(sql,(encode_msg(msg),time))
        # print(f"UPDATE {table_name} SET `DecodedMsg` = {encode_msg(msg)} WHERE TIME = {time}")
        # 提交
        conn.commit()
cur.close()
conn.close()