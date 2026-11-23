<!--
The index of the problem space: every subdomain with its type, its glossary and its subdomain map,
and how the subdomains relate. There is no second index of the glossaries. Whoever creates a
glossary (domain-init, the glossary skill in domain-interview) adds its subdomain's row in
the same change, with `–` in the column Subdomain map; whoever creates the subdomain map
(assets/subdomain-map.md: domain-init, functional-requirement) sets its link. functional-requirement adds subdomains and relationships an AC needs. The methodology glossary
(‹methodology-glossary›) stands in the config, not here.
This comment is not copied into the map.
-->
# Domain Map

<The domain in one sentence: who uses the software and what for.>

## Subdomains

| Subdomain | Type | Glossary | Subdomain map | Description |
|---|---|---|---|---|
| <subdomain> | <Core \| Supporting \| Generic \| open> | [<file>.md](../glossaries/<file>.md) | [subdomain-map.md](<subdomain>/subdomain-map.md) or – | <what belongs to it in business terms, one sentence> |

## Relationships

| From | To | Description |
|---|---|---|
| <subdomain> | <subdomain> | <what flows or is triggered, in glossary terms> |
