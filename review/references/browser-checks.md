# Browser checks without project writes

1. Inspect `playwright-cli --help` and needed command help locally; do not guess flags or install dependencies. Read project scripts and the implementer's test URL. Use an isolated test environment and disposable data/accounts. Do not submit real forms, send messages, or mutate production state.
2. Run from a temporary directory outside the project with a unique session. Inspect CLI configuration affecting artifact/profile paths. Keep snapshots, profiles, and caches outside the project. Do not run `playwright-cli install` in the project or use a package runner that silently downloads dependencies.
3. Prefer an already running application. Start a server only when generated files stay outside the original project (redirect outputs or use an isolated temporary test copy) and it uses a safe test environment. Otherwise ask the implementer to prepare it; the browser gate remains incomplete.
4. The local CLI commonly supports this sequence; verify syntax first:

   ```text
   playwright-cli -s=<unique-session> open <test-url>
   playwright-cli -s=<unique-session> snapshot
   playwright-cli -s=<unique-session> click <observed-ref>
   playwright-cli -s=<unique-session> fill <observed-ref> <test-value>
   playwright-cli -s=<unique-session> console
   playwright-cli -s=<unique-session> requests
   playwright-cli -s=<unique-session> close
   ```

   Use fresh snapshot references. Exercise the relevant happy path, meaningful failure/boundary cases, and changed responsive/keyboard behavior when applicable. Record expected/actual outcomes. Inspect relevant console/network failures without attributing unrelated noise to this change.
5. Close only the session/server you started; avoid global close/kill commands. Report scenarios, outcomes, and artifact locations without secrets. Screenshots support visual findings but alone do not establish working behavior.
