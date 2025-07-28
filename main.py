import os
import json
import fitz  # PyMuPDF

INPUT_DIR = "input"
OUTPUT_DIR = "output"

def get_title_and_headings(doc):
    spans_by_size = []
    size_counts = {}

    # Step 1: Gather font sizes from first 2 pages for title detection
    for page_num in range(min(2, len(doc))):
        page = doc[page_num]
        blocks = page.get_text("dict")["blocks"]
        for block in blocks:
            for line in block.get("lines", []):
                for span in line.get("spans", []):
                    text = span["text"].strip()
                    if text:
                        size = round(span["size"], 1)
                        spans_by_size.append((size, text, page_num))
                        size_counts[size] = size_counts.get(size, 0) + 1

    # Step 2: Rank font sizes by usage frequency
    sorted_sizes = sorted(size_counts.items(), key=lambda x: (-x[1], -x[0]))
    font_ranks = [size for size, _ in sorted_sizes]

    # Step 3: Map font sizes to levels
    size_to_level = {}
    if len(font_ranks) > 0:
        size_to_level[font_ranks[0]] = "title"
    if len(font_ranks) > 1:
        size_to_level[font_ranks[1]] = "H1"
    if len(font_ranks) > 2:
        size_to_level[font_ranks[2]] = "H2"
    if len(font_ranks) > 3:
        size_to_level[font_ranks[3]] = "H3"
    if len(font_ranks) > 4:
        size_to_level[font_ranks[4]] = "H4"

    # Step 4: Extract the title from first 2 pages
    title = ""
    for size, text, _ in spans_by_size:
        if size_to_level.get(size) == "title":
            title += text.strip() + " "
    title = title.strip()

    # Step 5: Extract headings across all pages
    heading_data = []
    for page_num in range(len(doc)):
        page = doc[page_num]
        blocks = page.get_text("dict")["blocks"]
        for block in blocks:
            for line in block.get("lines", []):
                line_text = ""
                line_size = 0
                for span in line.get("spans", []):
                    text = span["text"].strip()
                    if not text or len(text) < 2:
                        continue
                    size = round(span["size"], 1)
                    level = size_to_level.get(size)

                    if level in {"H1", "H2", "H3", "H4"}:
                        if line_size == 0:
                            line_size = size
                        line_text += " " + text

                if line_text.strip():
                    word_count = len(line_text.strip().split())
                    if 2 <= word_count <= 18:
                        heading_data.append({
                            "level": size_to_level.get(line_size),
                            "text": line_text.strip(),
                            "page": page_num
                        })

    return title, heading_data


def process_pdf(file_path, output_path):
    doc = fitz.open(file_path)
    title, outline = get_title_and_headings(doc)
    result = {
        "title": title,
        "outline": outline
    }
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    doc.close()


if __name__ == "__main__":
    os.makedirs(INPUT_DIR, exist_ok=True)
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    for filename in os.listdir(INPUT_DIR):
        if filename.lower().endswith(".pdf"):
            input_path = os.path.join(INPUT_DIR, filename)
            output_path = os.path.join(OUTPUT_DIR, filename.replace(".pdf", ".json"))
            print(f"Processing {filename}")
            process_pdf(input_path, output_path)
            print(f"Saved outline to {output_path}")
