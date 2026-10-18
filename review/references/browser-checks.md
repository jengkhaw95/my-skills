# Browser checks without project writes

Use the browser automation the harness provides. Any tool is acceptable if it can navigate, inspect the page, interact, and expose console/network errors, and if its artifacts can stay outside the project. Examples include playwright-cli, a Playwright or Chrome DevTools MCP server, and a built-in browser tool.

1. **Discover the capability.** Inspect the tool's help locally; do not guess flags or install dependencies. Read project scripts and the implementer's test URL. Use an isolated test environment and disposable data/accounts. Do not submit real forms, send messages, or mutate production state.
2. **Isolate artifacts.** Run from a temporary directory outside the project with a unique session/profile. Inspect configuration affecting artifact/profile paths. Keep snapshots, profiles, screenshots, downloads, and caches outside the project. Do not run a browser install command in the project or use a package runner that silently downloads dependencies.
3. **Prefer an already running application.** Start a server only when generated files stay outside the original project (redirect outputs or use an isolated temporary test copy) and it uses a safe test environment. Otherwise ask the implementer to prepare it; the browser gate remains incomplete.
4. **Exercise the scope.** Navigate to the test URL, inspect the accessibility/DOM snapshot, interact using fresh references, and read console and network output. Exercise the relevant happy path, meaningful failure/boundary cases, and changed responsive/keyboard behavior when applicable. Record expected/actual outcomes. Inspect relevant console/network failures without attributing unrelated noise to this change.
5. **Clean up.** Close only the session/server you started; avoid global close/kill commands. Report scenarios, outcomes, and artifact locations without secrets. Screenshots support visual findings but alone do not establish working behavior.

## Example: playwright-cli

If the harness provides `playwright-cli`, verify syntax and flags against its local help first. A common sequence is:

```text
playwright-cli -s=<unique-session> open <test-url>
playwright-cli -s=<unique-session> snapshot
playwright-cli -s=<unique-session> click <observed-ref>
playwright-cli -s=<unique-session> fill <observed-ref> <test-value>
playwright-cli -s=<unique-session> console
playwright-cli -s=<unique-session> requests
playwright-cli -s=<unique-session> close
```

Adapt command names and flags to the installed version. Use fresh snapshot references. If the tool exposes the same capabilities under a different interface, use that interface instead.
