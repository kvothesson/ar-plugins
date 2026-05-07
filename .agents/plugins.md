# Plugins

## Estructura obligatoria

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

## plugin.json

Las skills **no se declaran** aqui — Claude Code las descubre automaticamente desde `skills/`. Solo metadata.

```json
{
  "name": "<nombre>",
  "version": "1.0.0",
  "description": "<descripcion corta sin emojis>",
  "author": { "name": "kvothesson" }
}
```

Campos opcionales: `homepage` (URL del repo), `repository` (objeto con `url`), `license`.

## Namespacing de skills

Se invocan como `/nombre-plugin:nombre-skill [argumentos]`. Si plugin y skill tienen el mismo nombre, el usuario puede usar `/nombre` directamente si no hay conflicto.

## Probar y validar

```bash
# Probar localmente
claude --plugin-dir /ruta/al/plugin

# Validar estructura antes de publicar
claude plugin validate /ruta/al/plugin

# Recargar sin reiniciar (desde Claude Code)
/reload-plugins
```

## README.md

1. Que hace el plugin (2-3 lineas)
2. Instalacion: `claude --plugin-dir /ruta/al/plugin`
3. Ejemplo real de output por cada comando — datos reales, no placeholders
4. Seccion "Fuentes" con URLs

**Los ejemplos deben ser reales.** Fetchear los datos antes de escribirlos. Nunca `$XX.XX` ni `[monto]`.

## .gitignore

```
.DS_Store
*.log
```

## Convencion de versiones

- `1.0.x` — fixes, actualizaciones de URLs
- `1.x.0` — skills nuevas o cambios de comportamiento
- `x.0.0` — refactor estructural o cambio de fuentes
