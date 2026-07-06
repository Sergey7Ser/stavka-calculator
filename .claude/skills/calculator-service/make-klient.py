#!/usr/bin/env python3
"""Генерирует klient.html — клиентскую версию astralium.html без внутренних цен.

Убирает: переключатель «Стандарт / Нижняя граница», все min-цены из прайса,
служебную приписку про правку цен. Запускать после каждой правки astralium.html:
    python3 .claude/skills/calculator-service/make-klient.py
"""
import re, pathlib

root = pathlib.Path(__file__).resolve().parents[3]
src = (root / 'astralium.html').read_text(encoding='utf-8')

# 1) выпилить нижние цены из данных (min: N и min20: N) — их не должно быть в исходнике
src = re.sub(r',\s*min:\s*[\d.]+', '', src)
src = re.sub(r',\s*min20:\s*[\d.]+', '', src)

# 2) убрать переключатель уровня прайса из шапки
src = re.sub(
    r'<div class="mode" title="Уровень прайса">.*?</div>\n', '', src, flags=re.S)

# 3) JS: заглушить обращения к кнопкам переключателя
src = src.replace("document.getElementById('modeStd').classList.toggle('on', m === 'std');\n", '')
src = src.replace("document.getElementById('modeMin').classList.toggle('on', m === 'min');\n", '')
src = src.replace("document.getElementById('modeStd').addEventListener('click', () => setMode('std'));\n", '')
src = src.replace("document.getElementById('modeMin').addEventListener('click', () => setMode('min'));\n", '')

# 4) клиентская подводка вместо служебной
src = re.sub(r'<p class="note">.*?</p>', (
    '<p class="note">Предварительный расчёт стоимости камня и работ. '
    'Финальная цена фиксируется в договоре после выезда на замер.</p>'), src, count=1, flags=re.S)

# 5) отдельное хранилище, чтобы не пересекаться с рабочей версией
src = src.replace("astralium_calc_v1", "astralium_klient_v1")

(root / 'klient.html').write_text(src, encoding='utf-8')
print('klient.html создан:', len(src), 'байт; упоминаний min:', len(re.findall(r'min\d*:', src)))
