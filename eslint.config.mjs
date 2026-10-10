// Root lint for this repo's own JS (no type-aware rules: no TS sources here).
// Services use enforce/typescript/eslint.config.mjs (strictTypeChecked).
// NOTE: enforce/ is ignored — nested eslint.config.* files get loaded as configs
// by ESLint, and the template's type-aware rules need project type info.
// The template is validated by import smoke test instead (see quality.yml).
import js from '@eslint/js';

export default [
  js.configs.recommended,
  {
    rules: {
      'no-warning-comments': ['error', { terms: ['todo', 'fixme', 'hack'], location: 'anywhere' }],
    },
  },
  { ignores: ['dist/', 'node_modules/', 'enforce/'] },
];
