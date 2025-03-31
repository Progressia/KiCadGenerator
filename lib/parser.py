import re
from sexpdata import loads, Symbol

def parse_kicad_sym(raw_text):
    """
    Parsuje plik .kicad_sym do uproszczonego formatu JSON (regex).
    """
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

def parse_kicad_sch(raw_text):
    """
    Parsuje plik .kicad_sch do uproszczonego formatu JSON (regex).
    Na razie placeholder.
    """
    return {
        "info": "Parser .kicad_sch w przygotowaniu",
        "lines": raw_text.splitlines()
    }

def parse_kicad_sym_sexp(raw_text):
    """
    Parser .kicad_sym z wykorzystaniem biblioteki sexpdata
    """
    try:
        data = loads(raw_text)
        return {"sexp": data}
    except Exception as e:
        return {"error": f"Nie udało się sparsować .kicad_sym przez sexpdata: {e}"}

def parse_kicad_sch_sexp(raw_text):
    """
    Parser .kicad_sch z wykorzystaniem biblioteki sexpdata
    """
    try:
        data = loads(raw_text)
        return {"sexp": data}
    except Exception as e:
        return {"error": f"Nie udało się sparsować .kicad_sch przez sexpdata: {e}"}
