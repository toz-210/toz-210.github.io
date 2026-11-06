---
layout: page
title: Categories
icon: fas fa-stream
order: 1
---

{%- assign cats = "dev|개발|fas fa-code,ctf-wargame|CTF/Wargame|fas fa-flag,bug-bounty|Bug Bounty|fas fa-bug,tech-doc|블로그/기술문서|fas fa-book,paper-conference|논문/컨퍼런스|fas fa-file-lines,contest-cert|공모전/자격증|fas fa-trophy" | split: "," -%}

<ul class="list-unstyled">
{%- for c in cats -%}
  {%- assign f = c | split: "|" -%}
  {%- assign n = site.categories[f[1]] | size %}
  <li class="py-2">
    <i class="{{ f[2] }} fa-fw me-2"></i>
    <a href="{{ '/category/' | append: f[0] | append: '/' | relative_url }}">{{ f[1] }}</a>
    <small class="text-muted ms-1">{{ n }}</small>
  </li>
{%- endfor %}
</ul>
