# # Słowa-klucze do ekstrakcji bloków i ich pól
# KEYWORDS = {
#     "symbol": ["lib_id", "at", "property", "uuid"],
#     "wire": ["pts", "stroke"],
#     "text": ["at", "effects", "text"],
#     "connection": ["pinref", "at"]
# }

import copy
from sexpdata import loads, Symbol

# Załóżmy, że template_json to zawartość Twojego pliku template.json wczytana jako słownik
template_json = {
    "version": "20250114",
    "generator": "eeschema",
    "generator_version": "9.0",
    "uuid": "GENERATED-DYNAMICZNIE",
    "paper": "A3",
    "title": "Simple RC Circuit",
    "lib_symbols": [],
    "symbols": []
}

def parse_kicad_sch_sexp(raw_text):
    try:
        # Parsowanie tekstu schematu KiCad do struktury S-expression
        sexp = loads(raw_text)
        
        # Tworzenie kopii szablonu, aby uniknąć modyfikacji oryginału
        parsed_data = copy.deepcopy(template_json)
        
        # Przetwarzanie głównych elementów schematu
        for item in sexp:
            if isinstance(item, list) and item:
                key = str(item[0])
                if key == "lib_symbols":
                    parsed_data["lib_symbols"] = process_lib_symbols(item[1:])
                elif key == "symbol":
                    parsed_data["symbols"].append(process_symbol(item[1:]))
                else:
                    # Obsługa innych kluczowych elementów schematu
                    parsed_data[key] = item[1] if len(item) > 1 else None
        
        return parsed_data
    except Exception as e:
        return {"error": f"Nie udało się sparsować .kicad_sch przez sexpdata: {e}"}

def process_lib_symbols(lib_symbols_data):
    # Przetwarzanie danych lib_symbols
    lib_symbols = []
    for lib_symbol in lib_symbols_data:
        if isinstance(lib_symbol, list):
            lib_symbols.append(str(lib_symbol[0]))  # Przykładowe przetwarzanie
    return lib_symbols

def process_symbol(symbol_data):
    # Przetwarzanie danych symbolu
    symbol = {}
    for item in symbol_data:
        if isinstance(item, list) and item:
            key = str(item[0])
            value = item[1:] if len(item) > 1 else None
            symbol[key] = value
    return symbol
