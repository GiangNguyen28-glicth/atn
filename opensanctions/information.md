| File                                  | Có `schema` | Thiếu `schema` |                                            `schema = null` |
| ------------------------------------- | ----------: | -------------: | ---------------------------------------------------------: |
| hr_crime_opensanctions.jsonl          |       10000 |              0 |                                                          0 |
| hr_peps.jsonl                         |       10000 |              0 |                                                          0 |
| hr_sanctions.jsonl                    |        5381 |       **4619** |                                                          0 |
| hr_sanctions_eu.jsonl                 |           0 |      **10000** |                                                          0 |
| hr_sanctions_europa_eu.jsonl          |           0 |      **10000** |                                                          0 |
| hr_sanctions_ofac_treas.jsonl         |           0 |      **10000** |                                                          0 |
| hr_terrorism_opensanctions.jsonl      |       10000 |              0 |                                                          0 |
| hr_wanted_info.jsonl                  |           0 |       **9616** | 0 *(384 record không parse được `information` thành JSON)* |
| hr_wanted_opensanctions.jsonl         |       10000 |              0 |                                                          0 |
| hr_watchlist_crime_fin.jsonl          |       10000 |              0 |                                                          0 |
| hr_watchlist_crime_investigated.jsonl |       10000 |              0 |                                                          0 |


| File                                      | Nội dung                          | Đối tượng chính                          | Ý nghĩa                                                                                                                                         |
| ----------------------------------------- | --------------------------------- | ---------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------- |
| **hr_peps.jsonl**                         | Politically Exposed Persons (PEP) | Person                                   | Danh sách cá nhân có ảnh hưởng chính trị (Tổng thống, Bộ trưởng, Nghị sĩ, Thẩm phán...) phục vụ AML/KYC. Không phải tội phạm hay bị trừng phạt. |
| **hr_sanctions.jsonl**                    | Global Sanctions                  | Person, Company, Organization, Vessel... | Tổng hợp các danh sách sanction từ nhiều quốc gia (OFAC, EU, UN...). Đây là dataset lớn nhất.                                                   |
| **hr_sanctions_eu.jsonl**                 | EU Sanctions                      | Person, Organization                     | Chỉ chứa danh sách sanction của Liên minh Châu Âu. Có vẻ được crawl từ nguồn EU nên thiếu `schema`.                                             |
| **hr_sanctions_europa_eu.jsonl**          | Europa EU Sanctions               | Person, Company                          | Cũng là sanctions của EU nhưng từ portal europa.eu. Thực chất gần giống file trên nhưng khác datasource.                                        |
| **hr_sanctions_ofac_treas.jsonl**         | OFAC SDN/Non-SDN                  | Person, Company, Vessel, Aircraft        | Danh sách sanction của Bộ Tài chính Hoa Kỳ (OFAC).                                                                                              |
| **hr_crime_opensanctions.jsonl**          | Crime Database                    | Person                                   | Người bị truy nã, bị kết án hoặc liên quan tới các vụ án hình sự từ nhiều nguồn OpenSanctions.                                                  |
| **hr_wanted_opensanctions.jsonl**         | Wanted Persons                    | Person                                   | Người đang bị truy nã (Interpol, FBI, Europol...).                                                                                              |
| **hr_wanted_info.jsonl**                  | Wanted Information                | Person                                   | Thông tin bổ sung về các đối tượng truy nã, thường lấy trực tiếp từ website cảnh sát nên không theo schema OpenSanctions.                       |
| **hr_terrorism_opensanctions.jsonl**      | Terrorism                         | Person, Organization                     | Cá nhân hoặc tổ chức có liên quan đến khủng bố hoặc nằm trong terrorist watchlist.                                                              |
| **hr_watchlist_crime_fin.jsonl**          | Financial Crime Watchlist         | Person, Company                          | Đối tượng liên quan tới tội phạm tài chính (money laundering, fraud, corruption...).                                                            |
| **hr_watchlist_crime_investigated.jsonl** | Crime Investigation Watchlist     | Person, Company                          | Các cá nhân/tổ chức đang bị điều tra hình sự nhưng chưa chắc đã bị kết án hoặc sanction.                                                        |

| entityType        |  Số lượng |
| ----------        | --------: |
| Individual=Person | **5.044** |
| Entity=Company    | **4.243** |
| Vessel            |   **415** |
| Aircraft=Airplane |   **298** |


python3 unique_format_by_profile_id.py hr_wanted_info.jsonl