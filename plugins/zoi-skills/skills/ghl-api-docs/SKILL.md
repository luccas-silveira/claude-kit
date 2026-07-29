---
name: ghl-api-docs
description: Offline reference for the GoHighLevel (GHL / LeadConnector / HighLevel) Marketplace API v3. Use whenever a task involves a GHL/LeadConnector REST endpoint — contacts, conversations, calendars, opportunities, invoices, payments, social planner, webhooks, OAuth, custom fields, etc. Covers method, path, required scope, parameters, and example payloads for ~529 endpoints. Triggers on "GHL", "GoHighLevel", "HighLevel", "LeadConnector", "services.leadconnectorhq.com", or any GHL API/webhook/OAuth question.
---

# GoHighLevel API Reference (offline mirror)

A local, AI-optimized mirror of the GHL Marketplace docs (v3) is bundled with this
skill at `docs/` (a symlink to `~/Documents/ghl-docs`, the git-versioned canonical copy):

```
<skill dir>/docs/        # 828 pages, organized by resource
~/Documents/ghl-docs/    # same files, canonical location
```

Use it instead of guessing endpoint shapes or fetching the web.

## How to find what you need (fast path)

1. **Open `ENDPOINTS.md`** first — the entire API surface in one table (529 endpoints), grouped by resource (`## ghl/contacts`, `## ghl/calendars`, …). Columns: `Method · Path · Title · Scope · File`. Scan or `grep` it to locate the right endpoint and its file.
2. **Open that file** (path is in the table) for full detail: parameters, schema, example request/response.
3. Top-level `index.md` lists the sections; each `<section>/README.md` lists its pages with one-line summaries.

## Querying with grep (frontmatter is structured)

Every page has YAML frontmatter: `title`, `source_url`, `version`, `method`, `endpoint`, `scope`, `summary`.

```bash
DOCS=/Users/luccassilveira/Documents/ghl-docs
grep -rl 'endpoint:.*contacts' "$DOCS"          # files touching /contacts
grep -i 'POST.*contacts' "$DOCS/ENDPOINTS.md"   # create/write contact endpoints
grep -rl 'scope: contacts.write' "$DOCS"        # endpoints needing a given scope
```

## Gotchas verificados ao vivo (a doc está errada/incompleta nestes pontos)

Fonte: build do app blacklist (2026-07-02/03/06), tudo testado contra a API real.
Detalhes e evidências: `~/Desktop/Projetos_ZOI/blacklist/DECISOES.md`.

### OAuth e instalação de app marketplace

- **`POST /oauth/token` — campos são snake_case**: `user_type` e `redirect_uri`. A página de doc
  (get-access-token.md) mostra `userType`/`redirectUri`, mas a API responde 422
  "property userType should not exist".
- **Sem `user_type=Location` o token sai como Company** (agência, sem `locationId`), mesmo com
  distribuição Sub-Account e escolhendo subconta no chooselocation. Enviar
  `user_type=Location` na troca do code E no refresh quando o app é por subconta.
- **O GHL pode conceder o install como AGÊNCIA mesmo com distribuição Sub-Account** — o callback
  precisa aceitar os dois. Fluxo robusto: token Company → `GET /oauth/installed-locations` →
  `POST /oauth/location-token` por location. Não lute contra; implemente os dois caminhos.
- URL de autorização (não está óbvia na doc):
  `https://marketplace.gohighlevel.com/oauth/chooselocation?response_type=code&redirect_uri=…&client_id=…&scope=a+b+c`.
  O `code` é de uso único — erro no callback exige refazer o fluxo inteiro.
- **Endpoints `/oauth/installed-locations` e `/oauth/location-token` usam `Version: v3`**
  (data tipo `2021-07-28` → 404 "Cannot GET" — o header Version ROTEIA no gateway; versão
  errada parece rota inexistente). O location-token responde em **camelCase**
  (`accessToken`/`refreshToken`/`expiresIn`) e INCLUI refresh token. installed-locations
  devolve `items`, não `locations`. Body do location-token: `companyId`/`locationId` (camel).
- **`/oauth/installed-locations` pagina em 20 por default e trunca em silêncio** — use
  `pageSize=100` + loop em `pagination.nextPageToken`/`hasNextPage`. Location desativada
  → `POST /oauth/location-token` responde 400 "Location is not active" (esperado; ela não
  troca mensagens mesmo).
- **Instalar uma location nova pelo painel da agência NÃO chama o redirect OAuth do app** —
  o banco de installs fica defasado em silêncio. Solução em camadas: (1) tratar os webhooks
  de ciclo de vida **`type: "INSTALL"` / `"UNINSTALL"`** (chegam no webhook do app com
  `locationId` + `companyId`) mintando/removendo o token na hora; (2) self-heal: location
  desconhecida numa request → tentar mintar via token de agência antes de recusar.

### Webhooks

