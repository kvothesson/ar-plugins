---
description: Configura CI/CD en un repo plugin de ar-plugins. Agrega conventional commits, check de version bump y branch protection en master. Usalo con /ar-plugins:setup-ci <owner/repo>.
---

# Skill: /ar-plugins:setup-ci

Dado un repo plugin, agrega:
- Workflow de conventional commits (commitlint)
- Workflow de version bump (solo en repos con `plugin.json`)
- `.commitlintrc.json`
- Branch protection ruleset en `master` (PR obligatorio + checks requeridos)

---

## Uso

```
/ar-plugins:setup-ci kvothesson/<nombre>
```

Si no se pasa repo, preguntar al usuario cuál quiere configurar.

---

## Paso 1 — Verificar scope `workflow`

```bash
gh auth status 2>&1 | grep "Token scopes"
```

Si el output **no contiene** `workflow`:

```
Para agregar workflows necesito el scope `workflow` en tu token de GitHub.
Corré esto y aprobá el acceso en el browser:

  gh auth refresh -s workflow

Avisame cuando esté listo.
```

Detener y esperar confirmación del usuario antes de continuar.

---

## Paso 2 — Detectar tipo de repo

```bash
gh api repos/<owner>/<repo>/contents/.claude-plugin/plugin.json 2>&1 | grep -c '"content"'
```

- Si retorna `1` → **repo plugin** → setup completo (version-bump + commitlint + ruleset)
- Si retorna `0` → **repo sin plugin.json** → solo commitlint + ruleset (ej: `ar-plugins`)

---

## Paso 3 — Clonar y crear branch

```bash
gh repo clone <owner>/<repo> /tmp/<repo>-setup-ci
cd /tmp/<repo>-setup-ci
git checkout -b ci/setup-ci
```

---

## Paso 4 — Agregar archivos

### `.commitlintrc.json` (siempre)

```bash
cat > /tmp/<repo>-setup-ci/.commitlintrc.json << 'EOF'
{
  "extends": ["@commitlint/config-conventional"],
  "rules": {
    "type-enum": [
      2,
      "always",
      ["feat", "fix", "chore", "docs", "refactor", "test", "ci"]
    ],
    "subject-case": [2, "never", ["start-case", "pascal-case", "upper-case"]],
    "header-max-length": [2, "always", 100]
  }
}
EOF
```

### Workflow commitlint (siempre)

```bash
mkdir -p /tmp/<repo>-setup-ci/.github/workflows
cat > /tmp/<repo>-setup-ci/.github/workflows/check-commits.yml << 'EOF'
name: Check commit messages

on:
  pull_request:

jobs:
  commitlint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Lint commit messages
        uses: wagoid/commitlint-github-action@v6
        with:
          configFile: .commitlintrc.json
EOF
```

### Workflow version bump (solo si tiene `plugin.json`)

```bash
cat > /tmp/<repo>-setup-ci/.github/workflows/check-version-bump.yml << 'EOF'
name: Check version bump

on:
  pull_request:
    paths:
      - '.claude-plugin/plugin.json'
      - 'skills/**'

jobs:
  version-bump:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Get version on base branch
        id: base
        run: |
          git fetch origin ${{ github.base_ref }}
          BASE_VERSION=$(git show origin/${{ github.base_ref }}:.claude-plugin/plugin.json | python3 -c "import sys,json; print(json.load(sys.stdin)['version'])")
          echo "version=$BASE_VERSION" >> $GITHUB_OUTPUT

      - name: Get version on PR branch
        id: pr
        run: |
          PR_VERSION=$(python3 -c "import json; print(json.load(open('.claude-plugin/plugin.json'))['version'])")
          echo "version=$PR_VERSION" >> $GITHUB_OUTPUT

      - name: Fail if version was not bumped
        run: |
          BASE="${{ steps.base.outputs.version }}"
          PR="${{ steps.pr.outputs.version }}"
          echo "Base version: $BASE"
          echo "PR version:   $PR"
          if [ "$BASE" = "$PR" ]; then
            echo "::error file=.claude-plugin/plugin.json::La version no fue actualizada (sigue en $PR). Bumpeala en .claude-plugin/plugin.json antes de mergear."
            exit 1
          fi
          echo "Version bumped: $BASE -> $PR OK"
EOF
```

---

## Paso 5 — Commit y push

```bash
cd /tmp/<repo>-setup-ci
git add .github/workflows/ .commitlintrc.json
git commit -m "ci: agregar conventional commits y check de version bump"
git push origin ci/setup-ci
```

---

## Paso 6 — Abrir PR

```bash
gh pr create \
  --repo <owner>/<repo> \
  --title "ci: setup conventional commits y branch protection" \
  --body "## Qué agrega este PR

- Workflow de conventional commits (commitlint) en todos los PRs
- Workflow de version bump en PRs que tocan \`skills/\` o \`plugin.json\`
- \`.commitlintrc.json\` con tipos: feat, fix, chore, docs, refactor, test, ci

## Branch protection

Después del merge, aplicar ruleset vía API:
\`\`\`bash
/ar-plugins:setup-ci <owner>/<repo> --solo-ruleset
\`\`\`
O manualmente en Settings → Branches → Add ruleset."
```

---

## Paso 7 — Aplicar branch protection ruleset

Después de que el PR esté mergeado (o si se corre con `--solo-ruleset`):

```bash
cat > /tmp/ruleset-<repo>.json << 'EOF'
{
  "name": "Protect master",
  "target": "branch",
  "enforcement": "active",
  "conditions": {
    "ref_name": {
      "include": ["refs/heads/master"],
      "exclude": []
    }
  },
  "rules": [
    {
      "type": "pull_request",
      "parameters": {
        "required_approving_review_count": 0,
        "dismiss_stale_reviews_on_push": false,
        "require_code_owner_review": false,
        "require_last_push_approval": false,
        "required_review_thread_resolution": false
      }
    },
    {
      "type": "required_status_checks",
      "parameters": {
        "required_status_checks": [
          { "context": "version-bump" },
          { "context": "commitlint" }
        ],
        "strict_required_status_checks_policy": false
      }
    },
    { "type": "non_fast_forward" }
  ]
}
EOF

gh api repos/<owner>/<repo>/rulesets --method POST --input /tmp/ruleset-<repo>.json
```

Para repos **sin** `plugin.json` (ej: `ar-plugins`), omitir `version-bump` de `required_status_checks`:

```json
"required_status_checks": [
  { "context": "commitlint" }
]
```

---

## Paso 8 — Confirmar

Reportar al usuario:

```
CI configurado en <owner>/<repo>:

  ✓ .commitlintrc.json
  ✓ .github/workflows/check-commits.yml
  ✓ .github/workflows/check-version-bump.yml  (si aplica)
  ✓ Branch protection ruleset activo en master

PR: <url>
```

Si algún paso falló, reportar el error exacto y qué hay que hacer manualmente.

---

## Tono

Directo. Si hay un blocker (scope faltante, repo no encontrado), reportarlo y detenerse — no intentar workarounds silenciosos.
