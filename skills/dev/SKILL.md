---
description: Skill de desarrollo para ar-plugins. Dado un número de issue, lo implementa, verifica las fuentes y abre un PR. Usalo con /dev resolver #N.
---

# Skill: /dev

## Comandos

### `/dev resolver #<número>`

Resolvé el issue indicado de `kvothesson/ar-plugins`, implementá el cambio, verificá que funcione y abrí un PR.

---

#### Paso 1 — Leer el issue

```bash
gh issue view <número> --repo kvothesson/ar-plugins
```

Determiná el tipo de cambio:
- **Plugin nuevo** → seguir flujo completo
- **Fix o actualización de plugin existente** → clonar ese repo y modificar
- **Cambio en marketplace o docs** → modificar directamente en ar-plugins

---

#### Paso 2 — Leer el contexto

Siempre leer AGENT.md antes de tocar archivos — es el contrato de calidad del ecosistema:

```bash
gh api repos/kvothesson/ar-plugins/contents/AGENT.md --jq '.content' | base64 -d
```

Si es plugin nuevo, leer también SPEC.md para la descripción completa del plugin:

```bash
gh api repos/kvothesson/ar-plugins/contents/SPEC.md --jq '.content' | base64 -d
```

Para ver un plugin de referencia:

```bash
gh api repos/kvothesson/arca/contents/skills/arca/SKILL.md --jq '.content' | base64 -d
```

---

#### Paso 3 — Verificar fuentes

Para cada skill del plugin, verificá que las URLs funcionen **antes de escribir el SKILL.md**:

- WebFetch a cada URL → ¿responde? ¿datos legibles y útiles?
- Si falla → buscar alternativa con WebSearch `site:<organismo>.gob.ar [tema]`
- Guardar qué URLs funcionaron — son las que van en el SKILL.md y en los ejemplos del README

Sin URLs verificadas no se escribe el SKILL.md.

---

#### Paso 4 — Crear branch y clonar

**Para cambios en ar-plugins directamente:**

```bash
gh repo clone kvothesson/ar-plugins /tmp/ar-plugins-fix-<N>
cd /tmp/ar-plugins-fix-<N>
git checkout -b feat/issue-<N>-<descripción-corta>
```

**Para cambios en el repo de un plugin:**

```bash
gh repo clone kvothesson/<nombre> /tmp/<nombre>-fix-<N>
cd /tmp/<nombre>-fix-<N>
git checkout -b fix/issue-<N>-<descripción-corta>
```

**Para plugin nuevo (repo propio):**

```bash
mkdir -p /tmp/<nombre>/.claude-plugin
mkdir -p /tmp/<nombre>/skills/<nombre>
cd /tmp/<nombre>
git init
```

---

#### Paso 5 — Implementar

**Estructura obligatoria de todo plugin:**

```
<nombre>/
  .claude-plugin/
    plugin.json
  skills/
    <nombre>/
      SKILL.md
  README.md
  .gitignore
```

**plugin.json:**

```json
{
  "name": "<nombre>",
  "version": "1.0.0",
  "description": "<descripcion corta sin emojis>",
  "skills": [
    {
      "name": "<nombre>",
      "path": "skills/<nombre>/SKILL.md"
    }
  ]
}
```

**Reglas del SKILL.md (nunca violarlas):**
- Frontmatter con `description` obligatorio
- Nunca hardcodear montos, fechas ni requisitos — siempre WebFetch/WebSearch a fuente primaria
- URL exacta a fetchear para cada comando
- Formato de respuesta con bloque de código de ejemplo
- Fallback si la URL principal falla
- Sección de tono al final
- Siempre mostrar fuente y fecha del dato en la respuesta

**Para fix/actualización:** solo modificar lo pedido. Sin refactors no solicitados.

---

#### Paso 6 — Testear

Para cada comando del SKILL.md, ejecutá las búsquedas/fetches que el skill haría en producción y verificá resultados. Usá esos datos reales para escribir los ejemplos del README — sin placeholders.

Checklist antes de continuar:

- [ ] `plugin.json` tiene name, version, description y skills correctos
- [ ] `SKILL.md` tiene frontmatter con `description`
- [ ] Cada URL de fetch verificada y funcional
- [ ] Cada skill tiene formato de respuesta definido en bloque de código
- [ ] Cada skill tiene fallback
- [ ] README tiene ejemplos con datos reales (no `$XX.XX` ni `[monto]`)
- [ ] README tiene sección "Fuentes" con URLs
- [ ] `.gitignore` existe

---

#### Paso 7 — Commit y push

**Para plugin existente (fix):**

```bash
git add -A
git commit -m "fix: <descripción corta> (closes #<N>)"
git push origin <branch>
```

**Para plugin nuevo:**

```bash
git add -A
git commit -m "feat: plugin <nombre> v1.0.0"
gh repo create kvothesson/<nombre> --public \
  --description "Plugin de Claude Code — <descripción>" \
  --source . --remote origin --push
```

---

#### Paso 8 — Actualizar marketplace.json (si aplica)

Si el cambio agrega un plugin nuevo o modifica su versión, actualizar `.claude-plugin/marketplace.json` en ar-plugins:

```bash
# Editar .claude-plugin/marketplace.json en el branch actual:
# - Plugin nuevo: agregar entrada al array "plugins"
# - Versión actualizada: cambiar "version" en la entrada existente
git add .claude-plugin/marketplace.json
git commit -m "feat: agrega <nombre> al marketplace"
```

---

#### Paso 9 — Abrir el PR

```bash
gh pr create \
  --repo kvothesson/ar-plugins \
  --title "<descripción corta>" \
  --body "Closes #<N>

## Qué hace
<descripción del cambio>

## Cómo se testeó
<URLs verificadas, datos obtenidos, fallbacks probados>"
```

---

## Tono del proceso

- Seguir AGENT.md al pie de la letra — es el contrato de calidad del ecosistema
- Resolver con sentido común ante ambigüedad, sin preguntar lo obvio
- Si algo está bloqueado (URL caída, permisos), informar el blocker concretamente antes de seguir

---

## Referencias

Recursos a consultar según lo que pida el issue — no son siempre necesarios, usarlos cuando aplique:

| Cuándo | Recurso |
|---|---|
| El issue involucra crear o modificar una skill | [Documentación de skills](https://code.claude.com/docs/en/skills) |
| Necesitás descubrir otras páginas de docs | [Índice completo de docs](https://code.claude.com/docs/llms.txt) |
| El issue involucra la estructura de un plugin | AGENT.md del repo (Paso 2) |
| El issue involucra un plugin específico | SPEC.md del repo (Paso 2) |
