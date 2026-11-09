# 홈 기판 SVG(Liquid 포함) 생성기. 사용: python3 tools/gen_board.py _includes/board.html
import sys

OUT = sys.argv[1]

# MCU: 가운데 QFP. 몸체 150x150, 변마다 다리 10개(간격 13)
MX0, MY0, MW = 365, 115, 150
PIN_L = [131.5 + 13 * i for i in range(10)]  # 왼쪽/오른쪽 다리 y
PIN_T = [381.5 + 13 * i for i in range(10)]  # 위/아래 다리 x


def r(x, y, w, h, cls, rx=None):
    rx_s = f' rx="{rx}"' if rx is not None else ''
    return f'<rect class="{cls}" x="{x:g}" y="{y:g}" width="{w:g}" height="{h:g}"{rx_s}/>'


def path(d, cls):
    return f'<path class="{cls}" d="{d}"/>'


def via(x, y, cls='via'):
    return f'<circle class="{cls}" cx="{x:g}" cy="{y:g}" r="4"/>'


def silk(x, y, t, cls='silk-ref', anchor='start'):
    return f'<text class="{cls}" x="{x:g}" y="{y:g}" text-anchor="{anchor}">{t}</text>'


def route(x0, y0, bend, y1, x1):
    """가로 → 45도 → 가로. x0에서 출발해 bend에서 꺾여 y1 높이로, x1까지."""
    dy = abs(y1 - y0)
    dx = dy if x1 > x0 else -dy
    if dy == 0:
        return f'M{x0:g} {y0:g} H{x1:g}'
    return f'M{x0:g} {y0:g} H{bend:g} L{bend + dx:g} {y1:g} H{x1:g}'


def cap0603(x, y, vertical=True):
    # 작은 칩 부품 (몸체 + 양끝 은색 전극)
    if vertical:
        return r(x - 4, y - 6, 8, 12, 'p-smd') + r(x - 4, y - 6, 8, 3, 'p-silver') + r(x - 4, y + 3, 8, 3, 'p-silver')
    return r(x - 6, y - 4, 12, 8, 'p-smd') + r(x - 6, y - 4, 3, 8, 'p-silver') + r(x + 3, y - 4, 3, 8, 'p-silver')


def led0603(x, y):
    return f'<g class="led0603">{r(x - 5, y - 3, 10, 6, "led-body", 1)}{r(x - 2.5, y - 2, 5, 4, "led", 1)}</g>'


# ---------- 카테고리별 주변 부품 (traces, part svg, refs, 라벨 위치, 클릭 영역) ----------
parts = []

# 0 개발: SWD 디버그 헤더 2x5 (왼쪽 위)
cy = 79
g = [r(205, cy - 15, 65, 30, 'p-plastic', 2)]
for k in range(5):
    for row in (cy - 6.5, cy + 6.5):
        g.append(r(211.5 + 13 * k - 3.5, row - 3.5, 7, 7, 'p-gold'))
traces = [route(270, cy - 6.5, 280, PIN_L[0], MX0 - 14), route(270, cy + 6.5, 275, PIN_L[1], MX0 - 14)]
refs = [silk(205, cy - 21, 'J1'), silk(270, cy - 21, 'SWD', anchor='end')]
parts.append(dict(side='L', cy=cy, g=g, traces=traces, extra=[], refs=refs))

# 1 CTF/Wargame: 크리스탈 3225 + 로드 콘덴서 2개 (왼쪽 가운데)
cy = 190
ya, yb = PIN_L[4], PIN_L[5]
g = [r(234, ya - 3, 6, 6, 'p-silver'), r(266, ya - 3, 6, 6, 'p-silver'),
     r(234, yb - 3, 6, 6, 'p-silver'), r(266, yb - 3, 6, 6, 'p-silver'),
     r(238, cy - 13, 30, 26, 'p-lid', 2), r(242, cy - 9, 22, 18, 'p-lid-in', 1)]
traces = [route(272, ya, 0, ya, MX0 - 14), route(272, yb, 0, yb, MX0 - 14)]
extra = [path(f'M300 {ya:g} V172', 'trace-plain'), cap0603(300, 166), path('M300 160 V152', 'trace-plain'), via(300, 150, 'via-gnd'),
         path(f'M300 {yb:g} V208', 'trace-plain'), cap0603(300, 214), path('M300 220 V228', 'trace-plain'), via(300, 230, 'via-gnd')]
refs = [silk(253, cy - 19, 'Y1', anchor='middle'), silk(308, 169, 'C1'), silk(308, 217, 'C2')]
parts.append(dict(side='L', cy=cy, g=g, traces=traces, extra=extra, refs=refs))

