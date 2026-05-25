---
name: Obsidian & Gold
colors:
  surface: '#131313'
  surface-dim: '#131313'
  surface-bright: '#393939'
  surface-container-lowest: '#0e0e0e'
  surface-container-low: '#1c1b1b'
  surface-container: '#20201f'
  surface-container-high: '#2a2a2a'
  surface-container-highest: '#353535'
  on-surface: '#e5e2e1'
  on-surface-variant: '#c4c7c7'
  inverse-surface: '#e5e2e1'
  inverse-on-surface: '#313030'
  outline: '#8e9192'
  outline-variant: '#444748'
  surface-tint: '#c9c6c5'
  primary: '#c9c6c5'
  on-primary: '#313030'
  primary-container: '#0d0d0d'
  on-primary-container: '#7c7a7a'
  inverse-primary: '#5f5e5e'
  secondary: '#e9c349'
  on-secondary: '#3c2f00'
  secondary-container: '#af8d11'
  on-secondary-container: '#342800'
  tertiary: '#ffb4a8'
  on-tertiary: '#690000'
  tertiary-container: '#250000'
  on-tertiary-container: '#dd4332'
  error: '#ffb4ab'
  on-error: '#690005'
  error-container: '#93000a'
  on-error-container: '#ffdad6'
  primary-fixed: '#e5e2e1'
  primary-fixed-dim: '#c9c6c5'
  on-primary-fixed: '#1c1b1b'
  on-primary-fixed-variant: '#474646'
  secondary-fixed: '#ffe088'
  secondary-fixed-dim: '#e9c349'
  on-secondary-fixed: '#241a00'
  on-secondary-fixed-variant: '#574500'
  tertiary-fixed: '#ffdad4'
  tertiary-fixed-dim: '#ffb4a8'
  on-tertiary-fixed: '#410000'
  on-tertiary-fixed-variant: '#920703'
  background: '#131313'
  on-background: '#e5e2e1'
  surface-variant: '#353535'
typography:
  headline-xl:
    fontFamily: Playfair Display
    fontSize: 72px
    fontWeight: '700'
    lineHeight: 80px
    letterSpacing: -0.02em
  headline-lg:
    fontFamily: Playfair Display
    fontSize: 48px
    fontWeight: '700'
    lineHeight: 56px
  headline-lg-mobile:
    fontFamily: Playfair Display
    fontSize: 32px
    fontWeight: '700'
    lineHeight: 40px
  headline-md:
    fontFamily: Playfair Display
    fontSize: 32px
    fontWeight: '600'
    lineHeight: 40px
  body-lg:
    fontFamily: Hanken Grotesk
    fontSize: 18px
    fontWeight: '400'
    lineHeight: 28px
  body-md:
    fontFamily: Hanken Grotesk
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 24px
  label-caps:
    fontFamily: Geist
    fontSize: 12px
    fontWeight: '600'
    lineHeight: 16px
    letterSpacing: 0.1em
  nav-link:
    fontFamily: Hanken Grotesk
    fontSize: 14px
    fontWeight: '500'
    lineHeight: 20px
    letterSpacing: 0.05em
spacing:
  margin-mobile: 1.5rem
  margin-desktop: 5rem
  gutter: 1.5rem
  stack-unit: 0.5rem
  section-gap: 8rem
---

## Brand & Style

The design system is engineered to reflect the precision and prestige of a premier Las Vegas tattoo studio. The brand personality is **Expert, Edgy, and Artistic**, demanding a UI that feels like a curated gallery rather than a service directory. 

The visual style is **High-Contrast / Bold** mixed with **Minimalism**. It utilizes deep, ink-inspired blacks and charcoal grays to create a canvas where the artistry is the focal point. The interface avoids unnecessary decoration, instead opting for a "Gallery-Grade" aesthetic: heavy whitespace (even in dark mode), precise alignment, and a sophisticated balance of raw energy and professional polish. The emotional response should be one of immediate trust in the artist’s technical skill and the studio's elite status.

## Colors

This design system uses a high-luxury dark palette. The primary background is a rich, near-black (`#0D0D0D`), creating maximum contrast for photography and the "Vegas Gold" accent.

