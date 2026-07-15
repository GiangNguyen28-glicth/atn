import sys
import json
from followthemoney import model
from followthemoney.proxy import EntityProxy
from followthemoney.types import registry


class Transformer:
    def __init__(self):
        # Cache tất cả entity parse được trong 1 lần transform (cả entity cha lẫn nested)
        self.entities: dict[str, EntityProxy] = {}

    def transform(self, raw_data: dict):
        """
        Entry point: raw_data là message gốc (kafka record...).
        Bạn tự parse field "information" (json string) ra dict FTM rồi gọi to_ftm_model.
        """
        info = raw_data.get("information")
        if isinstance(info, str):
            info = json.loads(info)

        if not info:
            return None

        schema = info.get("schema")
        entity = self.to_ftm_model(schema, info)
        return entity

    def to_ftm_model(self, schema: str, raw_data: dict) -> EntityProxy:
        """
        Parse 1 dict dạng FTM (có id/schema/properties) thành EntityProxy.
        Tự động đệ quy nếu gặp property kiểu 'entity' mà value là nested dict.
        """
        ftm_schema = model.get(schema)
        if ftm_schema is None:
            print(f"[WARN] Unknown schema: {schema}, skip entity {raw_data.get('id')}")
            return None

        entity = model.make_entity(ftm_schema)
        entity.id = raw_data.get("id")

        properties = raw_data.get("properties", {}) or {}

        for name, values in properties.items():
            prop = ftm_schema.get(name)
            if prop is None:
                # property không tồn tại trong schema này -> bỏ qua
                continue

            if not isinstance(values, list):
                values = [values]

            for value in values:
                if value is None or value == "":
                    continue
                try:
                    resolved = self._resolve_value(prop, value)
                    if resolved is None:
                        continue
                    if prop.stub:
                        continue
                    entity.add(prop.name, resolved)
                except Exception as e:
                    print(f"[ERROR] prop='{name}' value={value!r} entity_id={entity.id}: {e}")

        self._register_entity(entity)
        return entity

    def _resolve_value(self, prop, value):
        """
        Nếu prop là kiểu entity-reference:
          - value là dict đầy đủ -> đây là nested entity thật sự, đệ quy parse,
            trả về id của nested entity để gắn vào entity cha.
          - value là string -> đã là id sẵn, giữ nguyên.
        Ngược lại trả raw value (string/number/date...).
        """
        if prop.type == registry.entity:
            if isinstance(value, dict):
                nested_schema = value.get("schema")
                if not nested_schema:
                    print(f"[WARN] Nested entity thiếu 'schema', bỏ qua: {value}")
                    return None
                nested_entity = self.to_ftm_model(nested_schema, value)
                return nested_entity if nested_entity else None
            return value  # đã là id string

        return value

    def _register_entity(self, entity: EntityProxy):
        if entity is None or entity.id is None:
            return
        existing = self.entities.get(entity.id)
        if existing is not None:
            existing.merge(entity)
        else:
            self.entities[entity.id] = entity