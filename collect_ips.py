import requests
from bs4 import BeautifulSoup
import re

# 默认过滤速度
default_filter_speed = 3

# 正则表达式用于匹配IP地址
ip_pattern = r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}"
speed_pattern = r"[0-9]+\.[0-9]+[Mm][Bb]/s"


def str_to_num(s, default=0) -> int:
    try:
        return int(s)  # 如果需要整数，可以用 int(s)
    except ValueError:
        return default


def get_url(url, op, ulist):
    element_text = ""

    # 发送HTTP请求获取网页内容
    response = requests.get(url)
    # 使用BeautifulSoup解析HTML
    soup = BeautifulSoup(response.text, "html.parser")
    # 找到包含IP地址的元素
    elements = soup.find_all("tr")
    # 遍历所有元素,查找IP地址
    for element in elements:

        if op == 1:
            element_text = element.get_text()
        elif op == 2:
            element_text = element.__str__()

        speed_matches = re.findall(speed_pattern, element_text)

        if (
            len(speed_matches) == 0
            or str_to_num(speed_matches[0].split(".")[0]) < default_filter_speed
        ):
            continue

        ip_matches = re.findall(ip_pattern, element_text)
        # 如果找到IP地址,则写入 list
        for ip in ip_matches:
            ip = ip + "#" + ip + "_" + speed_matches[0]
            ulist.append(ip)


if __name__ == "__main__":
    ip_list = []

    get_url("http://ip.164746.xyz", 1, ip_list)

    # ip 去重
    ip_list_unique = list(dict.fromkeys(ip_list))

    if len(ip_list_unique):
        # 创建一个文件来存储IP地址
        with open("ip.txt", "w") as file:

            file.write("\n".join(ip_list_unique) + "\n")
