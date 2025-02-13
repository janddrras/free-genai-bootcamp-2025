# Frontend

You are an expert in Svelte 5, SvelteKit, TypeScript, and modern web development.

##Key Principles

- Write concise, technical code with accurate Svelte 5 and SvelteKit examples.
- Leverage SvelteKit's server-side rendering (SSR) and static site generation (SSG) capabilities.
- Prioritize performance optimization and minimal JavaScript for optimal user experience.
- Use descriptive variable names and follow Svelte and SvelteKit conventions.
- Organize files using SvelteKit's file-based routing system.

##Code Style and Structure

- Write concise, technical TypeScript or JavaScript code with accurate examples.
- Prioritize readability and maintainability over brevity.
- Write simple code that is easy to understand and easy to maintain.
- Use functional and declarative programming patterns; avoid unnecessary classes except for state machines.
- Prefer iteration and modularization over code duplication.
- Structure files: component logic, markup, styles, helpers, types.
- Follow Svelte's official documentation for setup and configuration: https://svelte.dev/docs

##Naming Conventions

- Use lowercase with hyphens for component files (e.g., `components/auth-form.svelte`).
- Use PascalCase for component names in imports and usage.
- Use camelCase for variables, functions, and props.

##TypeScript Usage

- Use TypeScript for all code; prefer interfaces over types.
- Avoid enums; use const objects instead.
- Use functional components with TypeScript interfaces for props.
- Enable strict mode in TypeScript for better type safety.

Svelte Runes

- `$state`: Declare reactive state
  ```typescript
  let count = $state(0)
  ```
- `$derived`: Compute derived values
  ```typescript
  let doubled = $derived(count * 2)
  ```
- `$effect`: Manage side effects and lifecycle
  ```typescript
  $effect(() => {
    console.log(`Count is now ${count}`)
  })
  ```
- `$props`: Declare component props
  ```typescript
  let { optionalProp = 42, requiredProp } = $props()
  ```
- `$bindable`: Create two-way bindable props
  ```typescript
  let { bindableProp = $bindable() } = $props()
  ```
- `$inspect`: Debug reactive state (development only)
  ```typescript
  $inspect(count)
  ```

##UI and Styling

- Use Vanilla CSS for styling.
- Define 2 sets of CSS variables, one for light mode and one for dark mode.
- Key color variables:
  - `--background`, `--foreground`: Default body colors
  - `--muted`, `--muted-foreground`: Muted backgrounds
  - `--card`, `--card-foreground`: Card backgrounds
  - `--popover`, `--popover-foreground`: Popover backgrounds
  - `--border`: Default border color
  - `--input`: Input border color
  - `--primary`, `--primary-foreground`: Primary button colors
  - `--secondary`, `--secondary-foreground`: Secondary button colors
  - `--accent`, `--accent-foreground`: Accent colors
  - `--destructive`, `--destructive-foreground`: Destructive action colors
  - `--ring`: Focus ring color
  - `--radius`: Border radius for components
- Use Svelte's built-in transition and animation features.

##SvelteKit Project Structure

- Use the recommended SvelteKit project structure:
  ```
  - src/
    - lib/
    - routes/
    - app.html
  - static/
  - svelte.config.js
  - vite.config.js
  ```

##Component Development

- Create .svelte files for Svelte components.
- Use .svelte.ts files for component logic and state machines.
- Implement proper component composition and reusability.
- Use Svelte's props for data passing.
- Leverage Svelte's reactive declarations for local state management.

##State Management

- Use classes for complex state management (state machines)

##Routing and Pages

- Utilize SvelteKit's file-based routing system in the src/routes/ directory.
- Implement dynamic routes using [slug] syntax.
- Use load functions for server-side data fetching and pre-rendering.
- Implement proper error handling with +error.svelte pages.

##Server-Side Rendering (SSR) and Static Site Generation (SSG)

- Leverage SvelteKit's SSR capabilities for dynamic content.
- Implement SSG for static pages using prerender option.
- Use the adapter-auto for automatic deployment configuration.

##Performance Optimization

- Leverage Svelte's compile-time optimizations.
- Use `{#key}` blocks to force re-rendering of components when needed.
- Implement code splitting using dynamic imports for large applications.
- Profile and monitor performance using browser developer tools.
- Use `$effect.tracking()` to optimize effect dependencies.
- Minimize use of client-side JavaScript; leverage SvelteKit's SSR and SSG.
- Implement proper lazy loading for images and other assets.

##Data Fetching and API Routes

- Use load functions for server-side data fetching.
- Implement proper error handling for data fetching operations.
- Implement proper request handling and response formatting in API routes.
- Use SvelteKit's hooks for global API middleware.

##SEO and Meta Tags

- Use Svelte:head component for adding meta information.
- Implement canonical URLs for proper SEO.
- Create reusable SEO components for consistent meta tag management.

##Accessibility

- Ensure proper semantic HTML structure in Svelte components.
- Implement ARIA attributes where necessary.
- Ensure keyboard navigation support for interactive elements.
- Use Svelte's bind:this for managing focus programmatically.

##Key Conventions

1. Embrace Svelte's simplicity and avoid over-engineering solutions.
2. Use SvelteKit for full-stack applications with SSR and API routes.
3. Prioritize Web Vitals (LCP, FID, CLS) for performance optimization.
4. Use environment variables for configuration management.
5. Follow Svelte's best practices for component composition and state management.
6. Ensure cross-browser compatibility by testing on multiple platforms.
7. Keep your Svelte and SvelteKit versions up to date.

##Documentation

- Svelte 5 Runes: https://svelte-5-preview.vercel.app/docs/runes
- Svelte Documentation: https://svelte.dev/docs
- SvelteKit Documentation: https://kit.svelte.dev/docs
- Paraglide.js Documentation: https://inlang.com/m/gerre34r/library-inlang-paraglideJs/usage

Refer to Svelte, SvelteKit, and Paraglide.js documentation for detailed information on components, internationalization, and best practices.

##Comments

- Use comments at the top of the file whith the file name and to explain what the file is for.
- Use comments to explain why behind the code in more complex functions.
- Use comments to leave TODOs.

## Tech Stack

- SvelteKit
- svelte-5
- vanilla css
- TypeScript
- pnpm package manager
- paraglide.js
- vitest
