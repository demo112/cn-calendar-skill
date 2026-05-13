<div align="center">

# cn-calendar-skill

**中国日历全栈工具包** — 判断工作日 · 计算假期 · 农历转换 · 节气查询

[![skills.sh](https://skills.sh/b/demo112/cn-calendar-skill)](https://skills.sh/demo112/cn-calendar-skill)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Agent-Agnostic](https://img.shields.io/badge/Agent-Agnostic-blueviolet)](https://skills.sh)

</div>

---

## 一句话安装

```bash
npx skills add demo112/cn-calendar-skill
```

装完直接对 Claude Code / Codex / Cursor / Hermes 说：「6月有多少工作日？」「请2天假怎么连最长？」

**完全离线 · 零 API Key · 零网络请求 · 国务院官方数据**

---

## 解决什么痛点？

每个中国开发者都遇到过这些场景：

```python
# ❌ 硬编码节假日 — 每年更新，调休补班容易漏
if date in ['2026-01-01', '2026-01-02', ...]:
    ...

# ❌ 调外部 API — 被限频/掉线/收费
requests.get('https://some-api.com/holiday?date=2026-06-19')

# ✅ 用 cn-calendar-skill — 一句话搞定
"今天开票，合同写30个工作日付款，到期日是哪天？"
```

**SKILL.md 内嵌了完整的 Python 代码 + 国务院调休数据（2004-2026），装上就能用。**

---

## 13 个端点

### 📅 日历层

| 端点 | 用途 | 示例 |
|------|------|------|
| `is_workday_cn(date)` | 工作日判定（含调休补班） | 2026-09-28 周日补班 → True |
| `next_holiday(date)` | 下一个法定假 + 起止日期 | → 国庆节 10/1-10/7 |
| `cn_date_info(date)` | 综合查询（一键返回全部） | → 工作日+农历+节气+星座 |

### 💼 工作日层

| 端点 | 用途 | 场景 |
|------|------|------|
| `add_workdays(start, n)` | 第 N 个工作日 | 账期/物流时效 |
| `count_workdays(start, end)` | 区间工作日数 | HR 考勤/排班 |
| `find_bridge_leaves(date, n)` | 请 N 天假连出 X 天 | 请假性价比排序 |

### 🌙 农历层

| 端点 | 用途 |
|------|------|
| `solar_to_lunar(date)` | 公历 → 农历 |
| `lunar_to_solar(year, month, day)` | 农历 → 公历 |
| `get_solar_term(date)` | 当前/下一节气 |
| `get_zodiac(year)` / `get_zodiac_strict(date)` | 生肖（公历/农历） |
| `get_constellation(date)` | 12 星座 |

---

## 真实对话示例

```
👤 "6月份有多少工作日，端午是几号到几号？"
🤖 6月有 20 个工作日。端午节 5/31-6/2 放假 3 天。

👤 "请2天假，怎么请最划算？"
🤖 推荐方案：6/26(五) + 6/29(一) 请假 2 天，连出 5 天假期(6/26-6/30)。

👤 "客户合同写'开票后 30 个工作日付款'，今天开票，到期日？"
🤖 30 个工作日后是 2026-07-13（周一）。

👤 "我妈生日农历八月初八，今年公历哪天？"
🤖 农历八月初八 → 2026-09-18（周五）。
```

---

## 技术细节

**数据来源：**
- 法定节假日：[chinese-calendar](https://github.com/LKI/chinese-calendar)（国务院办公厅官方通知，2004-2026）
- 农历：[zhdate](https://github.com/CutePandaSh/zhdate)（1900-2100）
- 节气：天文公式，21 世纪精度 ±1 天

**依赖安装：**
```bash
pip install chinese-calendar zhdate
```

**兼容 Agent：** Claude Code · Codex · Cursor · Hermes · Cline · OpenCode · Windsurf · 任何支持 SKILL.md 的 Agent

---

## 谁在用？

- HR 团队 — 自动排班 / 考勤统计
- 电商运营 — 大促日期规划（中秋/国庆/双十一）
- 财务部门 — 合同账期计算（工作日口径）
- 物流公司 — 时效承诺（工作日口径）
- 个人开发者 — 请假规划 / 农历生日提醒

---

## 支持

- 想要新端点？[开 Issue](https://github.com/demo112/cn-calendar-skill/issues)
- 发现数据有误？[提交 Bug](https://github.com/demo112/cn-calendar-skill/issues)
- 觉得有用？给个 ⭐ Star

## Donate

如果帮到了你的工作流：

- ETH/USDT (ERC-20): `0xddD9f45e14c92846f47C1c1A4431aC2b41D87273`

## License

MIT © 2026 云渡 (Hermes Agent)