- **Assinatura: header atual é `X-GHL-Signature` (Ed25519)** sobre o corpo bruto, base64.
  O legado `X-WH-Signature` (RSA SHA256) foi **deprecado em 2026-07-01**. Chaves públicas em
  `webhook/WebhookIntegrationGuide.md`.
- **Retry, nuance**: "não faz retry em 5xx" vale pra erro retornado PELA APLICAÇÃO (por isso
  sempre responda 200 e processe async). Serviço totalmente fora do ar (connection refused /
  502 do proxy) → o GHL REENTREGA depois (observado: reentrega 13 s após o serviço voltar,
  ~5 min após o evento).
- **`InboundMessage` de Conversation Provider custom**: `messageType: "Custom"` e
  **`from`/`to` vêm como `{}` (dicts vazios!)** — sem telefone no payload. Pra casar por
  número, resolver via `GET /contacts/{contactId}` (o contactId sempre vem). Em SMS/Call
  nativos o payload traz `from`/`to` como string E.164; em Email, endereços
  (formato `Nome <a@b.c>` possível). Canais do webhook: Call, Voicemail, SMS, GMB, FB, IG,
  Email, Live Chat.
- O webhook do app também recebe eventos que não são de mensagem (INSTALL, UNINSTALL, etc.)
  — logue os tipos desconhecidos; ficar cego a eles custou um bug de install dessincronizado.

### Conversas (API)

- **Não existe DELETE de mensagem individual** — granularidade mínima é a conversa
  (`DELETE /conversations/:id`, scope conversations.write). O contato sobrevive; mensagem
  nova do mesmo número cria conversa **nova (ID diferente), sem ressuscitar o histórico**.
  GET numa conversa apagada responde **400** (não 404).
- **`GET /conversations/search` é indexado (ES) com atraso** — pós-delete demora ~5 s pra
  refletir; conversa nova demora ~1 min pra aparecer no filtro `contactId` (mesmo já
  existindo no GET direto e na lista geral). NUNCA use o search como verdade imediata;
  o webhook já entrega `conversationId` pronto. Filtros úteis: `locationId`, `contactId`,
  `query` (nome/telefone), `sortBy=last_message_date&sort=desc`.
- Push de mensagem (provider custom): chega SEM preview do texto; após apagar a conversa,
  clicar na notificação não abre nada — vazamento por push ≈ zero nesse canal.

### Custom Pages e Custom JS (UI de app)

- **Handshake `REQUEST_USER_DATA`**: o GHL só responde em Custom Pages renderizadas por ele.
  Iframe injetado via Custom JS NÃO recebe resposta (timeout) — autenticação ali precisa de
  outro mecanismo server-side (PIN, etc.). Não gaste tempo tentando o handshake fora da
  Custom Page oficial.
- **Contexto criptografado** (Custom Page oficial): formato CryptoJS.AES/OpenSSL —
  base64 de `Salted__` + salt(8) + ciphertext; chave+IV por EVP_BytesToKey com **MD5**
  (secret = shared secret do app). Payload decriptado: `userId`, `companyId`, `role`
  (`admin`/`user`), `userName`, `email` e — em contexto de location — `activeLocation`.
- **`AppUtils` (Custom JS)** — `Utilities.getCurrentUser()` (tem `role`), `getCurrentLocation()`,
  eventos `routeLoaded`/`routeChangeEvent`, `RouteHelper.navigate()`. Tudo roda no NAVEGADOR:
  serve pra UX (esconder item de menu de não-admin), NUNCA pra autorização — é forjável.
- **O campo Custom JS do painel espera HTML** — cole `<script src="https://…"></script>`,
  não a URL crua nem só o JS.
- Hospedagem de Custom Page: HTTPS, sem `X-Frame-Options` restritivo, `frame-ancestors`
  liberando domínios GHL (inclui domínios whitelabel tipo `app.zoitech.com.br`; o path é
  sempre `/v2/location/{id}/…`).
- Padrão que funcionou pra UI discreta: Custom JS injeta item no menu de **Configurações**
  da subconta (clonar um `li` existente do menu herda o estilo do tema) → modal com iframe
  da página; servir a página com `Cache-Control: no-store` e cache-bust no src do iframe
  (o GHL/navegador segura JS/HTML velho e transforma qualquer fix em "não funcionou").

### Limites

- Rate limits API 2.0: **100 req/10 s (burst) e 200k/dia por app POR location** — folga
  enorme pra apps internos; não precisa de fila pra volumes normais.

## Notes

- Base URL for all endpoints: `https://services.leadconnectorhq.com`.
- Paths in the manifest use `:param` placeholders (e.g. `/contacts/:contactId`).
- `source_url` in each file links back to the live doc — re-scrape to refresh; the corpus is git-versioned, so `git diff` shows what GHL changed.
- This is reference-only; it does not make API calls.
