import sys
import json
import math
import struct
import binascii
import sqlite3

# 从 face.json 中读取表情映射
with open('face.json', 'r', encoding='utf-8') as f:
	faceMap = json.load(f)

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
        return self.buf is None or len(self.buf) <= self.off

    # 读取n个字节
    def read(self, n) -> bytes:
        if self.empty():
            return None
        r = self.buf[self.off : self.off + n]
        self.off += n
        return r

    # 跳过n个字节
    def skip(self, n):
        self.off += n

    # 获取4个字节，转化为小端int
    def uint32(self) -> int:
        (u,) = struct.unpack_from("<I", self.buf, self.off)
        # 等同于
        # u = int.from_bytes(self.buf[self.off:self.off+4], byteorder='little')
        self.off += 4
        return u

    # 获取2个字节，转化为小端int
    def uint16(self):
        (u,) = struct.unpack_from("<H", self.buf, self.off)
        self.off += 2
        return u

    # 获取1个字节
    def byte(self) -> int:
        by = self.buf[self.off]
        self.off += 1
        return by

    # 获取一个字节
    def t(self) -> int:
        return self.byte()

    # 获取2个字节
    def l(self) -> int:
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
        return ",".join([f"{k}:{v}" for k, v in self.__dict__.items()])


def DecodeNickname(b: bytes) -> str:
    # print(f"进入DecodeNickname,len(b):{len(b)}")
    buf = Buffer(b)
    while not buf.empty():
        t, _, v = buf.tlv()
        # print(f"DecodeNickname内部,t:{t}, v:{v}")
        if t in (1, 2):
            return v.decode("utf-16")
        return ""


class Msg:
    def __init__(self):
        self.Header = Header()
        self.Elements = []
        self.SenderNickname = ""

    def __str__(self):  # 定义打印对象时打印的字符串
        return "\n".join([f"{k}:{v}" for k, v in self.__dict__.items()])


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
            h = bytearray(v[244 : 244 + 16])
            for i in range(len(h)):
                h[i] ^= 0xEF
            return VideoElement(hash=h)
    return None


MsgDecoders = {
    MsgText: DecodeTextMsg,
    MsgFace: DecodeFace,
    MsgGroupImage: DecodeImage,
    MsgPrivateImage: DecodeImage,
    MsgVoice: DecodeVoice,
    MsgVideo: DecodeVideo,
}


def encode_msg(msg) -> str:
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
                ok += (
                    f"[t:voice,file="
                    ",hash={binascii.hexlify(elem.Hash).decode('utf-8')}.amr]"
                )
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
                print("[!]", end='', flush=True)

        return ok

    return encode_elem(msg.Elements)


def Unpack(b: bytes) -> Msg:
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


def run(db_path: str):
    # 连接数据库
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    # 获取表名
    cur.execute("PRAGMA mmap_size = 10240000")  # 1mb 内存缓存
    cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
    for table in cur.fetchall():
        table_name = table[0]
        print(f"开始解码 {table_name}", end='|')
        # 获取表的列名
        cur.execute(f"SELECT * FROM {table_name} limit 1")
        # print(f"cur.description:{cur.description}")
        col_name_list = [tuple[0] for tuple in cur.description]
        if "MsgContent" not in col_name_list:  # 如果这个表不包含MsgContent,则不做处理
            print(f"不包含MsgContent, 跳过")
            continue
        # print(col_name_list)
        if "DecodedMsg" in col_name_list:
            print(f"已经解码过, 跳过")
            continue
        # 尝试增加一列
        try:
            # 添加新列到数据库
            cur.execute(f"ALTER TABLE {table_name} ADD DecodedMsg text")
            conn.commit()
        except Exception as e:
            print(f"添加新列到数据库失败:{e}")
            continue
        # 遍历每一列并且更新DecodedMsg字段
        # 获取查询结果
        cur.execute(f"SELECT TIME, MsgContent FROM {table_name}")
        try:
            rows = cur.fetchall()
        except Exception as e:
            print(f"获取查询结果失败:{e}")
            continue
        row_len = len(rows)
        
        if row_len == 0:
            print('没有数据,跳过')
            continue
        
        print(f"数据长度: {row_len} log10: {math.log10(row_len)}")
        log_size = math.log10(row_len)  # 取对数 算个位数 整个进度
        if row_len > 500:  
            # 超过 500 条数据 就输出进度条
            # 进度条长度 100 个 .
            print_len = int(row_len / 100)
            print(f"比例: 1:{print_len}")
            counter = 0
            for row in rows:
                time, msg_content = row
                msg = Unpack(msg_content)
                cur.execute(f"UPDATE {table_name} SET `DecodedMsg` = ? WHERE TIME = ?", (encode_msg(msg), time,))
                # print(f"UPDATE {table_name} SET `DecodedMsg` = {encode_msg(msg)} WHERE TIME = {time}")
                # 提交
                counter += 1
                if counter > print_len:
                    counter = 0
                    print('.', end='', flush=True)
                    conn.commit()
            conn.commit()
        else:
            # 不足 500 条数据 就不输出进度条
            for row in rows:
                time, msg_content = row
                msg = Unpack(msg_content)
                cur.execute(f"UPDATE {table_name} SET `DecodedMsg` = ? WHERE TIME = ?", (encode_msg(msg), time,))
                # print(f"UPDATE {table_name} SET `DecodedMsg` = {encode_msg(msg)} WHERE TIME = {time}")
                # 提交
            conn.commit()
        print("解码完成")
    cur.close()
    conn.close()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python index.py [db_path]")
        sys.exit(1)
    db_path = sys.argv[1]
    run(db_path)
