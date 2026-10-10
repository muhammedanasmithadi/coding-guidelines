# TypeScript — Do vs Avoid

Sources: TS Handbook https://www.typescriptlang.org/docs/handbook/intro.html, Google TS https://google.github.io/styleguide/tsguide.html, zod https://zod.dev/basics, neverthrow https://github.com/supermacro/neverthrow

## 1. Naming

Do:

```ts
export const MAX_RETRY_COUNT = 3;
export function isRetryableError(err: unknown): boolean {
  return err instanceof NetworkError;
}
```

Avoid:

```ts
const d = 86400; // smell: magic, cryptic
let flag = true; // smell: unsearchable
```

## 2. Purity + types

Do:

```ts
export function calculateTotal(items: readonly LineItem[], taxRate: number): number {
  return items.reduce((s, i) => s + i.price * i.qty, 0) * (1 + taxRate);
}
```

Avoid:

```ts
export function calc(x) {
  // smell: implicit any + hidden global
  total += x;
  return total;
}
```

## 3. unknown narrowing

Do:

```ts
function parsePayload(input: unknown): string {
  if (typeof input !== 'object' || input === null) throw new ValidationError('object');
  if (!('id' in input) || typeof input.id !== 'string') throw new ValidationError('id');
  return input.id;
}
```

Avoid:

```ts
function parsePayload(input: any) {
  return (input as any).id; // smell: runtime TypeError
}
```

## 4. Errors — Result

Do:

```ts
import { ok, err, type Result } from 'neverthrow';
type DbError = { code: 'NOT_FOUND' | 'DB_DOWN'; message: string };
export async function getUser(id: string): Promise<Result<User, DbError>> {
  try {
    const u = await db.find(id);
    return u ? ok(u) : err({ code: 'NOT_FOUND', message: id });
  } catch (e) {
    return err({ code: 'DB_DOWN', message: String(e) });
  }
}
```

Avoid:

```ts
throw 'not found'; // smell: untyped string-throw
```

## 5. Validation — zod at edge

Do:

```ts
import { z } from 'zod';
const CreateUserSchema = z.object({ email: z.string().email() });
export type CreateUser = z.infer<typeof CreateUserSchema>;
export function handleCreate(input: unknown): CreateUser {
  return CreateUserSchema.parse(input);
}
```

Avoid:

```ts
function handleCreate(b: any) {
  if (!b.email.includes('@')) throw new Error('bad'); // smell: partial, drifts
  return b as CreateUser;
}
```

## 6. Async — AbortController

Do (timeout `5s` is TEAM CHOICE):

```ts
export async function fetchWithTimeout(url: string, ms = 5_000): Promise<Response> {
  const ctl = new AbortController();
  const t = setTimeout(() => ctl.abort(), ms);
  try {
    return await fetch(url, { signal: ctl.signal });
  } finally {
    clearTimeout(t);
  }
}
```

Avoid:

```ts
await fetch(url); // smell: hangs on stalled socket
users.forEach(async (u) => await save(u)); // smell: unawaited
```

## 7. Testing — property

Do:

```ts
import * as fc from 'fast-check';
fc.assert(fc.property(fc.array(fc.nat()), (a) => expect(sum(a)).toBeGreaterThanOrEqual(0)));
```

Avoid:

```ts
const r = await fetch('https://prod/api'); // smell: network in unit, flaky
expect(r.ok).toBe(true);
```

## 8. tsconfig strict

Enforced file is `enforce/typescript/tsconfig.json` (`noEmit: true` for typecheck-only CI). Use `noEmitOnError` instead only for build emits.

Do (`tsconfig.json`, matches `enforce/typescript/tsconfig.json`):

```json
{
  "compilerOptions": {
    "strict": true,
    "noUncheckedIndexedAccess": true,
    "exactOptionalPropertyTypes": true,
    "noImplicitOverride": true,
    "verbatimModuleSyntax": true,
    "isolatedModules": true,
    "noEmit": true
  }
}
```

Avoid:

```json
{ "compilerOptions": { "strict": false } }


// smell: ships null/any bugs
```
