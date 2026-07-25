import pandas as pd
import io

file_path = "/Users/themainframe/.gemini/antigravity-ide/brain/0dc8cfd6-a750-4284-a81c-1d76f563788c/.system_generated/steps/155/content.md"
with open(file_path, 'r') as f:
    lines = f.readlines()

csv_start_idx = 0
for i, line in enumerate(lines):
    if line.startswith("Title,Url"):
        csv_start_idx = i
        break

csv_content = "".join(lines[csv_start_idx:])
df = pd.read_csv(io.StringIO(csv_content))

md_lines = []
md_lines.append("---")
md_lines.append("relational_density: 0.8")
md_lines.append("---")
md_lines.append("")
md_lines.append("# Humanities Links")
md_lines.append("")
md_lines.append("| Title | Source |")
md_lines.append("|---|---|")

for _, row in df.iterrows():
    if pd.isna(row['Title']):
        continue
        
    title = str(row['Title']).strip()
    url = str(row['Url']).strip() if pd.notna(row['Url']) else ""
    source_title = str(row['Source.Title']).strip() if pd.notna(row['Source.Title']) else ""
    source_url = str(row['Source.Url']).strip() if pd.notna(row['Source.Url']) else ""
    
    title_link = f"[{title}]({url})" if url else title
    source_link = f"[{source_title}]({source_url})" if source_url else source_title
        
    md_lines.append(f"| {title_link} | {source_link} |")

with open("/Users/themainframe/antifallin/mighty-joe-black/docs/humanities_links.md", 'w') as f:
    f.write("\n".join(md_lines))
