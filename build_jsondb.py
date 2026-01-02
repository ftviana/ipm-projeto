import sys
import json
import pandas as pd
import numpy as np
from pathlib import Path

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

CITIES = ['porto', 'lisbon', 'barcelona']
PERIODS = ['2025-03', '2025-06', '2025-09']
PERIOD_LABELS = {
    '2025-03': 'Mar 2025',
    '2025-06': 'Jun 2025',
    '2025-09': 'Sep 2025'
}

def clean_price(value):
    if pd.isna(value): return 0
    if isinstance(value, (int, float)): return value
    clean = str(value).replace('$', '').replace(',', '')
    try:
        return float(clean)
    except:
        return 0

def load_csv_optimized(path):
    try:
        df_head = pd.read_csv(path, nrows=0)
        existing_cols = [c for c in KEEP_COLUMNS if c in df_head.columns]
        df = pd.read_csv(path, usecols=existing_cols)
        
        if 'price' in df.columns:
            df['price'] = df['price'].apply(clean_price)
        if 'review_scores_rating' in df.columns:
            df['review_scores_rating'] = df['review_scores_rating'].fillna(0)
        if 'availability_365' in df.columns:
            df['availability_365'] = df['availability_365'].fillna(0).astype(int)
        
        df = df.replace([np.nan, np.inf, -np.inf], None)
        return df
        
    except Exception as e:
        print(f"   ❌ Error processing {path}: {e}")
        return pd.DataFrame()

def compute_metrics(df):
    if df.empty:
        return None
    
    count = len(df)
    avg_price = df['price'].mean() if 'price' in df.columns else 0
    
    occupancy = 0
    if 'availability_365' in df.columns:
        occupancy = ((365 - df['availability_365'].mean()) / 365 * 100)
    
    avg_rating = 0
    reviews_count = 0
    if 'review_scores_rating' in df.columns:
        rated = df[df['review_scores_rating'] > 0]
        if len(rated) > 0:
            avg_rating = rated['review_scores_rating'].mean()
            reviews_count = rated['number_of_reviews'].sum() if 'number_of_reviews' in rated.columns else 0
    
    return {
        'count': int(count),
        'avgPrice': round(avg_price, 2),
        'occupancyRate': round(occupancy, 1),
        'avgRating': round(avg_rating, 2),
        'reviewsCount': int(reviews_count)
    }

def build_historical_data(base_dir):
    data = {}
    base_dir = Path(base_dir).resolve()
    
    print(f"🔍 Analyzing folder: {base_dir}\n")
    
    for city in CITIES:
        print(f"📍 Processing {city.upper()}...")
        
        city_history = []
        
        for period in PERIODS:
            csv_path = base_dir / city / period / 'listings.csv'
            period_key = period.replace("-", "_")
            
            if csv_path.exists():
                print(f"   📄 {period}/listings.csv", end="")
                df = load_csv_optimized(csv_path)
                
                if not df.empty:
                    metrics = compute_metrics(df)
                    metrics['period'] = period
                    metrics['label'] = PERIOD_LABELS[period]
                    city_history.append(metrics)
                    print(f" → {metrics['count']} listings")
                    
                    data[f"{city}_{period_key}_listings"] = df.to_dict(orient="records")
                else:
                    print(" → Empty or error")
            else:
                print(f"   ⚠️  {period}/listings.csv not found")
        
        if city_history:
            data[f"{city}_history"] = city_history
            print(f"   ✅ {len(city_history)} periods loaded")
        
        print()
    
    return data

def main():
    if len(sys.argv) < 2:
        print("Usage: python build_jsondb.py <db_folder>")
        print("Example: python build_jsondb.py db")
        sys.exit(1)

    base_dir = sys.argv[1].strip()
    output_path = "db.json"

    db_data = build_historical_data(base_dir)

    print(f"💾 Saving {output_path}...")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(db_data, f, indent=None, ensure_ascii=False)
    
    print("\n🚀 Done! API endpoints created:")
    for key in db_data.keys():
        print(f"   GET /{key}")
    print("\nRun: npm run server")

if __name__ == "__main__":
    main()