# TypeScript robustness principles (T3 / Total TypeScript practice) — Do vs Avoid

Principles below are normative. tRPC and t3-env are cited as conforming examples,
not mandates: any tool that satisfies the principle conforms.
Sources: T3 env https://create.t3.gg/en/usage/env-variables, T3 tRPC https://create.t3.gg/en/usage/trpc, t3-env https://env.t3.gg/, Total TypeScript Zod https://www.totaltypescript.com/tutorials/zod, tRPC https://trpc.io/

## 1. Validated, typed config at boot (t3-env is one conforming approach)

Do — every variable validated at boot, server/client split, `.env.example` committed:

```ts
import { createEnv } from '@t3-oss/env-nextjs';
import { z } from 'zod';

export const env = createEnv({
  server: { DATABASE_URL: z.string().url(), RETRY_BUDGET: z.coerce.number() },
  client: {},
  runtimeEnv: {
    DATABASE_URL: process.env.DATABASE_URL,
    RETRY_BUDGET: process.env.RETRY_BUDGET,
  },
});
```

Avoid:

```ts
const dbUrl = process.env.DATABASE_URL; // smell: string|undefined, fails at 3am not boot
```

## 2. End-to-end type safety between client and server (tRPC is one conforming approach)

Do — Zod input at the edge, resolver returns values (throw typed errors), export the type only:

```ts
const userRouter = createTRPCRouter({
  getById: publicProcedure.input(z.string()).query(({ ctx, input }) => {
    return ctx.db.user.findFirst({ where: { id: input } });
  }),
});
export type AppRouter = typeof appRouter; // client imports the type, never server code
```

Avoid — hand-rolled fetch + manual method/body validation (see T3 comparison: URL strings, method checks, untyped JSON).

## 3. Caller-based integration tests (not mocks)

Do — test through `createCaller` with a real context (T3 sample test):

```ts
const ctx = await createInnerTRPCContext({ session: null });
const caller = appRouter.createCaller(ctx);
const example = await caller.example.hello({ text: 'test' });
expect(example).toMatchObject({ greeting: 'Hello test' });
```

Avoid: `assert mock.called` — checks the mock, not behavior (see `testing-gaps.md`, AI-slop §1).

## 4. Exhaustive handling with `never`

Do:

```ts
function area(s: Shape): number {
  switch (s.kind) {
    case 'circle':
      return Math.PI * s.r ** 2;
    case 'square':
      return s.s ** 2;
    default:
      throw new Error(`unhandled: ${s satisfies never}`);
  }
}
```

Avoid: silent `default: return 0` — new union members fail silently instead of at compile time.

## 5. Preserve types across the wire

Do: `superjson` transformer so `Date` arrives as `Date`, not string (T3 default). Avoid: manual `new Date(s)` rehydration scattered per call site.
