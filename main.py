import followthemoney
print(followthemoney.__version__)

from followthemoney import model

schema = model.get("LegalEntity")
prop = schema.get("sanctions")

print(prop)
print("stub =", prop.stub)
print("type =", prop.type)
print("range =", getattr(prop, "range", None))
print("reverse =", getattr(prop, "reverse", None))