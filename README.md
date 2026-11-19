<picture>
  <source media="(prefers-color-scheme: dark)" srcset="./assets/card-dark.svg">
  <img src="./assets/card-light.svg" width="100%" alt="natsuki@sonar — Fengsheng Xia: Computer Science @ Monash University '28. Agents, Tool Use, MCP, RAG. 65 PRs opened, 15 merged upstream." />
</picture>

### Hi, I'm Fengsheng (Natsuki).

I build agents that do the boring part of being online for you.
CS undergrad at **Monash University** ('28). Most of my time goes into two things:
an always-on price agent I actually depend on, and fixing bugs in the agent frameworks I learn from.

## What I'm building

**Sonar** · a cross-marketplace price agent for Japan's second-hand market

Watches **6 marketplaces** (Mercari, Suruga-ya, Yahoo! Auctions, PayPay Flea Market, Rakuma, BOOK OFF) around the clock,
finds *the exact item* in hand-written, code-less listing titles, and pushes a good price to my phone within seconds.
**470k+ price events** logged so far, running unattended on a server overseas.

- **Tool-Use agent:** one sentence like *"watch the PS4 edition for me, under ¥5,000"* becomes a plan: resolve the title, locate it in the catalog, read the market, propose a price cap, ask me, add the watch.
- **Human-in-the-loop by design:** anything that writes waits for a yes; a "no" goes back to the model so it can re-plan.
- **MCP server:** the same tool table is exposed over MCP, so Claude Code can drive Sonar directly.
- **Matching that earns its keep:** recall and precision are split into two keywords; keywords self-calibrate against real seller titles; a grey zone keeps near-misses visible instead of silently dropping them.

`Python` `FastAPI` `SQLite` `DeepSeek function calling` `MCP` `Playwright` `pytest` · 400+ commits · 39 test modules · source private for now, demo on request

## Merged upstream

Bugs I found, reproduced and fixed in other people's agent / RAG infrastructure.

| Project | What I fixed | PRs |
|:--|:--|:--|
| **[agentscope-ai/agentscope](https://github.com/agentscope-ai/agentscope)** | RAG metadata filters wrongly matching `None` on stores that can't match null | [#4058](https://github.com/agentscope-ai/agentscope/pull/4058) |
| **[agentscope-ai/OpenJudge](https://github.com/agentscope-ai/OpenJudge)** | ActionLoop signatures for dict / nested arguments; graders tripping on empty substrings | [#245](https://github.com/agentscope-ai/OpenJudge/pull/245) [#244](https://github.com/agentscope-ai/OpenJudge/pull/244) |
| **[agentscope-ai/ReMe](https://github.com/agentscope-ai/ReMe)** | IPv6 hosts in startup URLs | [#753](https://github.com/agentscope-ai/ReMe/pull/753) |
| **[Tencent/WeKnora](https://github.com/Tencent/WeKnora)** | unset MCP tool-selection mode exposing *all* tools; context leaking into saved knowledge; missing auth header on document parsing | [#5450](https://github.com/Tencent/WeKnora/pull/5450) [#5119](https://github.com/Tencent/WeKnora/pull/5119) [#5057](https://github.com/Tencent/WeKnora/pull/5057) |
| **[Tencent/AI-Infra-Guard](https://github.com/Tencent/AI-Infra-Guard)** | agent-scan severity lost for CVSS scores and Chinese levels; skill-scan finish-tool casing; a data race in the logger; a racy test | [#777](https://github.com/Tencent/AI-Infra-Guard/pull/777) [#776](https://github.com/Tencent/AI-Infra-Guard/pull/776) [#765](https://github.com/Tencent/AI-Infra-Guard/pull/765) [#772](https://github.com/Tencent/AI-Infra-Guard/pull/772) |
| **[pydantic/logfire](https://github.com/pydantic/logfire)** | generator messages consumed early under Anthropic instrumentation | [#2714](https://github.com/pydantic/logfire/pull/2714) |
| **[langgenius/dify](https://github.com/langgenius/dify)** | test cleanup | [#44837](https://github.com/langgenius/dify/pull/44837) |
| **[OpenSandbox](https://github.com/opensandbox-group/OpenSandbox)** | tests mutating global state (`time.Local`, gin mode) | [#2885](https://github.com/opensandbox-group/OpenSandbox/pull/2885) [#2842](https://github.com/opensandbox-group/OpenSandbox/pull/2842) |

<sub>[all of them →](https://github.com/search?q=author%3Afxia0018+is%3Apr+is%3Amerged&type=pullrequests)</sub>

## Toolbox

<img src="https://skillicons.dev/icons?i=py,go,ts,fastapi,sqlite,swift,linux,git,vscode&theme=dark" height="40" alt="Python, Go, TypeScript, FastAPI, SQLite, Swift, Linux, Git, VS Code" />

---

<a href="https://www.linkedin.com/in/fengsheng-xia-2a30403b8"><img src="https://img.shields.io/badge/LinkedIn-Fengsheng%20Xia-0A66C2?style=flat-square&logo=linkedin&logoColor=white" alt="LinkedIn" /></a>
<a href="mailto:fxia0018@student.monash.edu"><img src="https://img.shields.io/badge/email-fxia0018%40student.monash.edu-24292f?style=flat-square&logo=gmail&logoColor=white" alt="Email" /></a>

<sub>I wrote an agent so I'd stop refreshing Mercari. Now I refresh its logs instead.</sub>
