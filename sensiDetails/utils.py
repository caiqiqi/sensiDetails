#coding=utf-8
import socket

def is_valid_url(p_url):
    # 去除掉url中存在的个人页
    u = "/display/~"
    return (not u in p_url)

def is_valid_details(p_details):
    # 去除掉pdf文档中的默认信息
    d = "your content that should be excluded"
    return (not d in p_details)

def filter_highlight(p_details):
    for i in ["@@@hl@@@", "@@@endhl@@@"]:
	p_details = p_details.replace(i, "")
    return p_details

def get_host_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()

    return ip
