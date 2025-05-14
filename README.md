# daily-wikipedia-md

A Python tool that grabs a random Wikipedia article, extracts its title, headers, and subheaders, and generates a 
well structured markdown file, formatted for Obsidian or other markdown editors.

## Features
- Fetches 100% random Wikipedia articles 
- Parses noteworthy headers while leaving sections like "references" or "external links" behind
- Generates markdown file with current date, time, and article title.
- Easily configurable file path and name

## Requirments
- Only requires a recent version of Python (3.x)

## How to Use

Clone the repo:

```bash
git clone https://github.com/SpencerF718/daily-wikipedia-md.git
cd daily-wikipedia-md
``` 

Then run:

```bash
python main.py
```

## Example Output

```markdown
2025-05-14 15:30:00
**Related Topics**:
**Link**: https://en.wikipedia.org/wiki/Example_Article
# Example Article #wikipedia

## History

### Early Years

## Legacy

```

