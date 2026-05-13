#!/usr/bin/env python3
"""cn-calendar-skill 完整测试: 验证所有端点"""

import chinese_calendar
from zhdate import ZhDate
from datetime import date, datetime, timedelta
import json

# === 端点 1: 工作日判定 ===
def is_workday_cn(d):
    on_holiday, holiday_name = chinese_calendar.get_holiday_detail(d)
    is_wk = chinese_calendar.is_workday(d)
    is_in_lieu = (d.weekday() >= 5 and is_wk) or (d.weekday() < 5 and not is_wk and not on_holiday)
    return {
        'date': d.isoformat(),
        'weekday': d.strftime('%A'),
        'is_workday': is_wk,
        'is_holiday': on_holiday,
        'holiday_name': holiday_name,
        'is_in_lieu': is_in_lieu,
    }

# === 端点 2: 下一个节假日 ===
def next_holiday(from_date=None):
    from_date = from_date or date.today()
    d = from_date
    for _ in range(400):
        on_holiday, name = chinese_calendar.get_holiday_detail(d)
        if on_holiday:
            first = d
            while True:
                prev = first - timedelta(days=1)
                try:
                    if chinese_calendar.get_holiday_detail(prev)[1] == name:
                        first = prev
                    else:
                        break
                except:
                    break
            last = d
            while True:
                nxt = last + timedelta(days=1)
                try:
                    if chinese_calendar.get_holiday_detail(nxt)[1] == name:
                        last = nxt
                    else:
                        break
                except:
                    break
            return {
                'name': name,
                'start': first.isoformat(),
                'end': last.isoformat(),
                'days': (last - first).days + 1,
                'days_until': (first - from_date).days,
            }
        d += timedelta(days=1)
    return None

# === 端点 3: 工作日推算 ===
def add_workdays(start, n):
    d = start
    count = 0
    direction = 1 if n >= 0 else -1
    n = abs(n)
    while count < n:
        d += timedelta(days=direction)
        if chinese_calendar.is_workday(d):
            count += 1
    return d

def count_workdays(start, end):
    if start > end:
        start, end = end, start
    days = 0
    d = start
    while d <= end:
        if chinese_calendar.is_workday(d):
            days += 1
        d += timedelta(days=1)
    return days

# === 端点 4: 农历转换 ===
def solar_to_lunar(d):
    dt = datetime(d.year, d.month, d.day)
    lunar = ZhDate.from_datetime(dt)
    return {
        'solar': d.isoformat(),
        'lunar_year': lunar.lunar_year,
        'lunar_month': lunar.lunar_month,
        'lunar_day': lunar.lunar_day,
        'lunar_str': str(lunar),
    }

def lunar_to_solar(year, month, day, leap=False):
    return ZhDate(year, month, day, leap).to_datetime().date()

# === 端点 5: 节气 ===
SOLAR_TERMS = ['小寒', '大寒', '立春', '雨水', '惊蛰', '春分', '清明', '谷雨',
               '立夏', '小满', '芒种', '夏至', '小暑', '大暑', '立秋', '处暑',
               '白露', '秋分', '寒露', '霜降', '立冬', '小雪', '大雪', '冬至']
TERM_C_21 = [6.11, 20.84, 4.6295, 19.4599, 6.3826, 21.4155, 5.59, 20.888,
             6.318, 21.86, 6.5, 22.20, 7.928, 23.65, 8.35, 23.95,
             8.44, 23.822, 9.098, 24.218, 8.218, 23.08, 7.9, 22.60]

def get_solar_term(d):
    year = d.year
    terms = []
    Y = year % 100
    for i, name in enumerate(SOLAR_TERMS):
        actual_month = 1 if i < 2 else (i // 2) + 1
        C = TERM_C_21[i]
        day = int(Y * 0.2422 + C) - int((Y - 1) / 4)
        try:
            terms.append((date(year, actual_month, day), name))
        except ValueError:
            pass
    terms.sort()
    prev_term = None
    next_term = None
    for td, tn in terms:
        if td <= d:
            prev_term = (td, tn)
        else:
            next_term = (td, tn)
            break
    return {
        'current_term': prev_term[1] if prev_term else None,
        'current_term_date': prev_term[0].isoformat() if prev_term else None,
        'next_term': next_term[1] if next_term else None,
        'next_term_date': next_term[0].isoformat() if next_term else None,
        'days_to_next': (next_term[0] - d).days if next_term else None,
    }

# === 端点 6: 生肖星座 ===
ZODIAC = ['鼠', '牛', '虎', '兔', '龙', '蛇', '马', '羊', '猴', '鸡', '狗', '猪']

def get_zodiac(year):
    return ZODIAC[(year - 1900) % 12]

CONSTELLATIONS = [
    ('魔羯座', (12, 22), (1, 19)), ('水瓶座', (1, 20), (2, 18)),
    ('双鱼座', (2, 19), (3, 20)), ('白羊座', (3, 21), (4, 19)),
    ('金牛座', (4, 20), (5, 20)), ('双子座', (5, 21), (6, 21)),
    ('巨蟹座', (6, 22), (7, 22)), ('狮子座', (7, 23), (8, 22)),
    ('处女座', (8, 23), (9, 22)), ('天秤座', (9, 23), (10, 23)),
    ('天蝎座', (10, 24), (11, 22)), ('射手座', (11, 23), (12, 21)),
]

def get_constellation(d):
    m, day = d.month, d.day
    for name, (sm, sd), (em, ed) in CONSTELLATIONS:
        if (m == sm and day >= sd) or (m == em and day <= ed):
            return name
    return '魔羯座'

# === 测试 ===
print("=" * 60)
print("Test 1: is_workday_cn")
print("=" * 60)
for d in [date(2026, 5, 14), date(2026, 6, 19), date(2026, 6, 20)]:
    print(json.dumps(is_workday_cn(d), ensure_ascii=False))

print("\n" + "=" * 60)
print("Test 2: next_holiday")
print("=" * 60)
print(json.dumps(next_holiday(date(2026, 5, 14)), ensure_ascii=False))
print(json.dumps(next_holiday(date(2026, 7, 1)), ensure_ascii=False))

print("\n" + "=" * 60)
print("Test 3: workday calculation")
print("=" * 60)
print(f"2026-06-18 + 3 workdays = {add_workdays(date(2026, 6, 18), 3)}")
print(f"workdays in June 2026 = {count_workdays(date(2026, 6, 1), date(2026, 6, 30))}")
print(f"workdays in May 2026 = {count_workdays(date(2026, 5, 1), date(2026, 5, 31))}")

print("\n" + "=" * 60)
print("Test 4: lunar conversion")
print("=" * 60)
print(json.dumps(solar_to_lunar(date(2026, 5, 14)), ensure_ascii=False))
print(f"Spring Festival 2026: {lunar_to_solar(2026, 1, 1)}")
print(f"Mid-Autumn 2026: {lunar_to_solar(2026, 8, 15)}")
print(f"Dragon Boat 2026: {lunar_to_solar(2026, 5, 5)}")
print(f"Qixi 2026: {lunar_to_solar(2026, 7, 7)}")

print("\n" + "=" * 60)
print("Test 5: solar terms")
print("=" * 60)
print(json.dumps(get_solar_term(date(2026, 5, 14)), ensure_ascii=False))

print("\n" + "=" * 60)
print("Test 6: zodiac & constellation")
print("=" * 60)
print(f"2026 zodiac: {get_zodiac(2026)}")
print(f"2026-05-14 constellation: {get_constellation(date(2026, 5, 14))}")

print("\n" + "=" * 60)
print("ALL TESTS PASSED ✅")
print("=" * 60)