# 2 Bug Bounty: UART 헤더 1x4, GND/TX/RX/VCC 인쇄 (왼쪽 아래)
cy = 301
pins = [cy - 19.5, cy - 6.5, cy + 6.5, cy + 19.5]
g = [r(256, cy - 27, 15, 54, 'p-plastic', 2)] + [r(260, y - 3.5, 7, 7, 'p-gold') for y in pins]
traces = [route(271, pins[1], 275, PIN_L[8], MX0 - 14), route(271, pins[2], 280, PIN_L[9], MX0 - 14)]
refs = [silk(263.5, cy - 33, 'UART', anchor='middle')] + [silk(250, y + 3, t, 'silk-pin', 'end') for y, t in zip(pins, ['GND', 'TX', 'RX', 'VCC'])]
parts.append(dict(side='L', cy=cy, g=g, traces=traces, extra=[], refs=refs))

# 3 블로그/기술문서: SPI 플래시 SOIC-8 (오른쪽 위)
cy = 79
sp = [cy - 9.75, cy - 3.25, cy + 3.25, cy + 9.75]
g = [r(615, y - 1.5, 8, 3, 'p-lead-box') for y in sp] + [r(652, y - 1.5, 8, 3, 'p-lead-box') for y in sp]
g += [r(622, cy - 14, 31, 28, 'p-ic', 2), '<circle class="ic-notch" cx="627" cy="70" r="1.8"/>', silk(637.5, cy + 3, 'FLASH', 'p-mark', 'middle')]
traces = [route(615, sp[0], 600, PIN_L[0], MX0 + MW + 14), route(615, sp[2], 605, PIN_L[1], MX0 + MW + 14)]
refs = [silk(622, cy - 20, 'U2')]
parts.append(dict(side='R', cy=cy, g=g, traces=traces, extra=[], refs=refs))

# 4 논문/컨퍼런스: 칩 안테나 + 정합 인덕터 (오른쪽 가운데)
cy = 190
ya = PIN_L[4]
g = [r(612, ya - 7, 52, 14, 'p-ceramic', 2), r(612, ya - 7, 7, 14, 'p-silver'), r(657, ya - 7, 7, 14, 'p-silver'), r(622, ya - 7, 4, 14, 'p-ant-band')]
traces = [f'M{MX0 + MW + 14} {ya:g} H559 M571 {ya:g} H612']
extra = [cap0603(565, ya, vertical=False)]
refs = [silk(612, ya - 12, 'ANT1'), silk(565, ya - 9, 'L1', anchor='middle')]
parts.append(dict(side='R', cy=cy, g=g, traces=traces, extra=extra, refs=refs))

# 5 공모전/자격증: 리셋 버튼 + 풀업 저항 (오른쪽 아래)
cy = 301
g = [r(612, 285, 7, 6, 'p-lead-box'), r(612, 311, 7, 6, 'p-lead-box'), r(659, 285, 7, 6, 'p-lead-box'), r(659, 311, 7, 6, 'p-lead-box'),
     r(618, cy - 21, 42, 42, 'p-silver', 3), r(623, cy - 16, 32, 32, 'p-sw-in', 2), f'<circle class="p-sw-btn" cx="639" cy="{cy}" r="10"/>']
yr = PIN_L[9]
traces = [route(MX0 + MW + 14, yr, 560, 288, 612)]
extra = [path(f'M545 {yr:g} V240', 'trace-plain'), cap0603(545, 234), path('M545 228 V220', 'trace-plain'), via(545, 216, 'via-vcc'),
         path('M612 314 H600', 'trace-plain'), via(596, 314, 'via-gnd')]
refs = [silk(618, cy - 27, 'SW1'), silk(553, 237, 'R1'), silk(666, cy - 27, 'RST', anchor='end')]
parts.append(dict(side='R', cy=cy, g=g, traces=traces, extra=extra, refs=refs))

# ---------- 출력 ----------
o = []
o.append('''{%- comment -%}
  홈 상단 기판 그림. 이 파일은 생성기로 만든 것 (좌표 계산). 손으로 고치기보다 생성기를 다시 돌리는 편이 안전.
  가운데 MCU = toz-210, 주변 = 실제로 MCU에 붙는 부품. 카테고리 순서는 _data/blog_categories.yml 순서
  (개발 SWD 헤더, CTF 크리스탈, Bug Bounty UART, 기술문서 SPI 플래시, 논문 칩 안테나, 공모전 리셋 버튼).
  이름 앞 작은 LED는 그 카테고리에 글이 있을 때만 켜짐.
{%- endcomment -%}
<figure class="board" aria-label="카테고리 기판">
<svg class="board-svg" viewBox="0 0 880 380" role="group" aria-label="카테고리 6개">
<rect class="pcb" x="4" y="4" width="872" height="372" rx="14"/>
<g class="holes" aria-hidden="true"><circle cx="30" cy="30" r="8"/><circle cx="850" cy="30" r="8"/><circle cx="30" cy="350" r="8"/><circle cx="850" cy="350" r="8"/></g>''')

