#!/usr/bin/env python3
"""Parse CV tex and generate news HTML rows for the homepage.

Hybrid mode:
- 1-2 papers at a venue: show individual titles (bold if first-author)
- 3+ papers: show count + highlights (oral, first-author count)
"""
import re
import sys
from collections import defaultdict
from html import escape

# Normalize long journal names to short forms
VENUE_NORMALIZE = {
    'IEEE Transactions on Pattern Analysis and Machine Intelligence': 'IEEE TPAMI',
    'IEEE Transactions on Medical Imaging': 'IEEE TMI',
    'IEEE Journal of Biomedical and Health Informatics': 'IEEE JBHI',
    'Medical Image Analysis': 'Medical Image Analysis',
    'Transactions on Machine Learning Research': 'TMLR',
}

VENUE_ALIASES = {'MICCA': 'MICCAI'}

JOURNALS = {'IEEE TPAMI', 'IEEE TMI', 'IEEE JBHI', 'Medical Image Analysis', 'TMLR',
            'European Heart Journal-Digital Health'}

# Approximate month (MM) for acceptance/publication announcements
VENUE_MONTH = {
    'CVPR': '02', 'ICCV': '07', 'ECCV': '07',
    'MIDL': '02', 'MICCAI': '06', 'MICCAI-MLMI': '06',
    'NeurIPS': '09', 'ICLR': '01', 'ICML': '05', 'BMVC': '08',
    'IEEE TPAMI': '03', 'IEEE TMI': '03', 'IEEE JBHI': '08',
    'Medical Image Analysis': '03', 'TMLR': '07',
    'European Heart Journal-Digital Health': '06',
}

VISIBLE_COUNT = 5
BULK_THRESHOLD = 3  # 3+ papers → grouped summary
MY_NAME = 'Fengbei Liu'


def extract_brace_arg(content, start):
    """Extract content of a {}-delimited argument starting at position start."""
    i = content.index('{', start)
    depth, begin = 0, i
    while i < len(content):
        if content[i] == '{':
            depth += 1
        elif content[i] == '}':
            depth -= 1
            if depth == 0:
                return content[begin + 1:i], i + 1
        i += 1
    return '', i


def strip_latex(s):
    """Remove common LaTeX commands from a string for plain-text display."""
    s = re.sub(r'\\textbf\{([^}]*)\}', r'\1', s)
    s = re.sub(r'\\textit\{([^}]*)\}', r'\1', s)
    s = re.sub(r'\\emph\{([^}]*)\}', r'\1', s)
    s = re.sub(r'\$[^$]*\$', '', s)  # remove inline math like $^*$
    s = re.sub(r'\\[a-zA-Z]+', '', s)  # remove remaining commands
    s = re.sub(r'[{}]', '', s)  # remove stray braces
    return s.strip()


def truncate(s, maxlen=70):
    """Truncate string with ellipsis if too long."""
    if len(s) <= maxlen:
        return s
    # Try to cut at colon (paper acronym: subtitle)
    colon = s.find(':')
    if 0 < colon <= maxlen:
        return s[:colon]
    return s[:maxlen - 3] + '...'


def is_first_author(authors_raw):
    """Check if MY_NAME appears as first author (possibly with co-first *)."""
    authors_clean = strip_latex(authors_raw)
    # Split by comma, check first 1-2 names (co-first author with *)
    parts = [a.strip() for a in authors_clean.split(',')]
    for p in parts[:2]:
        if MY_NAME in p:
            return True
        # Stop at first author without * marker
        if '*' not in p:
            break
    return False


def parse_publications(tex_content):
    """Parse all \\resumePubheading entries into structured records."""
    results = []
    idx = 0
    while True:
        pos = tex_content.find('\\resumePubheading', idx)
        if pos == -1:
            break
        title_raw, after1 = extract_brace_arg(tex_content, pos)
        authors_raw, after2 = extract_brace_arg(tex_content, after1)
        venue_str, after3 = extract_brace_arg(tex_content, after2)
        idx = after3

        # Extract year
        year_match = re.search(r'(20\d{2})', venue_str)
        if not year_match:
            continue
        year = year_match.group(1)

        # Extract venue name
        venue_raw = venue_str[:year_match.start()].strip().rstrip(',').strip()
        for long_name, short_name in VENUE_NORMALIZE.items():
            if long_name in venue_raw:
                venue_raw = short_name
                break
        venue_raw = VENUE_ALIASES.get(venue_raw, venue_raw)

        # Extract qualifiers (Oral, Early Accept, etc.)
        after_year = venue_str[year_match.end():]
        qualifiers = [q.strip() for q in after_year.split(',') if q.strip()]

        title = strip_latex(title_raw)
        first_author = is_first_author(authors_raw)

        results.append({
            'title': title,
            'venue': venue_raw,
            'year': year,
            'first_author': first_author,
            'oral': any('oral' in q.lower() for q in qualifiers),
            'qualifiers': qualifiers,
        })
    return results


