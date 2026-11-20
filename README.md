<picture>
  <source media="(prefers-color-scheme: dark)" srcset="./assets/card-dark.svg">
  <img src="./assets/card-light.svg" width="100%" alt="natsuki — CS @ Monash '28, agents, MCP, RAG. 69 PRs opened, 20 merged upstream." />
</picture>

## Projects

**[furima-mcp](https://github.com/fxia0018/furima-mcp)** · MCP server for Japan's second-hand marketplaces. Searches Mercari, Yahoo! Auctions, Yahoo! Flea Market and Rakuma in one call, prices items against what actually sold (split by condition), and watches searches for new listings. Python, on [PyPI](https://pypi.org/project/furima-mcp/) and the official MCP Registry.

## Merged upstream

Bugs I found, reproduced and fixed in other people's agent / RAG infrastructure. Updated daily.

<!-- merged:start -->
| Project | What I fixed |
|:--|:--|
| **[langgenius/dify](https://github.com/langgenius/dify)**<br><sub>★ 162k</sub> | [#44837](https://github.com/langgenius/dify/pull/44837) clean away unnecessary \_\_new\_\_ in tests |
| **[Tencent/WeKnora](https://github.com/Tencent/WeKnora)**<br><sub>★ 38k</sub> | [#5450](https://github.com/Tencent/WeKnora/pull/5450) treat an unset MCP selection mode as none, not all<br>[#5119](https://github.com/Tencent/WeKnora/pull/5119) strip host context from getUserQuery for save-to-knowledge-base<br>[#5057](https://github.com/Tencent/WeKnora/pull/5057) send Authorization header on legacy MinerU /file\_parse and /docs probes |
| **[agentscope-ai/agentscope](https://github.com/agentscope-ai/agentscope)**<br><sub>★ 36k</sub> | [#4058](https://github.com/agentscope-ai/agentscope/pull/4058) reject None metadata\_filter values on stores that cannot match null |
| **[opensandbox-group/OpenSandbox](https://github.com/opensandbox-group/OpenSandbox)**<br><sub>★ 18k</sub> | [#2885](https://github.com/opensandbox-group/OpenSandbox/pull/2885) stop snapshot template tests from writing time.Local<br>[#2842](https://github.com/opensandbox-group/OpenSandbox/pull/2842) set gin test mode once for controller tests |
| **[Tencent/AI-Infra-Guard](https://github.com/Tencent/AI-Infra-Guard)**<br><sub>★ 7.6k</sub> | [#783](https://github.com/Tencent/AI-Infra-Guard/pull/783) make GitClone retries work after a timeout<br>[#782](https://github.com/Tencent/AI-Infra-Guard/pull/782) keep files extracted from .tgz targets readable<br>[#781](https://github.com/Tencent/AI-Infra-Guard/pull/781) close each extracted zip entry before the next<br>[#777](https://github.com/Tencent/AI-Infra-Guard/pull/777) keep severity of CVSS-score and Chinese finding levels<br>[#776](https://github.com/Tencent/AI-Infra-Guard/pull/776) honor finish tool name casing<br>[#772](https://github.com/Tencent/AI-Infra-Guard/pull/772) lock the callback slice in TestRunner\_Callback\_Invoked<br>[#765](https://github.com/Tencent/AI-Infra-Guard/pull/765) stop writing a package global on every log call |
| **[pydantic/logfire](https://github.com/pydantic/logfire)**<br><sub>★ 4.6k</sub> | [#2714](https://github.com/pydantic/logfire/pull/2714) materialize generator messages in instrument\_anthropic |
| **[agentscope-ai/ReMe](https://github.com/agentscope-ai/ReMe)**<br><sub>★ 3.8k</sub> | [#753](https://github.com/agentscope-ai/ReMe/pull/753) bracket IPv6 hosts in startup banner URLs |
| **[agentscope-ai/OpenJudge](https://github.com/agentscope-ai/OpenJudge)**<br><sub>★ 1.1k</sub> | [#251](https://github.com/agentscope-ai/OpenJudge/pull/251) preserve tool call accuracy raw score before bounding<br>[#250](https://github.com/agentscope-ai/OpenJudge/pull/250) keep texts shorter than n in n-gram Jaccard<br>[#245](https://github.com/agentscope-ai/OpenJudge/pull/245) build ActionLoop signatures from dict and nested arguments<br>[#244](https://github.com/agentscope-ai/OpenJudge/pull/244) ignore empty entries in contains\_all/contains\_any substrings |
<!-- merged:end -->

<sub>[all of them →](https://github.com/search?q=author%3Afxia0018+is%3Apr+is%3Amerged&type=pullrequests)</sub>

<a href="mailto:fxia0018@student.monash.edu"><img src="https://img.shields.io/badge/email-fxia0018%40student.monash.edu-24292f?style=flat-square&logo=gmail&logoColor=white" alt="Email" /></a>
