# cn-calendar-skill

> 中国日历全栈工具包 — AI Agent Skill · 13 个端点 · 自包含零外部 API · 国务院数据 2004-2026

一个自包含的 Skill 文件，把"判断这天是否上班/请假能连出多长假期/农历日期/节气"这些**每个中国开发者都遇到过**的日历问题，封装成 AI 编程助手直接能调用的工具集。

> 兼容 [Claude Code](https://github.com/anthropics/claude-code) · [Codex](https://github.com/openai/codex) · [Hermes Agent](https://github.com/NousResearch/hermes-agent) · OpenClaw · 任何支持 SKILL.md 的 Agent
>
> Skill 文件本质是结构化 Markdown + 内嵌 Python，任何支持上下文注入的 AI 编程助手都能用。

---

## 痛点

写一个"判断下周一是不是工作日"的脚本，国内开发者要么：
- ❌ 硬编码节假日（每年要更新，调休班/补班容易漏）
- ❌ 调外部 API（被限频/掉线/收费）
- ❌ 自己爬国务院通知（费时费力且不稳定）

这个 Skill 把数据 + 代码全部内嵌，**完全离线，零 API Key，零网络请求**。

---

## 13 个端点能力清单

### 日历层
| 端点 | 用途 |
|------|------|
| `is_workday_cn(date)` | 判断是否工作日（含国务院调休补班） |
| `next_holiday(date)` | 下一个法定节假日 + 完整起止日期 |

### 工作日层
| 端点 | 用途 |
|------|------|
| `add_workdays(start, n)` | 第 N 个工作日是哪天（账期/物流时效） |
| `count_workdays(start, end)` | 区间内工作日数（HR考勤/排班） |
| `find_bridge_leaves(date, n)` | 请 N 天假能连出多长假期（性价比排序） |

### 农历层
| 端点 | 用途 |
|------|------|
| `solar_to_lunar(date)` | 公历转农历 |
| `lunar_to_solar(year, month, day)` | 农历转公历（春节/中秋/七夕等传统节日） |

### 节气层
| 端点 | 用途 |
|------|------|
| `get_solar_term(date)` | 当前所属节气 + 下一个节气 + 距离天数 |

### 生肖星座
| 端点 | 用途 |
|------|------|
| `get_zodiac(year)` | 公历年的生肖 |
| `get_zodiac_strict(date)` | 严格按农历年的生肖 |
| `get_constellation(date)` | 12 星座 |

### 综合
| 端点 | 用途 |
|------|------|
| `cn_date_info(date)` | 一次返回某天所有信息 |

---

## 快速开始

**3 步，2 分钟。**

```bash
# 1. 创建 skill 目录
mkdir -p ~/.claude/skills/cn-calendar

# 2. 把 SKILL.md 放进去
curl -o ~/.claude/skills/cn-calendar/SKILL.md \
  https://raw.githubusercontent.com/demo112/cn-calendar-skill/main/SKILL.md

# 3. 安装依赖
pip install chinese-calendar zhdate
```

启动 Claude Code，说一句「6月份有几个工作日，端午是几号？」，自动激活。

> **Codex / Hermes Agent / OpenClaw 用户：** 把 SKILL.md 的内容贴入你的系统 prompt 或项目上下文文件即可，内嵌的 Python 代码可直接执行。

---

## 真实使用场景

| 场景 | 一句话激活 |
|------|------|
| 📋 HR 考勤 | "6月份本部门排班，告诉我6月有多少工作日，端午是几号到几号" |
| 🛒 电商大促 | "今年中秋是哪天？双十一前一周有调休吗？" |
| 💰 财务账期 | "客户合同写'付款日为开票后30个工作日'，今天开票，到期日是哪天？" |
| 🏖️ 请假规划 | "我想5月底请2天假，怎么请最划算？" |
| 📦 物流时效 | "今天下单，承诺5个工作日送达，预计哪天到？" |
| 🎂 农历提醒 | "我妈生日是农历八月初八，今年公历是哪天？" |
| 🍂 节气营销 | "立秋是什么时候？秋季养生套餐推广" |

---

## 数据来源 & 范围

- **法定节假日**：基于 [LKI/chinese-calendar](https://github.com/LKI/chinese-calendar)，**国务院办公厅**官方通知
  - 覆盖：2004-01-01 至 2026-12-31
  - 包含：调休补班 / 法定假日 / 周末普通休
- **农历**：基于 [CutePandaSh/zhdate](https://github.com/CutePandaSh/zhdate)
  - 覆盖：1900-2100
- **二十四节气**：天文公式，21 世纪精度 ±1 天

---

## Donate

如果这个工具帮到你的工作流，欢迎支持作者持续更新 ☕

- ETH/USDT (ERC-20): `0xddD9f45e14c92846f47C1c1A4431aC2b41D87273`
- 微信赞赏码：（待补充）
- 想要新端点？开 [Issue](https://github.com/demo112/cn-calendar-skill/issues) 提需求

---

## License

MIT © 2026 云渡 (Hermes Agent) · maintained by Cooper

---

## Roadmap

- [x] V1.0: 13 个核心端点
- [ ] V1.1: 黄历宜忌（择日）
- [ ] V1.2: 国际节假日（美/日/港台）
- [ ] V2.0: TypeScript 版本
