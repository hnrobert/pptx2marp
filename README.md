# PPTX to Marp Converter

A Python-based converter for turning Microsoft PowerPoint `.pptx` files into Marp-compatible Markdown.

## Features

- [x] Convert slide text into Markdown
- [x] Marp frontmatter generation (`marp: true`, `paginate: true`)
- [x] Slide separator generation (`---`)
- [x] Export picture shapes into `assets/`
- [x] Convert simple tables to Markdown tables
- [x] Command line interface
- [x] Batch conversion with wildcard support
- [x] Project packaging with `pyproject.toml`
- [x] GitHub Action for release and PyPI publish

## Installation

### Install from source

```bash
git clone https://github.com/HNRobert/pptx2marp.git
cd pptx2marp
pip install -e .
```

### Install only runtime dependency

```bash
pip install python-pptx
```

## Usage

### Command line tool

After installation, use `pptx2marp`:

```bash
# Convert a single file
pptx2marp demo.pptx

# Convert and write to output file
pptx2marp demo.pptx -o demo.md

# Batch conversion to output directory
pptx2marp *.pptx -o out/

# Override Marp title field
pptx2marp demo.pptx -o demo.md -t "Team Weekly Report"

# Verbose logs
pptx2marp demo.pptx -v
```

### Python script entry

```bash
python main.py demo.pptx -o demo.md
```

## Output structure

With default behavior, converting `slides.pptx` creates:

```text
slides/
	slides.md
	assets/
		slide001_img01.png
		slide002_img01.jpg
```

If a slide contains no extractable content, converter outputs:

```markdown
<!-- empty slide -->
```

## Development

Build distribution artifacts:

```bash
python -m pip install --upgrade build
python -m build --sdist --wheel
```

## License

MIT
