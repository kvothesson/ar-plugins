# AR Plugins — Spec de desarrollo

Guía para construir y publicar plugins en el ecosistema AR.

---

## Qué es un plugin

Un plugin es un directorio que extiende Claude Code con uno o más **skills** (slash commands).
La unidad mínima es: `plugin.json` + al menos un `SKILL.md`.

---

## Estructura de un plugin

```
mi-plugin/
  .claude-plugin/
    plugin.json           # manifiesto del plugin
  skills/
    mi-skill/
      SKILL.md            # definición del skill (prompt + lógica)
  memory/
    *.example.md          # plantillas públicas (gitignored los reales)
  README.md
  .gitignore
```

### `.claude-plugin/plugin.json`

```json
{
  "name": "nombre-del-plugin",
  "version": "1.0.0",
  "description": "Una línea que explique para qué sirve.",
  "skills": [
    {
      "name": "mi-skill",
      "path": "skills/mi-skill/SKILL.md"
    }
  ]
}
```

### `skills/<nombre>/SKILL.md`

```markdown
---
description: Texto que ve Claude Code al listar skills. Incluye cuándo usar este skill.
---

# Skill: /mi-skill

[Instrucciones para Claude. Qué leer, qué hacer, cómo presentar el resultado.]
```

El frontmatter `description` es clave: Claude lo usa para decidir si activar el skill.

---

## Ciclo de desarrollo

```
1. Creás el repo  →  github.com/usuario/nombre-plugin
2. Desarrollás localmente con:  claude --plugin-dir .
3. Testeás con /mi-skill en una sesión real
4. Subís el repo
5. Registrás en ar-plugins/marketplace.json
```

### Testear localmente

```bash
cd mi-plugin
claude --plugin-dir .
```

---

## Convenciones

| Ítem | Convención |
|---|---|
| Nombre del plugin | kebab-case, en español o inglés |
| Nombre del skill | kebab-case, directo y descriptivo |
| Idioma del SKILL.md | Español (el ecosistema es hispanohablante) |
| Versión | semver: `MAJOR.MINOR.PATCH` |
| Datos personales | Siempre gitignored, plantillas `.example.md` públicas |
| README | Genérico — sirve para cualquier usuario, sin pistas del autor |

---

## Publicar en el marketplace

Abrí un PR a [kvothesson/ar-plugins](https://github.com/kvothesson/ar-plugins) agregando tu plugin al array `plugins` en `marketplace.json`:

```json
{
  "name": "mi-plugin",
  "description": "Una línea que explique para qué sirve.",
  "repository": "https://github.com/usuario/mi-plugin",
  "version": "1.0.0"
}
```

### Criterios para ser aceptado

- [ ] Tiene `plugin.json` válido
- [ ] Tiene al menos un `SKILL.md` con frontmatter `description`
- [ ] No contiene datos personales ni credenciales
- [ ] README genérico (usable por cualquiera)
- [ ] `.gitignore` protege cualquier archivo de contexto personal

---

## Plugins del ecosistema

| Plugin | Descripción | Estado |
|---|---|---|
| [nodo](https://github.com/kvothesson/nodo) | Contexto personal persistente entre sesiones | ✅ v1.0.0 |

---

## Roadmap de plugins

Ideas para desarrollar:

- **inbox** — gestión de inbox diario con prioridades
- **standup** — genera el standup del día desde los commits/tareas
- **review** — code review con criterios configurables
- **deploy** — checklist de deploy personalizable
- **aprender** — registra y repasa conceptos (spaced repetition ligero)
