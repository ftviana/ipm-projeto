import os
import sys
import json
import pandas as pd
import numpy as np
from pathlib import Path

# --- CONFIGURAÇÃO: Colunas essenciais para o Vue ---
KEEP_COLUMNS = [
    'id', 
    'name', 
    'neighbourhood_cleansed',  
    'latitude', 
    'longitude', 
    'room_type', 
    'price', 
    'availability_365', 
    'review_scores_rating', 
    'number_of_reviews',
    'last_review',
    'accommodates',
    'host_id',
    'host_name'
]

def clean_price(value):
    """Remove $ e , do preço e converte para float"""
    if pd.isna(value): return 0
    if isinstance(value, (int, float)): return value
    clean = str(value).replace('$', '').replace(',', '')
    try:
        return float(clean)
    except:
        return 0

def load_csv_optimized(path):
    # Ler apenas as colunas que nos interessam para poupar memória
    # usecols=lambda c: c in KEEP_COLUMNS (lê apenas se a coluna existir)
    try:
        # Primeiro lemos o header para saber quais colunas existem no ficheiro
        df_head = pd.read_csv(path, nrows=0)
        existing_cols = [c for c in KEEP_COLUMNS if c in df_head.columns]
        
        # Agora lemos os dados apenas dessas colunas
        df = pd.read_csv(path, usecols=existing_cols)
        
        # --- LIMPEZA DE DADOS ---
        # 1. Limpar Preços
        if 'price' in df.columns:
            df['price'] = df['price'].apply(clean_price)
            
        # 2. Tratar Ratings (converter NaN para None ou 0)
        if 'review_scores_rating' in df.columns:
            df['review_scores_rating'] = df['review_scores_rating'].fillna(0)

        # 3. Tratar Disponibilidade
        if 'availability_365' in df.columns:
            df['availability_365'] = df['availability_365'].fillna(0).astype(int)

        # 4. Substituir valores vazios/infinitos por None (para JSON válido)
        df = df.replace([np.nan, np.inf, -np.inf], None)
        
        return df.to_dict(orient="records")
        
    except Exception as e:
        print(f"Erro ao processar CSV {path}: {e}")
        return []

def load_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)

def collect_data(base_dir):
    data = {}
    base_dir = Path(base_dir).resolve()

    print(f"🔍 A analisar pasta: {base_dir}")

    for root, _, files in os.walk(base_dir):
        for file in files:
            ext = Path(file).suffix.lower()
            path = Path(root) / file
            
            # Ignorar ficheiros ocultos ou de sistema
            if file.startswith('.'): continue

            # Construir a chave (ex: db/porto/listings.csv -> porto_listings)
            rel_path = path.relative_to(base_dir)
            
            # Truque: Usar UNDERSCORE para o json-server aceitar como rota
            # db/porto/listings.csv -> porto_listings
            key_parts = list(rel_path.with_suffix("").parts)
            key = "_".join(key_parts)

            print(f"   📄 Processando: {file} -> Rota: /{key}")

            try:
                if ext == ".csv":
                    content = load_csv_optimized(path)
                elif ext == ".json":
                    content = load_json(path)
                else:
                    continue
                
                if content:
                    data[key] = content
                    print(f"      ✅ {len(content)} registos importados.")
            except Exception as e:
                print(f"      ❌ Erro em {file}: {e}")

    return data

def main():
    if len(sys.argv) < 2:
        print("Uso: python build_jsondb.py <pasta_db>")
        print("Exemplo: python build_jsondb.py db")
        sys.exit(1)

    base_dir = sys.argv[1].strip()
    output_path = "db.json"

    db_data = collect_data(base_dir)

    print(f"\n💾 A guardar {output_path}...")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(db_data, f, indent=None, ensure_ascii=False) # indent=None para ficheiro mais pequeno
    
    print("🚀 Concluído! Podes correr: npm run server")

if __name__ == "__main__":
    main()