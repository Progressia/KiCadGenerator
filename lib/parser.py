import re

def parse_kicad_sym(raw_text):
    """
    Parsuje plik .kicad_sym do uproszczonego formatu JSON.
    """
    symbols = []

    # Znajdź bloki (symbol "...")
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
    Parsuje plik .kicad_sch do uproszczonego formatu JSON.
    Na razie placeholder.
    """
    return {
        "info": "Parser .kicad_sch w przygotowaniu",
        "lines": raw_text.splitlines()
    }