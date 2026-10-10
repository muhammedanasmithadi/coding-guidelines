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
