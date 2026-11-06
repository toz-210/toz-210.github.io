---
layout: page
title: 공모전/자격증
icon: fas fa-trophy
order: 6
---

{%- assign posts = site.categories["공모전/자격증"] -%}
{%- if posts and posts.size > 0 %}
{% for p in posts %}
- [{{ p.title }}]({{ p.url | relative_url }}) <small>{{ p.date | date: "%Y.%m.%d" }}</small>
{%- endfor %}
{% else %}
준비 중
{% endif %}

관련 저장소: [Contests-Certifications](https://github.com/toz-210/Contests-Certifications)
