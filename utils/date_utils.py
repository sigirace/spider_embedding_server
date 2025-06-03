from datetime import datetime
import re


def parse_pdf_date(date_str: str) -> str:
    if not date_str or not date_str.startswith("D:"):
        return date_str  # 파싱 불가능한 경우 원본 반환

    date_str = date_str[2:]  # "D:" 제거

    # 타임존 제거 후 파싱
    match = re.match(r"(\d{14})(Z|[+-]\d{2}'\d{2}')?", date_str)
    if not match:
        return date_str

    dt_str, tz = match.groups()

    try:
        dt = datetime.strptime(dt_str, "%Y%m%d%H%M%S")
        return dt.strftime("%Y-%m-%d %H:%M:%S")
    except Exception:
        return date_str
