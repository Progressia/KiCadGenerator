import re
from sexpdata import loads, Symbol

# Słowa-klucze do ekstrakcji bloków i ich pól
KEYWORDS = {
    "meta": ["version", "generator", "generator_version", "uuid", "paper", "title"],
    "lib_symbols": ["symbol"],
    "symbols": ["lib_id", "at", "property", "uuid"]
}

def parse_kicad_sym(raw_text):
    symbols = []
    symbol_blocks = re.findall(r'\(symbol\s+"[^"]+".*?\n\)', raw_text, re.DOTALL)

    for block in symbol_blocks:
        name_match = re.search(r'\(symbol\s+"([^"]+)"', block)
        name = name_match.group(1) if name_match else "Unnamed"
        symbols.append({
            "name": name,
            "raw": block.strip()
        })

    return {
        "symbols": symbols
    }

def parse_kicad_text(raw_text, sections=["meta", "lib_symbols", "symbols"]):
    try:
        sexp = loads(raw_text)
        result = {}

        # METADANE (z poziomu root tree, nie flat)
        if "meta" in sections and "meta" in KEYWORDS:
            result["meta"] = extract_meta_fields(sexp, KEYWORDS["meta"])

        # Pozostałe sekcje wymagają spłaszczonego drzewa
        flat_tree = parse_sexp_tree_flat(sexp)

        for section in sections:
            if section == "meta" or section not in KEYWORDS:
                continue
            blocks = extract_blocks(flat_tree, "symbol") if section == "symbols" else extract_blocks(flat_tree, section)
            result[section] = [extract_fields_from_block(b, KEYWORDS[section]) for b in blocks]

        return result

    except Exception as e:
        return {"error": f"Nie udało się sparsować pliku przez sexpdata: {e}"}

def parse_sexp_tree_flat(sexp):
    if isinstance(sexp, list):
        return [parse_sexp_tree_flat(s) for s in sexp]
    elif isinstance(sexp, Symbol):
        return str(sexp)
    else:
        return sexp

def flatten_symbol_line(symbol_data):
    if isinstance(symbol_data, list):
        return " ".join(str(item) if not isinstance(item, list) else flatten_symbol_line(item) for item in symbol_data)
    return str(symbol_data)

def extract_blocks(flat_tree, section="symbol"):
    results = []
    for item in flat_tree:
        if isinstance(item, list) and len(item) > 0 and item[0] == section:
            results.append(item)
    return results

def extract_fields_from_block(block, fields):
    result = {}
    for item in block:
        if isinstance(item, list) and len(item) > 0:
            key = str(item[0])
            if key in fields:
                result[key] = item[1:]
    return result

def extract_meta_fields(sexp_tree, fields):
    result = {}
    for item in sexp_tree:
        if isinstance(item, list) and len(item) > 0:
            key = str(item[0])
            if key in fields:
                result[key] = item[1] if len(item) > 1 else None
    return result
