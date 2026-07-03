import sys
import os

# Set up path for import
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from src.extra_pages_content import EXTRA_PAGES

print(f"Total Extra Pages: {len(EXTRA_PAGES)}")
print("-" * 80)
print(f"{'Category':<15} | {'Slug':<40} | {'Related Course Slug':<30}")
print("-" * 80)
for pg in EXTRA_PAGES:
    print(f"{pg.get('category'):<15} | {pg.get('slug'):<40} | {pg.get('related_course_slug'):<30}")
