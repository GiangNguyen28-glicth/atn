
CREATE TABLE gold_entities (
    canonical_id TEXT PRIMARY KEY,
    schema TEXT,
    properties JSONB,
    referents TEXT[],
    datasets TEXT[],
    first_seen TIMESTAMP,
    last_change TIMESTAMP,
    updated_at TIMESTAMP
);

CREATE TABLE gold_referents (
    referent_id TEXT PRIMARY KEY,
    canonical_id TEXT NOT NULL,
    first_linked_at TIMESTAMP,
    updated_at TIMESTAMP
);



BRONZE = Append Only
SILVER = MERGE INTO

delta_data = select * from gold_entities where updated_at >= logical_date

{
    "id": "ofac-9615", "schema": "Person",
    "referents": [],
    "properties": {
        "name": ["GUN GUN RUSMAN GUNAWAN"],
        "addressEntity": ["NK-giHBkgGYzV56ZnusajSZEe"]
    },
    "last_change": "2026-07-20" 
}

if referents.length
    build_referents_table
    referent = {
        canonical_id = Q123101874,
        referent_id = de-aw-a42a485247368b1a0893e82ec2a4316521f6ff59
    }
    delete gold_entities where canonical_id = de-aw-a42a485247368b1a0893e82ec2a4316521f6ff59
else:
    master_profile = {
        id: opensanction_co-cedula-10060765,
        referents: [co-cedula-10060765]
    }


{
    "id": "Q12509206", "schema": "Person",
    "referents": ["ofac-9615", "unsc-111952", "gb-fcdo-aqd0180"],
    "properties": {
        "name": ["GUN GUN RUSMAN GUNAWAN"],
        "addressEntity": ["NK-giHBkgGYzV56ZnusajSZEe"]
    },
    "last_change": "2026-07-20"
}

entity.id = Q12509206 → chưa có trong gold_entities

Loop qua referents:
  - "ofac-9615" → TÌM THẤY trong gold_entities (record ngày 1!)
      → DELETE gold_entities WHERE canonical_id = 'ofac-9615'
      → UPSERT gold_referents (referent_id='ofac-9615', canonical_id='Q12509206')
  - "unsc-111952", "gb-fcdo-aqd0180"... → chưa từng thấy độc lập
      → vẫn UPSERT gold_referents cho từng cái

INSERT gold_entities (canonical_id='Q12509206', schema=Person, 
                       properties={..., addressEntity: ['NK-giHBk...']})

Rebuild gold_edges cho entity này (xoá edge cũ theo source_id='ofac-9615', 
ghi lại theo source_id='Q12509206'):
  DELETE gold_edges WHERE source_id = 'ofac-9615'
  INSERT gold_edges (source_id='Q12509206', property='addressEntity', 
                      target_id='NK-giHBk...')
