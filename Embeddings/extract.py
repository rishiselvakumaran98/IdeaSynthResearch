import requests
import time
from bs4 import BeautifulSoup
import os

start_time = time.time()
paper_name = "paper-1"
with open(f"{paper_name}.pdf", "rb") as pdf_file:
    resp = requests.post(
        "http://localhost:8070/api/processFulltextDocument",
        files={"input": pdf_file}
    )
tei_xml = resp.text
print(f"GROBID processing took {time.time() - start_time:.1f}s")


soup = BeautifulSoup(tei_xml, "xml")
body = soup.find("text").find("body")

sections_dir = os.path.join("outputs", f"{paper_name}_sections")
os.makedirs(sections_dir, exist_ok=True)

heads = body.find_all("head")
for idx, head in enumerate(heads, start=1):
    sec_id = head.get("n") or str(idx)
    safe_id = sec_id.replace(".", "_")
    title = head.get_text(strip=True)

    content_parts = [title, ""]
    for sib in head.find_next_siblings():
        if sib.name == "head":
            break
        content_parts.append(sib.get_text(strip=True))

    section_text = "\n\n".join(p for p in content_parts if p)

    fname = f"{paper_name}_section_{safe_id}.txt"
    path = os.path.join(sections_dir, fname)
    with open(path, "w", encoding="utf-8") as f:
        f.write(section_text)

    print(f"Wrote {fname}")

with open(os.path.join("outputs", f"{paper_name}_document.xml"), "w", encoding="utf-8") as f:
    f.write(tei_xml)

print("Done. All sections saved in ./outputs/sections/")
