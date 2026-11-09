# OFFMENU · Redes sociales

- `estrategia.html` · estrategia completa (se genera desde `estrategia-src.html`).
- `posts/` · publicaciones 1080 × 1350 en PNG (originales) y JPG (para la web).
- `reels/` · reels 1080 × 1920 en MP4 y sus portadas.

## Regenerar

```bash
python3 rrss/build.py          # inserta los logotipos en las plantillas
node rrss/render_posts.js      # exporta las publicaciones
node rrss/render_reels.js      # renderiza los reels (fotograma a fotograma + ffmpeg)
```

Para crear piezas nuevas: añadir una `<section class="post">` en `posts-src.html` o un reel en el objeto `REELS` de `reels-src.html`.
