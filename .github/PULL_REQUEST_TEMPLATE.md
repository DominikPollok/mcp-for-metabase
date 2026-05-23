## Summary

Describe the change.

## Safety

- [ ] No Metabase mutation bypasses `SafetyPolicy`.
- [ ] New write-capable behavior supports `dry_run`.
- [ ] Destructive/admin behavior requires `all-writes` and `confirm=true`.
- [ ] Mutating requests route through `MetabaseClient.request`.

## Tests

- [ ] `ruff format --check .`
- [ ] `ruff check .`
- [ ] `mypy src`
- [ ] `pytest`
- [ ] Docs updated, if behavior changed.
