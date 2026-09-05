"""
真实天气客户端,基于 wttr.in(免 key)
优先用 j1 JSON 拿到结构化字段,失败回退 format=3 简短文本
"""
import requests
from utils.config_handler import weather_conf
from utils.logger_handler import logger


CITY_ZH_TO_EN = {
    "北京": "Beijing", "上海": "Shanghai", "广州": "Guangzhou", "深圳": "Shenzhen",
    "杭州": "Hangzhou", "南京": "Nanjing", "苏州": "Suzhou", "成都": "Chengdu",
    "重庆": "Chongqing", "武汉": "Wuhan", "西安": "Xian", "天津": "Tianjin",
    "长沙": "Changsha", "青岛": "Qingdao", "厦门": "Xiamen", "宁波": "Ningbo",
    "合肥": "Hefei", "福州": "Fuzhou", "济南": "Jinan", "郑州": "Zhengzhou",
    "昆明": "Kunming", "兰州": "Lanzhou", "贵阳": "Guiyang", "南宁": "Nanning",
    "海口": "Haikou", "三亚": "Sanya", "南昌": "Nanchang", "石家庄": "Shijiazhuang",
    "太原": "Taiyuan", "沈阳": "Shenyang", "大连": "Dalian", "哈尔滨": "Harbin",
    "长春": "Changchun", "乌鲁木齐": "Urumqi", "拉萨": "Lhasa", "银川": "Yinchuan",
    "西宁": "Xining", "呼和浩特": "Hohhot", "香港": "Hong Kong", "澳门": "Macau",
    "台北": "Taipei", "无锡": "Wuxi", "佛山": "Foshan", "东莞": "Dongguan",
    "珠海": "Zhuhai", "温州": "Wenzhou", "烟台": "Yantai", "泉州": "Quanzhou",
}


def _normalize_city(city: str) -> str:
    city = (city or "").strip()
    if not city:
        return city
    if any("一" <= ch <= "鿿" for ch in city):
        return CITY_ZH_TO_EN.get(city, city)
    return city


def _format_from_j1(data: dict) -> str:
    current = data["current_condition"][0]
    area = data.get("nearest_area", [{}])[0]
    area_name = (area.get("areaName", [{}])[0] or {}).get("value", "")
    desc = current["weatherDesc"][0]["value"]
    temp_c = current["temp_C"]
    feels_c = current["FeelsLikeC"]
    humidity = current["humidity"]
    wind = current["windspeedKmph"]
    wind_dir = current["winddir16Point"]
    visibility = current["visibility"]
    desc_line = f"{area_name}当前天气:{desc}" if area_name else f"当前天气:{desc}"
    return (
        f"{desc_line},气温{temp_c}摄氏度(体感{feels_c}摄氏度),"
        f"空气湿度{humidity}%,{wind_dir}风{wind}公里/小时,"
        f"能见度{visibility}公里"
    )


def _format_from_short(text: str) -> str:
    return f"当前天气:{text.strip()}"


def _fetch_j1(city_en: str) -> str:
    url = f"{weather_conf['base_url']}/{city_en}"
    params = {"format": weather_conf["format"], "lang": weather_conf["language"]}
    headers = {"User-Agent": weather_conf["user_agent"]}
    resp = requests.get(url, params=params, headers=headers, timeout=weather_conf["timeout"])
    resp.raise_for_status()
    return _format_from_j1(resp.json())


def _fetch_short(city_en: str) -> str:
    url = f"{weather_conf['base_url']}/{city_en}"
    params = {"format": "3", "lang": weather_conf["language"]}
    headers = {"User-Agent": weather_conf["user_agent"]}
    resp = requests.get(url, params=params, headers=headers, timeout=weather_conf["timeout"])
    resp.raise_for_status()
    return _format_from_short(resp.text)


def fetch_weather(city: str) -> str:
    """
    获取城市实时天气,返回中文描述字符串
    失败时返回友好提示,不抛异常
    """
    city_en = _normalize_city(city)
    if not city_en:
        return f"暂时无法获取天气:城市名为空"

    for fetcher in (_fetch_j1, _fetch_short):
        try:
            text = fetcher(city_en)
            logger.info("[weather_client]成功获取%s(%s)天气:%s", city, city_en, text[:30])
            return text
        except Exception as e:
            logger.warning("[weather_client]%s 获取%s天气失败:%s", fetcher.__name__, city, e)
            continue

    return f"暂时无法获取{city}的天气,稍后再试或换个城市"


if __name__ == '__main__':
    print(fetch_weather("深圳"))
