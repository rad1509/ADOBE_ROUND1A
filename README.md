# PDF Heading Structure Extractor

This project extracts structured **titles and section headings** from PDF documents and outputs them in a standardized **JSON format**.

---

## 📌 What This Does

Given a PDF file such as a proposal, report, or technical document, the script:

1. **Extracts the main title** by identifying the largest text spans on the first two pages.
2. **Detects section headings** (e.g., "Background", "Timeline", "Evaluation Criteria") using font size analysis.
3. **Assigns heading levels** (`H1`, `H2`, `H3`, `H4`) based on relative font size frequencies.
4. **Filters noisy text** and selects lines that likely represent meaningful headings.
5. Outputs the structured result as a `.json` file with this format:

   ```json
   {
     "title": "Main Title of the Document",
     "outline": [
       { "level": "H1", "text": "Section Heading", "page": 1 },
       { "level": "H2", "text": "Subsection Heading", "page": 2 }
     ]
   }