def oral_tag(n=1):
    label = f'{n} ' if n > 1 else ''
    return f' <span class="news-tag">[{label}Oral]</span>'


def is_accepted(p):
    """True if the paper is accepted/in-press rather than fully published."""
    return any('accept' in q.lower() or 'in press' in q.lower() for q in p['qualifiers'])


def venue_verb(is_journal, accepted):
    """Pick the announcement verb. Journals: published vs accepted-in-press."""
    if is_journal:
        return 'accepted in' if accepted else 'published in'
    return 'accepted at'


def generate_venue_entry(venue, year, papers):
    """Generate news text for papers at a single venue."""
    is_journal = venue in JOURNALS
    venue_display = f'{venue} {year}' if not is_journal else venue
    month = VENUE_MONTH.get(venue, '01')
    n_oral = sum(1 for p in papers if p['oral'])

    if len(papers) < BULK_THRESHOLD:
        # Individual titles
        rows = []
        for p in papers:
            safe_title = escape(p['title'])
            title_html = f'<span class="papertitle">{safe_title}</span>'
            qual = oral_tag() if p['oral'] else ''
            verb = venue_verb(is_journal, is_accepted(p))
            text = f'{title_html} {verb} {venue_display}.{qual}'
            rows.append((year, month, text))
        return rows
    else:
        # Grouped summary
        count = len(papers)
        verb = venue_verb(is_journal, all(is_accepted(p) for p in papers))
        text = f'{count} papers {verb} {venue_display}.'
        qual = oral_tag(n_oral) if n_oral else ''
        return [(year, month, text + qual)]


def generate_news_html(pubs):
    """Generate HTML news rows with hybrid format.

    Recent years (current & previous): per-venue detail.
    Older years: one compressed line per year.
    """
    from datetime import date
    recent_cutoff = str(date.today().year - 1)  # e.g. "2025"

    # Split into recent vs old
    recent, old = [], []
    for p in pubs:
        (recent if p['year'] >= recent_cutoff else old).append(p)

    entries = []

    # --- Recent: per-venue hybrid ---
    recent_groups = defaultdict(list)
    for p in recent:
        recent_groups[(p['year'], p['venue'])].append(p)
    for (year, venue), papers in recent_groups.items():
        entries.extend(generate_venue_entry(venue, year, papers))

    # --- Old: one line per year ---
    old_by_year = defaultdict(list)
    for p in old:
        old_by_year[p['year']].append(p)
    for year in sorted(old_by_year.keys(), reverse=True):
        papers = old_by_year[year]
        count = len(papers)
        n_oral = sum(1 for p in papers if p['oral'])
        # Collect unique venue names
        venues_seen = []
        for p in papers:
            v = p['venue']
            if v not in venues_seen:
                venues_seen.append(v)
        venue_list = ', '.join(venues_seen)
        count_word = 'One' if count == 1 else str(count)
        paper_word = 'paper' if count == 1 else 'papers'
        across = 'in' if len(venues_seen) == 1 else 'across'
        text = f'{count_word} {paper_word} published {across} {venue_list}.'
        qual = oral_tag(n_oral) if n_oral else ''
        # Use latest month among venues for sort order
        month = max(VENUE_MONTH.get(v, '01') for v in venues_seen)
        entries.append((year, month, text + qual))

    entries.sort(key=lambda x: (x[0], x[1]), reverse=True)

    rows = []
    for i, (year, month, text) in enumerate(entries):
        cls = ' class="hidden-news"' if i >= VISIBLE_COUNT else ''
        rows.append(f'    <tr{cls}><td class="date">{year}.{month}</td><td>{text}</td></tr>')
    return '\n'.join(rows)


def update_index_html(index_path, news_html):
    """Replace content between NEWS_AUTO markers in index.html."""
    with open(index_path) as f:
        content = f.read()

    pattern = r'(<!-- NEWS_AUTO:START -->\n).*?(\n\s*<!-- NEWS_AUTO:END -->)'
    replacement = f'\\1{news_html}\\2'
    new_content, count = re.subn(pattern, replacement, content, flags=re.DOTALL)

    if count == 0:
        print('ERROR: NEWS_AUTO markers not found in index.html', file=sys.stderr)
        sys.exit(1)

    with open(index_path, 'w') as f:
        f.write(new_content)
    print(f'Updated {index_path} with {news_html.count("<tr")} news entries.')


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print(f'Usage: {sys.argv[0]} <cv.tex> <index.html>', file=sys.stderr)
        sys.exit(1)

    tex_path, index_path = sys.argv[1], sys.argv[2]
    with open(tex_path) as f:
        tex_content = f.read()

    pubs = parse_publications(tex_content)
    news_html = generate_news_html(pubs)
    update_index_html(index_path, news_html)
