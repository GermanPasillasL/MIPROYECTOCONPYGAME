# Flujo de trabajo del repositorio

Este documento explica cómo voy a organizar el trabajo en ramas durante el curso.

## Ramas

- **`main`** — versión estable. Siempre debe funcionar. Nunca trabajo directo aquí (salvo el README inicial); solo recibe merges de `v01`.
- **`v01`** — rama de integración de la versión 1 del proyecto. Aquí hago merge de las ramas de actividades y pruebo que el juego corra antes de pasarlo a `main`.
- **`actividad1`**, **`actividad2`** — una rama por sesión/actividad. Ahí vive el avance de cada una (`actividad1`: escena base; `actividad2`: tienda y compañero, creada a partir de `actividad1`).

## Pasos de cada actividad

1. Crear la rama de la actividad (`git checkout -b actividadN`).
2. Programar y hacer commits frecuentes con mensajes descriptivos (ej.: `Agrega tienda con mejoras en actividad2`).
3. Subir la rama (`git push -u origin actividadN`).
4. Cambiarme a `v01` y hacer `git merge --no-ff actividadN`.
5. Ejecutar el juego en `v01` y comprobar que funciona.
6. Solo si todo funciona: `git checkout main` y `git merge --no-ff v01`, luego `git push`.

## Reglas que me puse

- No borrar ramas hasta resolver sus conflictos de merge; si hay conflicto, lo documento y lo consulto en clase.
- Mensajes de commit en español, en presente, diciendo qué cambió y dónde.
- Probar siempre en `v01` antes de tocar `main`.
- Para las siguientes actividades se crearán nuevas ramas (`actividad3`, ...) con el mismo ciclo, y las versiones grandes del juego se integrarán en ramas `v02`, `v03`, etc.

## Comandos que uso

```bash
git checkout -b actividad2        # crear rama de trabajo
git add . && git commit -m "..."  # guardar cambios
git checkout v01                  # ir a la rama de integración
git merge --no-ff actividad2      # integrar la actividad
git checkout main && git merge --no-ff v01
git log --oneline --graph --all   # ver el grafo de ramas
```
