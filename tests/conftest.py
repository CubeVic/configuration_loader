from hypothesis.strategies import one_of, text, integers, lists, dictionaries, recursive, booleans, sampled_from


basic_types = one_of(text(max_size=30), integers(), lists(elements=text(max_size=30)))
key_characteristics_toml = text(min_size=1, alphabet="abcdefghijklmnopqrstuvwxyz0123456789_", max_size=20)
config_strategy = recursive(
    dictionaries(
        keys=key_characteristics_toml, values=basic_types, min_size=1),
    lambda children: dictionaries(keys=key_characteristics_toml, values=children, min_size=1),
    max_leaves=10,
)

# Primitive types allowed in TOML
primitive = one_of(
    text(min_size=1, max_size=20, alphabet="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"),
)

# Only allow lists of strings or ints (TOML-safe arrays)
array = one_of(
    lists(text(min_size=1, max_size=10, alphabet="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"), min_size=1, max_size=5),
    lists(integers(min_value=1, max_value=100), min_size=1, max_size=5),
    lists(booleans(), min_size=1, max_size=5),
)

toml_value = one_of(primitive, array)

# Valid TOML key names: lowercase letters, digits, and underscores
key_characteristics_toml = text(
    min_size=1,
    max_size=20,
    alphabet="abcdefghijklmnopqrstuvwxyz"
)

# Section names
section_names = sampled_from(["base", "etc", "database", "logging", "features"])

# One section = dict of key-values
section_dict = dictionaries(
    keys=key_characteristics_toml,
    values=toml_value,
    min_size=1,
    max_size=5
)

# Final strategy: dict of sections
config_strategy_with_sections = dictionaries(
    keys=section_names,
    values=section_dict,
    min_size=1,
    max_size=4
)
