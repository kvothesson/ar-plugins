# Workflows de desarrollo

## Resolver un issue

```bash
/dev resolver #5
```

Ver `skills/dev/SKILL.md` para el detalle paso a paso.

## Crear un plugin nuevo

1. Leer `SPEC.md` para entender que hay que construir
2. Verificar que las URLs/APIs funcionen con WebFetch antes de escribir el SKILL.md
3. Crear directorio local con la estructura obligatoria (ver [plugins.md](plugins.md))
4. Escribir en orden: `plugin.json` → `SKILL.md` → `.gitignore` → `README.md`
5. Testear cada comando del SKILL.md (fetch real + fallback)
6. Validar: `claude plugin validate /ruta/al/plugin`
7. Crear repo y pushear
8. Agregar entrada a `marketplace.json`

```bash
# Paso 7 — crear repo
cd /tmp/<nombre>
git init && git add -A
git commit -m "feat: plugin <nombre> v1.0.0 — <descripcion corta>"
gh repo create kvothesson/<nombre> --public \
  --description "Plugin de Claude Code — <descripcion>" \
  --source . --remote origin --push

# Paso 8 — actualizar marketplace
gh repo clone kvothesson/ar-plugins /tmp/ar-plugins-mkt
# editar .claude-plugin/marketplace.json
git -C /tmp/ar-plugins-mkt add .claude-plugin/marketplace.json
git -C /tmp/ar-plugins-mkt commit -m "feat: agrega <nombre> al marketplace"
git -C /tmp/ar-plugins-mkt push && rm -rf /tmp/ar-plugins-mkt
```

## Actualizar un plugin existente

```bash
gh repo clone kvothesson/<nombre> /tmp/<nombre>
cd /tmp/<nombre>
git checkout -b fix/<descripcion>
# editar lo necesario
git add -A && git commit -m "fix: <descripcion>"
git push origin fix/<descripcion>
gh pr create --title "<descripcion>" --body "Describe el cambio y como se teseto"
rm -rf /tmp/<nombre>
```

## Cargar un issue proactivo

Si durante el trabajo se detecta un caso no cubierto, fuente caida o mejora obvia, registrarlo con `/reportar`. Detecta el repo destino por contexto, verifica duplicados y pide aprobacion antes de abrir.

Ver [kvothesson/reportar](https://github.com/kvothesson/reportar).

## Checklist antes de publicar

- [ ] `plugin.json` tiene name, version y description (sin array de skills)
- [ ] `SKILL.md` tiene frontmatter con `name` y `description` en tercera persona
- [ ] Cada URL de fetch verificada y funcional
- [ ] Cada skill tiene formato de respuesta en bloque de codigo
- [ ] Cada skill tiene fallback operativo
- [ ] `claude plugin validate` pasa sin errores
- [ ] README tiene ejemplos con datos reales (no placeholders)
- [ ] README tiene seccion "Fuentes" con URLs
- [ ] `.gitignore` existe
- [ ] Repo creado bajo `kvothesson/<nombre>` con `--public`
- [ ] Entrada en `marketplace.json` usa `"source": "github"` con `"repo": "kvothesson/<nombre>"`
- [ ] Entrada en `marketplace.json` tiene `"category"` correcta
