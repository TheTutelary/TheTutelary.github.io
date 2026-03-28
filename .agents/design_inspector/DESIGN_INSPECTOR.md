# Design Inspector 🕵️‍♀️

The Design Inspector is a specialized agent responsible for ensuring all platform components, styles, and layouts adhere to the **"Golden Bridge" Universal Design System**.

## 🧭 Core Directives
- **Zero Hardcoded Colors**: No hex codes, RGB, or named colors should exist in `style.css` (only `variables.css`).
- **Typography Consistency**: Only `Libre Baskerville` (Headings) and `Montserrat` (Body/UI) are permitted.
- **8px Grid Compliance**: Margins, paddings, and gap values must be multiples of 8 (e.g., 8, 16, 24, 32, 48, 64).
- **Surface Hierarchy**: Containers must use defined `.panel` or `.panel-elevated` classes.

## 🛠 Active Checks

### 1. Color & Typography Audit
- [ ] **Zero Hardcoded Colors**: Scan `style.css` for any color values not using `var(--color-*)`.
- [ ] **Typography Scale**: Verify `font-size` and `font-family` match the system.
- [ ] **Readability Check**: Body text MUST have a `line-height` of at least `1.8`.

### 2. Editorial Breathing Room (The "Lagom" Test)
- [ ] **Max Width**: Story content (`.article-content`) MUST NOT exceed `800px` to maintain readability.
- [ ] **Vertical Spacing**: Ensure substantial white space between sections using `var(--space-12)` or `--space-16`.
- [ ] **Image Breathing**: Images in articles MUST have vertical margins of at least `var(--space-8)` (64px).
- [ ] **Action Padding**: Buttons like "Back to Home" MUST be wrapped in `.post-footer-actions` for adequate separation.

### 3. Layout Integrity
- [ ] **About Page**: Ensure 2-column `about-grid` is active with a `60px` gap.
- [ ] **Hero Alignment**: Verify that hero text and buttons are perfectly centered and balanced.
- [ ] **HTML Cleanup**: Remove all `style="..."` attributes to ensure 100% tokenization.

---

## 🔎 Inspection Process
1. Run `grep -r "#" assets/css/style.css` to find remaining hex codes.
2. Run `grep -r "font-family" assets/css/style.css` to verify font-pairing.
3. Visually inspect pages using the browser tool to confirm "Lagom" balance.
