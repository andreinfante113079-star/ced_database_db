#!/usr/bin/env python3
"""
Build script for Primary Structures dashboard.

Downloads the latest Excel file from Google Drive, cleans the data,
and emits projects.json next to the dashboard HTML.

Environment variables required:
  GDRIVE_FILE_ID         - the file ID from the Google Drive share link
  GOOGLE_CREDENTIALS_JSON - service account credentials (JSON string)
"""
import os
import io
import json
import re
import sys
import numpy as np
import pandas as pd
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload


FILE_ID = os.environ.get('GDRIVE_FILE_ID', '').strip()
CREDS_JSON = os.environ.get('GOOGLE_CREDENTIALS_JSON', '').strip()
OUTPUT_DIR = os.environ.get('OUTPUT_DIR', 'public')

if not FILE_ID:
    sys.exit("ERROR: GDRIVE_FILE_ID env var not set")
if not CREDS_JSON:
    sys.exit("ERROR: GOOGLE_CREDENTIALS_JSON env var not set")


def download_excel():
    """Download the .xlsx file from Google Drive using a service account."""
    creds = service_account.Credentials.from_service_account_info(
        json.loads(CREDS_JSON),
        scopes=['https://www.googleapis.com/auth/drive.readonly']
    )
    service = build('drive', 'v3', credentials=creds)

    request = service.files().get_media(fileId=FILE_ID)
    buf = io.BytesIO()
    downloader = MediaIoBaseDownload(buf, request)
    done = False
    while not done:
        _, done = downloader.next_chunk()
    buf.seek(0)
    print(f"  Downloaded {buf.getbuffer().nbytes} bytes from Google Drive")
    return buf


def parse_year(v):
    if pd.isna(v):
        return None
    m = re.search(r'(\d{4})', str(v))
    return int(m.group(1)) if m else None


def num(v):
    if pd.isna(v):
        return None
    try:
        f = float(v)
        if np.isnan(f):
            return None
        return int(f) if f.is_integer() else round(f, 4)
    except (ValueError, TypeError):
        return None


def text(v):
    if pd.isna(v):
        return None
    s = str(v).strip()
    return s if s else None


def clean_dataframe(df):
    """Normalize categorical duplicates and trim whitespace."""
    df = df.drop(
        columns=[c for c in ['Unnamed: 0', 'Unnamed: 3', 'Unnamed: 26'] if c in df.columns],
        errors='ignore'
    )
    df = df.dropna(subset=['PROJECT']).reset_index(drop=True)

    for c in df.select_dtypes(include='object').columns:
        df[c] = df[c].astype(str).str.strip()
        df[c] = df[c].replace({'nan': np.nan, 'NaN': np.nan, '': np.nan})

    df['BUILDING CATEGORY'] = df['BUILDING CATEGORY'].replace({
        'MIXED USE BLDGS': 'MIXED USE',
        'STANDARD FACTORY': 'PRODUCTION PLANT',
    })
    df['DESIGNER'] = df['DESIGNER'].replace({
        'JOSE ROE T. BAEL - STED': 'JOSE ROE T. BAEL',
        'WALLACE': 'ENGR. WALLACE D. LESTANO, F. ASEP',
    })
    df['TYPE OF OCCUPANCY'] = df['TYPE OF OCCUPANCY'].replace({
        'RESIDENTIAL & HOTEL': 'RESIDENTIAL',
    })
    df['TYPE OF FOUNDATION'] = df['TYPE OF FOUNDATION'].replace({
        'MAT FOOTING + ISOLATED FTG': 'ISOLATED FTG + MAT FOOTING',
        'ISOLATED FTG AND MAT FOOTING': 'ISOLATED FTG + MAT FOOTING',
    })

    df['YEAR_START'] = df['YEAR'].apply(parse_year)
    return df


def row_to_dict(r):
    return {
        'name': text(r.get('PROJECT')),
        'owner': text(r.get('OWNER')),
        'location': text(r.get('LOCATION')),
        'year': text(r.get('YEAR')),
        'yearStart': num(r.get('YEAR_START')),
        'occupancy': text(r.get('TYPE OF OCCUPANCY')),
        'category': text(r.get('BUILDING CATEGORY')),
        'designer': text(r.get('DESIGNER')),
        'tfa': num(r.get('TFA (sqm)')),
        'footprint': num(r.get('BUILDING FOOTPRINT')),
        'units': num(r.get('NO. OF UNITS')),
        'height': num(r.get('BUILDING HEIGHT')),
        'levels': num(r.get('NO. OF LEVELS')),
        'foundation': text(r.get('TYPE OF FOUNDATION')),
        'approach': text(r.get('CONSTRUCTION APPROACH')),
        'concrete': num(r.get('CONCRETE, cu.m')),
        'rebar': num(r.get('REBAR, kgs.')),
        'forms': num(r.get('FORMS, sq.m')),
        'cumTfa': num(r.get('CUM/TFA')),
        'kgTfa': num(r.get('KG/TFA')),
        'sqmTfa': num(r.get('SQM/TFA')),
    }


def main():
    print("→ Downloading Excel from Google Drive...")
    excel_buf = download_excel()

    print("→ Reading 'Database Library' sheet...")
    df = pd.read_excel(excel_buf, sheet_name='Database Library', header=4)

    print(f"→ Cleaning data (raw: {len(df)} rows)...")
    df = clean_dataframe(df)
    print(f"  After cleanup: {len(df)} projects")

    projects = [row_to_dict(row) for _, row in df.iterrows()]

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    out_path = os.path.join(OUTPUT_DIR, 'projects.json')

    from datetime import datetime, timezone
    payload = {
        'updatedAt': datetime.now(timezone.utc).isoformat(),
        'count': len(projects),
        'projects': projects,
    }

    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)

    print(f"✓ Wrote {out_path} ({len(projects)} projects)")


if __name__ == '__main__':
    main()
