#!/usr/bin/env python3
"""
sync_search_query_intent.py

In-place search query intent synchronization script for CACTS.
Enriches existing location and course pages with targeted FAQ Q&As and Schema synonyms
based on real Google Search Console query metrics without creating duplicate pages or
replacing existing content.

Usage:
    python scripts/sync_search_query_intent.py [--dry-run]
"""

import os
import sys
import json
import re

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REGISTRY_PATH = os.path.join(PROJECT_ROOT, "src", "gsc_query_intent_registry.json")


def load_registry():
    if not os.path.exists(REGISTRY_PATH):
        print(f"[ERROR] Registry not found at {REGISTRY_PATH}")
        sys.exit(1)
    with open(REGISTRY_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def update_schema_alternate_names(content, new_alternates):
    """
    Appends new synonym strings to the first primary alternateName array in JSON-LD.
    If alternateName does not exist in top LocalBusiness schema (like index.html), injects it.
    """
    if not new_alternates:
        return content, False

    # Check if alternateName exists in schema
    pattern = re.compile(r'("alternateName"\s*:\s*\[)(.*?)(\])', re.DOTALL)
    match = pattern.search(content)
    if match:
        prefix, body, suffix = match.group(1), match.group(2), match.group(3)
        existing_items = re.findall(r'"([^"]+)"', body)
        
        added_items = []
        for item in new_alternates:
            if item not in existing_items and item not in added_items:
                added_items.append(item)

        if not added_items:
            return content, False

        last_line_indent = "  "
        indent_match = re.search(r'\n([ \t]+)"[^"]+"', body)
        if indent_match:
            last_line_indent = indent_match.group(1)

        formatted_additions = ",\n" + ",\n".join(f'{last_line_indent}"{item}"' for item in added_items)
        new_body = body.rstrip() + formatted_additions + "\n  "
        new_content = content[:match.start()] + prefix + new_body + suffix + content[match.end():]
        return new_content, True
    else:
        # Injects alternateName after "name": "CACTS - Centre of Advanced Computer Training and Studies",
        inject_pattern = re.compile(r'("name"\s*:\s*"CACTS\s*-\s*Centre of Advanced Computer Training and Studies",)', re.DOTALL)
        inject_match = inject_pattern.search(content)
        if inject_match:
            formatted_list = ",\n".join(f'            "{item}"' for item in new_alternates)
            injected_block = (
                f'\n      "alternateName": [\n'
                f'{formatted_list}\n'
                f'      ],'
            )
            new_content = content[:inject_match.end()] + injected_block + content[inject_match.end():]
            return new_content, True

    return content, False


def update_faq_schema(content, faqs):
    """
    Appends new Question entities to the FAQPage JSON-LD schema mainEntity array.
    """
    if not faqs:
        return content, False

    faq_pattern = re.compile(r'("@type"\s*:\s*"FAQPage".*?"mainEntity"\s*:\s*\[)(.*?)(\]\s*\})', re.DOTALL)
    match = faq_pattern.search(content)
    if not match:
        return content, False

    prefix, body, suffix = match.group(1), match.group(2), match.group(3)

    added_faqs = []
    for faq in faqs:
        q_clean = faq["q"].strip()
        if q_clean not in body:
            added_faqs.append(faq)

    if not added_faqs:
        return content, False

    schema_entries = []
    for faq in added_faqs:
        entry = (
            "    {\n"
            '      "@type": "Question",\n'
            f'      "name": {json.dumps(faq["q"])},\n'
            '      "acceptedAnswer": {\n'
            '        "@type": "Answer",\n'
            f'        "text": {json.dumps(faq["a"])}\n'
            "      }\n"
            "    }"
        )
        schema_entries.append(entry)

    sep = ",\n"
    new_body = body.rstrip() + sep + ",\n".join(schema_entries) + "\n  "
    new_content = content[:match.start()] + prefix + new_body + suffix + content[match.end():]
    return new_content, True


def update_dom_faqs(content, faqs, is_course=False):
    """
    Appends new FAQ cards to the visible DOM FAQ section.
    """
    if not faqs:
        return content, False

    added_count = 0
    new_content = content

    for faq in faqs:
        q_text = faq["q"].strip()
        a_text = faq["a"].strip()

        if is_course:
            # Check if already in accordion
            accordion_pattern = re.compile(r'(<div\s+class=["\']course-faqs-accordion["\']\s*>)(.*?)(</div>\s*</div>\s*</div>\s*<aside)', re.DOTALL)
            match = accordion_pattern.search(new_content)
            if match:
                body = match.group(2)
                if q_text in body:
                    continue

                dom_entry = (
                    '\n              <div class="curriculum-module">\n'
                    '                <div class="module-header faq-header">\n'
                    f'                  <h4>{q_text}</h4>\n'
                    '                  <span class="accordion-icon">+</span>\n'
                    '                </div>\n'
                    '                <div class="faq-content module-content">\n'
                    '                  <div class="module-content-inner">\n'
                    '                    <p style="color: var(--text-secondary); font-size: 0.95rem">\n'
                    f'                      {a_text}\n'
                    '                    </p>\n'
                    '                  </div>\n'
                    '                </div>\n'
                    '              </div>'
                )
                start, mid, end = match.group(1), match.group(2), match.group(3)
                new_content = new_content[:match.start()] + start + mid + dom_entry + "\n            " + end + new_content[match.end():]
                added_count += 1
        else:
            # Location page: check inside u-90160b container
            loc_pattern = re.compile(r'(<div\s+class=["\']u-90160b["\']\s*>)(.*?)(</div>\s*</section>)', re.DOTALL)
            match = loc_pattern.search(new_content)
            if match:
                body = match.group(2)
                if q_text in body:
                    continue

                dom_card = (
                    '\n  <div class="card p-6">\n'
                    '  <h3 class="accent-title-sm">\n'
                    f'  {q_text}\n'
                    '  </h3>\n'
                    '  <p class="text-muted-relaxed">\n'
                    f'  {a_text}\n'
                    '  </p>\n'
                    '  </div>\n  '
                )
                start, mid, end = match.group(1), match.group(2), match.group(3)
                new_content = new_content[:match.start()] + start + mid + dom_card + end + new_content[match.end():]
                added_count += 1

    return new_content, (added_count > 0)


def sync_page(page_cfg, dry_run=False):
    rel_path = page_cfg["page_path"]
    full_path = os.path.join(PROJECT_ROOT, rel_path.replace("/", os.sep))

    if not os.path.exists(full_path):
        print(f"[SKIP] Page not found: {rel_path}")
        return False

    with open(full_path, "r", encoding="utf-8") as f:
        content = f.read()

    is_course = "courses" in rel_path
    new_content = content
    changes_made = []

    # 1. Update Schema alternateName
    new_content, alt_changed = update_schema_alternate_names(new_content, page_cfg.get("schema_alternates", []))
    if alt_changed:
        changes_made.append(f"alternateName ({len(page_cfg.get('schema_alternates', []))} items)")

    # 2. Update FAQ Schema
    new_content, faq_schema_changed = update_faq_schema(new_content, page_cfg.get("faqs", []))
    if faq_schema_changed:
        changes_made.append(f"FAQPage Schema ({len(page_cfg.get('faqs', []))} Q&As)")

    # 3. Update DOM FAQs
    new_content, dom_changed = update_dom_faqs(new_content, page_cfg.get("faqs", []), is_course=is_course)
    if dom_changed:
        changes_made.append(f"DOM FAQs ({len(page_cfg.get('faqs', []))} Q&As)")

    if changes_made:
        print(f"[{'DRY-RUN' if dry_run else 'UPDATED'}] {rel_path} -> Added: {', '.join(changes_made)}")
        if not dry_run:
            with open(full_path, "w", encoding="utf-8") as f:
                f.write(new_content)
        return True
    else:
        print(f"[UNCHANGED] {rel_path} -> Already synchronized.")
        return False


def main():
    dry_run = "--dry-run" in sys.argv
    registry = load_registry()
    pages = registry.get("pages", [])

    print(f"=== Starting In-Place GSC Query Intent Synchronization ({'DRY-RUN' if dry_run else 'LIVE'}) ===")
    print(f"Total target pages configured: {len(pages)}")

    total_updated = 0
    for page_cfg in pages:
        updated = sync_page(page_cfg, dry_run=dry_run)
        if updated:
            total_updated += 1

    print(f"\nSynchronization completed. Pages modified: {total_updated} / {len(pages)}")


if __name__ == "__main__":
    main()
