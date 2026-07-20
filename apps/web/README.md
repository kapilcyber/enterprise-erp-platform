# Finance Control Center

Finance-only Next.js frontend for the Enterprise ERP Platform. The browser talks to FastAPI through same-origin route handlers, while access and refresh tokens remain in secure HttpOnly cookies.

## Configuration

Create `apps/web/.env.local`:

```env
ERP_API_URL=http://localhost:8000/api/v1
ERP_TENANT_ID=00000000-0000-0000-0000-000000000001
NEXT_PUBLIC_APP_NAME=Enterprise ERP
```

`ERP_API_URL` and `ERP_TENANT_ID` are server-only variables and are not included in the browser bundle.

## Run

```bash
npm install
npm run dev
```

Open `http://localhost:3000`. The authenticated application is available under `/finance`.

## Verification

```bash
npm run lint
npm run typecheck
npm test
npm run test:e2e
npm run build
```

The end-to-end suite requires Playwright browsers (`npx playwright install chromium webkit`).
