// Root lint for this repo's own JS (no type-aware rules: no TS sources here).
// Services use enforce/typescript/eslint.config.mjs (strictTypeChecked).
import js from '@eslint/js';

export default [
  js.configs.recommended,
  {
    rules: {
      'no-warning-comments': ['error', { terms: ['todo', 'fixme', 'hack'], location: 'anywhere' }],
    },
  },
  { ignores: ['dist/', 'node_modules/'] },
];
