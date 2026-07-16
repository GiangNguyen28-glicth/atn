# Xử lý Canonical Entity khi đồng bộ dữ liệu OpenSanctions

Tài liệu này mô tả cách hệ thống xử lý khi OpenSanctions thay đổi Canonical Entity trong các lần đồng bộ incremental.

---

# Case 1 - Xuất hiện Canonical Entity mới

## Mô tả

Ở lần đồng bộ đầu tiên, một Person được publish độc lập với ID `ofac-9615`.

Đến lần đồng bộ tiếp theo, OpenSanctions xác định Person này trùng với nhiều nguồn dữ liệu khác và tạo ra một Canonical Entity mới `Q12509206`.

---

## Trạng thái ban đầu

### Bronze (Append Only)

| id | schema |
|----|--------|
| ofac-9615 | Person |

---

### entities_state

| canonical_id | schema | name |
|--------------|--------|------|
| ofac-9615 | Person | Gun Gun Rusman Gunawan |

---

### entities_referents

> Chưa có dữ liệu

---

## Incremental Record

```json
{
  "id": "Q12509206",
  "schema": "Person",
  "referents": [
    "ofac-9615",
    "unsc-111952",
    "gb-fcdo-aqd0180"
  ],
  "properties": {
    "name": [
      "GUN GUN RUSMAN GUNAWAN"
    ],
    "addressEntity": [
      "NK-giHBkgGYzV56ZnusajSZEe"
    ]
  },
  "last_change": "2026-07-20"
}
```

> Lưu ý:
>
> - `ofac-9615` trước đây là Canonical Entity.
> - OpenSanctions đã rewrite toàn bộ nested entity (`addressEntity`) sang Canonical ID mới.

---

# Bước 1 - Xác định Canonical Entity cũ

Loop qua toàn bộ `referents`.

| Referent | Có tồn tại trong entities_state? |
|----------|----------------------------------|
| ofac-9615 | ✅ Có |
| unsc-111952 | ❌ Không |
| gb-fcdo-aqd0180 | ❌ Không |

---

## entities_state trước khi xử lý

| canonical_id |
|--------------|
| ofac-9615 |

---

## Action

```text
DELETE canonical_id = 'ofac-9615'
```

---

## entities_state sau khi xử lý

> Không còn dữ liệu

---

# Bước 2 - Upsert Canonical Entity mới

## entities_state trước khi xử lý

> Không còn dữ liệu

---

## Action

```text
UPSERT

canonical_id = Q12509206
```

---

## entities_state sau khi xử lý

| canonical_id | schema |
|--------------|--------|
| Q12509206 | Person |

---

# Bước 3 - Đồng bộ Referent Mapping

## entities_referents trước khi xử lý

> Không có dữ liệu

---

## Action

```text
ofac-9615      -> Q12509206

unsc-111952    -> Q12509206

gb-fcdo-aqd0180 -> Q12509206
```

---

## entities_referents sau khi xử lý

| referent_id | canonical_id |
|-------------|--------------|
| ofac-9615 | Q12509206 |
| unsc-111952 | Q12509206 |
| gb-fcdo-aqd0180 | Q12509206 |

---

# Trạng thái cuối cùng

## Bronze

| id |
|----|
| ofac-9615 |
| Q12509206 |

> Bronze luôn là Append Only.

---

## entities_state

| canonical_id |
|--------------|
| Q12509206 |

---

## entities_referents

| referent_id | canonical_id |
|-------------|--------------|
| ofac-9615 | Q12509206 |
| unsc-111952 | Q12509206 |
| gb-fcdo-aqd0180 | Q12509206 |

---

# Case 2 - Canonical Entity đã tồn tại

## Mô tả

Canonical Entity đã được tạo từ lần đồng bộ trước.

Ở lần đồng bộ tiếp theo, OpenSanctions chỉ bổ sung thêm Referent mới.

Không phát sinh Canonical Entity mới.

---

## Trạng thái ban đầu

### Bronze

| id |
|----|
| ofac-9615 |
| Q12509206 |

---

### entities_state

| canonical_id |
|--------------|
| Q12509206 |

---

### entities_referents

| referent_id | canonical_id |
|-------------|--------------|
| ofac-9615 | Q12509206 |
| unsc-111952 | Q12509206 |

---

## Incremental Record

```json
{
  "id": "Q12509206",
  "schema": "Person",
  "referents": [
    "ofac-9615",
    "unsc-111952",
    "gb-fcdo-aqd0180",
    "eu-fsf-001"
  ],
  "properties": {
    "name": [
      "GUN GUN RUSMAN GUNAWAN"
    ]
  },
  "last_change": "2026-07-25"
}
```

---

# Bước 1 - Xác định Canonical Entity cũ

Loop qua toàn bộ Referents.

| Referent | Có tồn tại trong entities_state? |
|----------|----------------------------------|
| ofac-9615 | ❌ Không |
| unsc-111952 | ❌ Không |
| gb-fcdo-aqd0180 | ❌ Không |
| eu-fsf-001 | ❌ Không |

Không tìm thấy Canonical Entity nào cần thay thế.

---

## entities_state

Không thay đổi.

| canonical_id |
|--------------|
| Q12509206 |

---

# Bước 2 - Cập nhật Canonical Entity

Do `canonical_id = Q12509206` đã tồn tại.

Action:

```text
UPSERT

canonical_id = Q12509206
```

Các thông tin mới (properties, datasets, last_change...) sẽ được cập nhật nếu thay đổi.

---

## entities_state sau khi xử lý

| canonical_id |
|--------------|
| Q12509206 |

---

# Bước 3 - Đồng bộ Referent Mapping

## entities_referents trước khi xử lý

| referent_id | canonical_id |
|-------------|--------------|
| ofac-9615 | Q12509206 |
| unsc-111952 | Q12509206 |

---

## Action

```text
UPSERT

ofac-9615       -> Q12509206

unsc-111952     -> Q12509206

gb-fcdo-aqd0180 -> Q12509206

eu-fsf-001      -> Q12509206
```

Các mapping đã tồn tại sẽ không thay đổi.

Chỉ bổ sung các Referent mới.

---

## entities_referents sau khi xử lý

| referent_id | canonical_id |
|-------------|--------------|
| ofac-9615 | Q12509206 |
| unsc-111952 | Q12509206 |
| gb-fcdo-aqd0180 | Q12509206 |
| eu-fsf-001 | Q12509206 |

---

# Trạng thái cuối cùng

## Bronze

| id |
|----|
| ofac-9615 |
| Q12509206 |

---

## entities_state

| canonical_id |
|--------------|
| Q12509206 |

---

## entities_referents

| referent_id | canonical_id |
|-------------|--------------|
| ofac-9615 | Q12509206 |
| unsc-111952 | Q12509206 |
| gb-fcdo-aqd0180 | Q12509206 |
| eu-fsf-001 | Q12509206 |

---

# Kết quả

Thiết kế này đảm bảo:

- Bronze luôn là **Append Only**, không cập nhật hoặc xóa dữ liệu lịch sử.
- `entities_state` chỉ lưu **Canonical Entity hiện tại**.
- `entities_referents` là bảng ánh xạ từ mọi Referent về Canonical Entity tương ứng.
- Khi OpenSanctions thay đổi Canonical Entity, hệ thống chỉ cần cập nhật `entities_state` và đồng bộ lại `entities_referents`.
- Các hệ thống downstream có thể tra cứu bằng bất kỳ Referent nào mà vẫn nhận được Canonical Entity mới nhất.