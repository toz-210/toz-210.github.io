---
layout: page
title: CTF/Wargame
icon: fas fa-flag
order: 2
---

{%- assign posts = site.categories["CTF/Wargame"] -%}
{%- if posts and posts.size > 0 %}
{% for p in posts %}
- [{{ p.title }}]({{ p.url | relative_url }}) <small>{{ p.date | date: "%Y.%m.%d" }}</small>
{%- endfor %}
{% else %}
준비 중
{% endif %}

관련 저장소: [CTF-Wargame](https://github.com/toz-210/CTF-Wargame)
