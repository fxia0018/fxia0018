<picture>
  <source media="(prefers-color-scheme: dark)" srcset="./assets/card-dark.svg">
  <img src="./assets/card-light.svg" width="100%" alt="natsuki@sonar — Natsuki: Computer Science @ Monash University '28. Agents, Tool Use, MCP, RAG. 67 PRs opened, 15 merged upstream." />
</picture>

### Hi, I'm Natsuki.

CS @ Monash ('28). I build agents, and fix bugs in the agent frameworks I learn from.

## What I'm building

**Sonar**: a price agent that watches 6 Japanese second-hand marketplaces around the clock and
pings my phone when the exact item I want shows up at a good price. 470k+ price events so far.

- **Tool use:** *"watch the PS4 edition, under ¥5,000"* → finds the item, reads the market, proposes a cap, adds the watch
- **Human-in-the-loop:** anything that writes waits for my yes
- **MCP server:** Claude Code can drive it directly

`Python` `FastAPI` `SQLite` `MCP` `Playwright` · private for now, demo on request

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

**Recently merged** <sub>(updated daily)</sub>

<!-- RECENT_MERGED:START -->
- `2026-11-19` **Tencent/AI-Infra-Guard** · [fix(agent-scan): keep severity of CVSS-score and Chinese finding levels](https://github.com/Tencent/AI-Infra-Guard/pull/777)
- `2026-11-19` **Tencent/AI-Infra-Guard** · [fix(skill-scan): honor finish tool name casing](https://github.com/Tencent/AI-Infra-Guard/pull/776)
- `2026-11-18` **agentscope-ai/agentscope** · [fix(rag): reject None metadata_filter values on stores that cannot match null](https://github.com/agentscope-ai/agentscope/pull/4058)
- `2026-11-18` **agentscope-ai/ReMe** · [fix(logo): bracket IPv6 hosts in startup banner URLs](https://github.com/agentscope-ai/ReMe/pull/753)
- `2026-11-18` **agentscope-ai/OpenJudge** · [fix(agent): build ActionLoop signatures from dict and nested arguments](https://github.com/agentscope-ai/OpenJudge/pull/245)
- `2026-11-18` **agentscope-ai/OpenJudge** · [fix(graders): ignore empty entries in contains_all/contains_any substrings](https://github.com/agentscope-ai/OpenJudge/pull/244)
<!-- RECENT_MERGED:END -->

<sub>[all of them →](https://github.com/search?q=author%3Afxia0018+is%3Apr+is%3Amerged&type=pullrequests)</sub>

## Toolbox

<img src="https://skillicons.dev/icons?i=py,go,ts,fastapi,sqlite,swift,linux,git,vscode&theme=dark" height="40" alt="Python, Go, TypeScript, FastAPI, SQLite, Swift, Linux, Git, VS Code" />

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/fxia0018/fxia0018/output/github-snake-dark.svg">
  <img src="https://raw.githubusercontent.com/fxia0018/fxia0018/output/github-snake.svg" width="100%" alt="Contribution graph eaten by a snake" />
</picture>

---

<a href="mailto:fxia0018@student.monash.edu"><img src="https://img.shields.io/badge/email-fxia0018%40student.monash.edu-24292f?style=flat-square&logo=gmail&logoColor=white" alt="Email" /></a>

<sub>I wrote an agent so I'd stop refreshing Mercari. Now I refresh its logs instead.</sub>
