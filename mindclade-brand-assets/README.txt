MINDCLADE — BRAND ASSETS
Frontier models for programmable biology

TWO FAMILIES

  CAPS      the MC tile — Instrument Sans 700, clay C.
            The company mark. Decks, site, signage, avatars,
            anything an investor or a journalist sees.
            Files: mc-*

  MONO      mc. and mindclade. — JetBrains Mono 500, clay
            period. The engineering mark. CLI, packages,
            docs, README badges, dev-facing pages.
            Files: mono-*

They are not interchangeable and they never appear together
in the same lockup. One page, one family.

============================================================
CONTENTS
============================================================

/svg — vector, live text (see the note at the bottom)
  mc-tile-ink.svg               primary monogram, ink field
  mc-tile-bone.svg              for dark backgrounds
  mc-tile-onecolor.svg          print, etch, embroidery
  mc-lockup-horizontal.svg      monogram + name + descriptor
  mc-lockup-horizontal-dark.svg
  mc-wordmark.svg               name only
  mc-submark.svg                mc.
  favicon.svg

/png — flat pixels, safe everywhere
  mc-tile-ink-1024.png          master
  mc-tile-bone-1024/512/256/128/64/32.png
  mc-tile-onecolor-1024/512/256/128/64/32.png

  mc-lockup-horizontal.png            2160 wide, transparent
  mc-lockup-horizontal-1080w.png
  mc-lockup-horizontal-540w.png
  mc-lockup-horizontal-dark.png       2160 wide
  mc-lockup-horizontal-dark-1080w.png
  mc-lockup-horizontal-dark-540w.png

  mc-wordmark.png               transparent
  mc-submark.png                transparent

  favicon-512/256/128.png       halved in steps from the master
  favicon-64/48/32/16.png       rendered natively at 1:1
  favicon-16-M.png              16 px reduction: M only
  apple-touch-icon-180.png
  mc-avatar-460.png             GitHub / LinkedIn / Slack
  mc-og-1200x630.png            social share card

  MONO FAMILY
  mono-tile-ink-1024/512/256/128.png     primary mono tile
  mono-tile-bone-1024/512/256/128.png    for dark backgrounds
  mono-tile-clay-1024/512/256/128.png    accent field
  mono-wordmark.png / -1080w / -540w     mindclade. transparent
  mono-wordmark-dark.png / -1080w / -540w
  mono-icon-180/64/48/32/16.png          native 1:1, dot dropped at 16

/svg — mono family
  mono-tile-ink.svg
  mono-tile-bone.svg
  mono-tile-clay.svg
  mono-wordmark.svg              ink text, clay period
  mono-wordmark-light.svg        for dark backgrounds

/fonts
  GET-THE-FONTS.txt             where to get them, how to install

/web
  head-snippet.html             fonts + favicons + OG tags
  tokens.css                    colour and type variables

============================================================
COLOUR
============================================================

  ink         #201C24    everything structural
  clay        #B5673F    the C, on light surfaces
  clay light  #D68A61    the C, on ink surfaces
  bone        #FBFAF7    paper
  bone warm   #F2EFE8    reversed type and tiles
  ink deep    #0F0D12    terminals, code blocks

The C is always clay. The M is never clay. Clay is never
body text.

============================================================
TYPE
============================================================

  Instrument Sans 700, -7.5% tracking   monogram
  Instrument Sans 600, -5% tracking     wordmark
  Instrument Sans 400/500               body
  JetBrains Mono 500                    code, labels, sub-mark

Both free under the SIL Open Font License. See /fonts.

============================================================
GEOMETRY
============================================================

  tile corner radius   23% of tile width
  cap height           30% of tile width
  clear space          25% of tile width, all sides
  wordmark gap         25% of tile width
  minimum tile         16 px / 5 mm

Below 24 px, use the tile alone — drop the wordmark.
At 16 px, two letters have about 10 pixels of cap height and
go soft no matter how the file is made. Use favicon-16-M.png
there — the tile with a clay M only.

GitHub crops avatars to a circle: upload mc-avatar-460.png
square and let the crop happen. Don't pre-round it.

============================================================
THE SUB-MARK
============================================================

mc. belongs where code already is: CLI, package name, docs
favicon, README badges. It replaces the caps tile, it never
sits next to the caps wordmark. Drop the period below 32 px —
mono-icon-16.png already has it removed.

mindclade. (mono-wordmark) is the long form of the same idea:
the period closes the name, so it needs no tile and no
descriptor. Use it as a header lockup on developer pages.

============================================================
NEVER
============================================================

  no gradients            no outlined version
  no rotation             no colours outside the palette
  no stretching           no drop shadows
  no reordered letters    no extra elements inside the tile

============================================================
A NOTE ON THE SVGs — READ THIS
============================================================

The monogram and wordmark are type, so the SVG files contain
live text rather than outlines. Two consequences:

1. Install Instrument Sans and JetBrains Mono first (both
   free — see /fonts). Without them the SVGs silently fall
   back to Helvetica and the logo is wrong.

2. Before sending an SVG to a printer, fabricator, agency or
   anyone outside the company, open it in Figma or
   Illustrator and convert the text to outlines
   (Type > Create Outlines). Then it is safe anywhere.

The PNGs are already flat and correct as-is. Treat
mc-tile-ink-1024.png and mc-lockup-horizontal.png as the
authoritative masters until you have an outlined vector.