# MCU + 전원 디커플링
mcu = ['<g class="ic" aria-hidden="true">']
for y in PIN_L:
    mcu.append(r(MX0 - 14, y - 2.5, 14, 5, 'pin'))
    mcu.append(r(MX0 + MW, y - 2.5, 14, 5, 'pin'))
for x in PIN_T:
    mcu.append(r(x - 2.5, MY0 - 14, 5, 14, 'pin'))
    mcu.append(r(x - 2.5, MY0 + MW, 5, 14, 'pin'))
mcu.append(r(MX0, MY0, MW, MW, 'ic-body', 4))
mcu.append(f'<circle class="ic-notch" cx="{MX0 + 14}" cy="{MY0 + 14}" r="4"/>')
mcu.append(f'<text class="ic-label" x="{MX0 + MW / 2:g}" y="{MY0 + MW / 2 + 6:g}" text-anchor="middle">toz-210</text>')
mcu.append('</g>')
tx, bx = PIN_T[4], PIN_T[5]
dec = ['<g class="decouple" aria-hidden="true">',
       path(f'M{tx:g} {MY0 - 14} V88', 'trace-plain'), cap0603(tx, 82), path(f'M{tx:g} 76 V66', 'trace-plain'), via(tx, 62, 'via-gnd'), silk(tx + 8, 85, 'C3'),
       path(f'M{bx:g} {MY0 + MW + 14} V292', 'trace-plain'), cap0603(bx, 298), path(f'M{bx:g} 304 V314', 'trace-plain'), via(bx, 318, 'via-gnd'), silk(bx + 8, 301, 'C4'),
       '</g>']
o += mcu + dec

# 접지 스티칭 비아 (장식)
o.append('<g aria-hidden="true">' + ''.join(via(x, y, 'via-gnd') for x, y in [(130, 30), (750, 30), (130, 350), (660, 350), (440, 30), (590, 350)]) + '</g>')

for i, p in enumerate(parts):
    cy = p['cy']
    if p['side'] == 'L':
        led_x, text_x, hit = 52, 62, (36, cy - 42, 250, 84)
    else:
        led_x, text_x, hit = 692, 704, (596, cy - 42, 260, 84)
    o.append(f'{{%- assign c = site.data.blog_categories[{i}] -%}}{{%- assign n = site.categories[c.name] | size -%}}')
    o.append(f'''<a class="fp{{% if n > 0 %}} is-on{{% endif %}}" href="{{{{ '/category/' | append: c.slug | append: '/' | relative_url }}}}" style="--i: {i}">''')
    o.append(r(*hit, 'fp-hit', 6))
    o += [path(d, 'trace') for d in p['traces']]
    o += p['extra']
    o.append('<g class="part" aria-hidden="true">' + ''.join(p['g']) + '</g>')
    o.append('<g aria-hidden="true">' + ''.join(p['refs']) + '</g>')
    o.append(f'<g class="led-wrap">{led0603(led_x, cy - 6)}</g>')
    o.append(f'<text class="fp-name" x="{text_x}" y="{cy - 1}">{{{{ c.name }}}}</text>')
    o.append(f'<text class="fp-count" x="{text_x}" y="{cy + 19}">{{% if n > 0 %}}글 {{{{ n }}}}개{{% else %}}비어 있음{{% endif %}}</text>')
    o.append('</a>')

o.append('''<text class="silk-rev" x="826" y="362" text-anchor="end">toz-210 rev {{ site.time | date: '%Y.%m.%d' }}</text>
</svg>

<ul class="board-list">
  <li class="board-list-ic">toz-210</li>
  {%- for c in site.data.blog_categories -%}
  {%- assign n = site.categories[c.name] | size -%}
  <li class="{% if n > 0 %}is-on{% endif %}">
    <a href="{{ '/category/' | append: c.slug | append: '/' | relative_url }}">
      <span class="bl-led" aria-hidden="true"></span>
      <span class="bl-name">{{ c.name }}</span>
      <span class="bl-count">{% if n > 0 %}글 {{ n }}개{% else %}비어 있음{% endif %}</span>
    </a>
  </li>
  {%- endfor -%}
</ul>
</figure>
''')
open(OUT, 'w', encoding='utf-8').write('\n'.join(o))
print('ok')
