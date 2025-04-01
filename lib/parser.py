import re
from sexpdata import loads, Symbol

# Słowa-klucze do ekstrakcji bloków i ich pól
KEYWORDS = {
    "meta": ["version", "generator", "generator_version", "uuid", "paper", "title"],
    "symbol": ["lib_id", "at", "property", "uuid"],
    "wire": ["pts", "stroke"],
    "text": ["at", "effects", "text"],
    "connection": ["pinref", "at"]
}

def extract_meta_fields(sexp_tree, fields):
    result = {}
    for item in sexp_tree:
        if isinstance(item, list) and len(item) > 0:
            key = str(item[0])
            if key in fields:
                result[key] = item[1] if len(item) > 1 else None
    return result

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

def extract_blocks(flat_tree, keyword="symbol"):
    results = []
    for item in flat_tree:
        if isinstance(item, list) and len(item) > 0 and item[0] == keyword:
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

def parse_kicad_sym_sexp(raw_text):
    try:
        sexp = loads(raw_text)
        flat = parse_sexp_tree_flat(sexp)
        symbols = extract_blocks(flat, "symbol")
        parsed = [extract_fields_from_block(s, KEYWORDS["symbol"]) for s in symbols]
        return {"symbols": parsed}
    except Exception as e:
        return {"error": f"Nie udało się sparsować .kicad_sym przez sexpdata: {e}"}

def parse_kicad_sch_sexp(raw_text):
    try:
        sexp = loads(raw_text)
        flat = parse_sexp_tree_flat(sexp)
        symbols = extract_blocks(flat, "symbol")
        parsed = [extract_fields_from_block(s, KEYWORDS["symbol"]) for s in symbols]
        return {"symbols": parsed}
    except Exception as e:
        return {"error": f"Nie udało się sparsować .kicad_sch przez sexpdata: {e}"}