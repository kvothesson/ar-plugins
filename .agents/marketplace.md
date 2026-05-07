# Marketplace

`marketplace.json` es el indice central del ecosistema. Usa el schema oficial de Claude Code.

## Estructura del archivo

```json
{
  "$schema": "https://json.schemastore.org/claude-code-marketplace.json",
  "name": "ar-plugins",
  "description": "...",
  "owner": { "name": "kvothesson" },
  "plugins": [ ... ]
}
```

## Formato de cada entrada

```json
{
  "name": "<nombre>",
  "description": "<descripcion corta>",
  "author": { "name": "kvothesson" },
  "source": {
    "source": "github",
    "repo": "kvothesson/<nombre>"
  },
  "homepage": "https://github.com/kvothesson/<nombre>",
  "category": "<categoria>"
}
```

## Tipos de source validos

| Tipo | Cuando usarlo | Forma |
|------|---------------|-------|
| `"github"` | Repo publico en GitHub — caso estandar | `{ "source": "github", "repo": "owner/repo" }` |
| `"url"` | Zip o tarball descargable | `{ "source": "url", "url": "https://..." }` |
| `"git-subdir"` | Subdirectorio dentro de un repo | `{ "source": "git-subdir", "url": "...", "subdir": "ruta" }` |
| `"npm"` | Paquete en npm | `{ "source": "npm", "package": "nombre" }` |
| ruta relativa | Plugin local en el mismo repo | `"source": "./plugins/nombre"` |

**Nunca usar** `"source": "git"` — no existe en el schema oficial.

## Category

Valores validos: `"development"`, `"productivity"`, `"data"`, `"communication"`.

Convencion de este ecosistema:
- `"development"` — tooling de dev (ej: `reportar`)
- `"productivity"` — plugins de datos para usuarios argentinos (todo lo demas)

## Version pinning

Si una entrada tiene campo `"version"`, Claude Code no actualiza el plugin automaticamente hasta que ese string cambie. **Omitir `version`** para que los usuarios siempre reciban la ultima version del repo.

## Ver estado actual

```bash
gh api repos/kvothesson/ar-plugins/contents/.claude-plugin/marketplace.json --jq '.content' | base64 -d
```
