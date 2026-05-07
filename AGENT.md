# AGENT.md — AR Plugins

Marketplace de plugins de Claude Code para el ecosistema argentino. Cada plugin conecta a Claude con datos reales de Argentina — organismos oficiales, APIs publicas, fuentes primarias.

**Objetivo:** datos reales, fuentes primarias, lenguaje llano. Sin intermediarios, sin hardcodear valores que cambian.

---

## Arquitectura

```
kvothesson/ar-plugins          <- este repo (indice + tooling de dev)
  .claude-plugin/
    marketplace.json           <- lista todos los plugins publicados
    plugin.json                <- ar-plugins como plugin instalable
  .agents/                     <- documentacion detallada por tema
  skills/dev/SKILL.md          <- /dev resolver #N
  SPEC.md                      <- spec de plugins planificados

kvothesson/<nombre>            <- cada plugin en su propio repo
  .claude-plugin/plugin.json
  skills/<nombre>/SKILL.md
  README.md
```

---

## Indice — leer segun tarea

| Tarea | Archivo |
|-------|---------|
| Editar o entender `marketplace.json` | [.agents/marketplace.md](.agents/marketplace.md) |
| Crear o modificar un plugin (`plugin.json`, estructura) | [.agents/plugins.md](.agents/plugins.md) |
| Escribir o corregir un `SKILL.md` | [.agents/skills.md](.agents/skills.md) |
| Crear plugin nuevo, actualizar existente, checklist | [.agents/workflows.md](.agents/workflows.md) |
| Principios del ecosistema y referencias | [.agents/principios.md](.agents/principios.md) |

Ver plugins planificados: `gh api repos/kvothesson/ar-plugins/contents/SPEC.md --jq '.content' | base64 -d`
