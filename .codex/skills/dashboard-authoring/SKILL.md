# Dashboard Authoring Skill

<!-- SPDX-License-Identifier: GPL-3.0-or-later -->

Use this skill when an agent is building dashboards through the Metabase MCP server.

## Best practices

- Inspect database metadata before creating cards.
- Create a collection for each dashboard project.
- Keep dashboard cards in the same collection as the dashboard unless the user explicitly requests another permission model.
- Give every card and dashboard a clear name and description.
- Prefer reusable questions/cards over embedding one-off logic.
- Use dashboard filters for common slicing dimensions such as date, region, team, customer, and product.
- Lay out dashboards in a 12-column grid with top-level KPIs first, trends next, and detail tables last.
- Use dry-runs before writes on production instances.