- **Primary (Ink):** `#0D0D0D` — Used for backgrounds and primary containers.
- **Secondary (Vegas Gold):** `#D4AF37` — Used for premium accents, icons, and primary CTAs to signify elite status.
- **Tertiary (Blood Red):** `#8B0000` — Used sparingly for secondary CTAs or "Book Now" highlights to evoke passion and intensity.
- **Neutral (Charcoal):** `#1A1A1A` — Used for secondary sections, cards, and input fields to provide subtle depth against the primary black.
- **Text:** White (`#FFFFFF`) for high-level headlines and a slightly muted Gray (`#E0E0E0`) for body text to maintain readability without harshness.

## Typography

The typography system pairs the high-character, editorial feel of **Playfair Display** with the technical precision of **Hanken Grotesk**.

- **Headlines:** Playfair Display is used to provide a "Fine Art" tattoo feel. Large headlines should use negative letter-spacing for a tighter, more dramatic look.
- **Body:** Hanken Grotesk provides ultra-clean, modern legibility that balances the traditional feel of the serif headings.
- **Labels & Utility:** **Geist** is used for technical labels, metadata, and monospaced accents to emphasize the professional/surgical precision of the studio. All utility text should be in uppercase with generous letter spacing to maintain an "expensive" feel.

## Layout & Spacing

The layout follows a **Fixed Grid** model for desktop to maintain a high-end, editorial feel, transitioning to a fluid model for mobile.

- **Desktop:** 12-column grid with a max-width of 1440px. Side margins are generous (80px) to allow the content to breathe.
- **Mobile:** 4-column grid with 24px margins.
- **Rhythm:** A vertical rhythm based on an 8px (0.5rem) increment. Section gaps are intentionally large (128px) to separate different artist portfolios and studio services, preventing visual clutter.
- **Photography:** Images should frequently break the grid or utilize "full-bleed" widths to highlight the artistic detail of the tattoos.

## Elevation & Depth

This design system eschews standard shadows in favor of **Tonal Layers** and **Subtle Textures**.

- **Layering:** Backgrounds use `#0D0D0D`. Elements meant to sit above the background (cards, modals) use `#1A1A1A` with a very thin, 1px border in `#333333` (Charcoal).
- **Glassmorphism:** Navigation bars and sticky booking bars use a deep, semi-transparent black blur (80% opacity, 20px blur) to maintain visibility over high-detail photography.
- **Textures:** Large background sections should occasionally feature a very low-opacity "Ink Wash" or "Clean Concrete" texture overlay (2-4% opacity) to add tactile depth without distracting from the portfolio pieces.
- **Interaction:** Hover states on interactive elements should use a "Glow" effect—a soft, low-spread outer glow using the Secondary Gold color.

## Shapes

The shape language is **Sharp (0)**. 

To reflect the precision of a tattoo needle and the "edgy" brand persona, all UI elements—including buttons, input fields, and portfolio cards—feature 0px corner radii. This creates a rigorous, architectural feel. The only exception is the use of circular "Artist Avatars" or specific badge shapes (Google/Yelp) to provide a necessary visual break from the sharp-edged grid.

## Components

- **Buttons:** Sharp-edged, no radius. Primary buttons are solid `#D4AF37` (Vegas Gold) with black text. On hover, they transition to an "Inverted" style or add a subtle gold outer glow.
- **Interactive Portfolio Grids:** Use a Masonry layout. On hover, images should slightly scale up, with a dark overlay revealing the artist's name and "Book Artist" label in Geist Mono.
- **Sticky Booking Bar:** A persistent bar at the bottom of the screen on mobile (top on desktop). It utilizes a glassmorphic background with a centered "Book Appointment" CTA in Blood Red (`#8B0000`).
- **Input Fields:** Bottom-border only (0px border on top/sides). Labels sit above the field in Geist Mono, 10px, uppercase.
- **Review Badges:** High-contrast, monochromatic versions of Google/Yelp logos to prevent brand-color clashing, appearing only in the footer or dedicated testimonial sections.
- **Sliders:** Minimalist progress indicators (lines, not dots) in Gold.