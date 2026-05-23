# Example Dashboard Build Prompt

Use the Metabase MCP server to build a sales operations dashboard.

1. Run `metabase_connection_test`.
2. Run `metabase_list_databases` and inspect the target database metadata.
3. Create a collection named `Sales Operations`.
4. Create questions/cards for revenue, orders, average order value, conversion rate, and top customers.
5. Create a dashboard named `Sales Operations Overview`.
6. Add cards in a 12-column grid with KPI cards on the first row and trend/detail cards below.
7. Add dashboard filters for date range and customer segment.
8. Keep all cards in the same collection as the dashboard unless permissions require otherwise.
9. Use `dry_run=true` before writes, then repeat with writes enabled.
