# OFFMENU · Kit para desarrollo web

Todo lo necesario para implementar la identidad de OFFMENU. Las reglas completas están en el
manual de marca (`manual/offmenu-manual.html`).

## Instalación rápida

1. Cargar las tipografías (Google Fonts, licencia SIL OFL):

   ```html
   <link rel="preconnect" href="https://fonts.googleapis.com">
   <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
   <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Schibsted+Grotesk:wght@400;500;700;800;900&family=IBM+Plex+Mono:wght@400;500&display=swap">
   ```

2. Importar `offmenu-tokens.css` antes que el resto de estilos. Incluye variables (`--om-*`),
   estilos base y componentes (`.om-boton`, `.om-campo`, `.om-tachado`, `.om-contenedor`).

3. Logotipo: pegar en línea `../logo/svg/offmenu-logotipo-plantilla.svg`. Las letras usan
   `currentColor` y la línea `var(--line)`:

   ```css
   .om-logo { color: var(--om-granate); --line: var(--om-rojo); line-height: 0; display: inline-block; }
   .om-logo svg { height: 22px; width: auto; }
   ```

   Nunca reconstruir el logotipo escribiendo el texto con la fuente.

4. Favicon e imagen para compartir: copiar `favicon/*` y `og-image.png` a la raíz pública.

   ```html
   <link rel="icon" href="/favicon.svg" type="image/svg+xml">
   <link rel="icon" href="/favicon-32.png" sizes="32x32" type="image/png">
   <link rel="apple-touch-icon" href="/apple-touch-icon.png">
   <meta name="theme-color" content="#42000E">
   <meta property="og:image" content="https://offmenu.es/og-image.png">
   ```

## Reglas que no se pueden saltar

- La línea del logotipo siempre es roja (#F5302A); las letras nunca son rojas.
- Fondo blanco por defecto, una sola banda granate por página, pie negro.
- Una sola tachadura (`.om-tachado`) por página.
- Esquinas rectas, filetes de 1 px, sin sombras ni degradados.
- El rojo #F5302A no se usa en texto de menos de 24 px; para eso existe `--om-rojo-texto`.
- WCAG 2.2 AA.

## Contenido

| Archivo | Uso |
|---|---|
| `offmenu-tokens.css` | Variables, base y componentes |
| `offmenu-tokens.json` | Los mismos valores para Figma u otras herramientas |
| `favicon/` | SVG y PNG (16, 32, 48, 192, 512) y apple-touch-icon (180) |
| `og-image.png` | Imagen para redes al compartir enlaces (1200 × 630) |
| `../logo/svg/` | Todas las versiones del logotipo |
