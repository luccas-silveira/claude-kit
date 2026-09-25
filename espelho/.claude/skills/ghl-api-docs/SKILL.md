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
DOCS=~/.claude/skills/ghl-api-docs/docs
grep -rl 'endpoint:.*contacts' "$DOCS"          # files touching /contacts
grep -i 'POST.*contacts' "$DOCS/ENDPOINTS.md"   # create/write contact endpoints
grep -rl 'scope: contacts.write' "$DOCS"        # endpoints needing a given scope
```

## Gotchas verificados ao vivo (a doc está errada/incompleta nestes pontos)

Fonte: build de um app marketplace (2026-07-02/03/06), tudo testado contra a API real.

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
- **Não existe "reinstalar": a subconta já instalada some da lista de instalação** (medido em
  2026-08-07). O modal "selecionar subcontas" do `/v2/oauth/chooselocation` só lista subcontas
  SEM o app — buscar pelo nome de uma instalada devolve lista vazia, sem mensagem nenhuma.
  Para reaplicar configuração de app (provider novo, escopo novo) numa subconta que já tem o
  app: **desinstale primeiro**, depois instale. A rota antiga `/oauth/chooselocation` (sem
  `/v2`) não é escape — responde `HttpException: No integration found with the id: <appId>`.
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

### Conversation Providers

Medido em 2026-08-07 (ZOI Hub, provider de SMS que entrega WhatsApp).

- **Workflow com ação "Send SMS" NUNCA usa provider marcado como canal extra.** A doc diz isso
  numa linha fácil de perder (`SMS (Add new conversation channel)` → "SMS module is not
  currently supported"), e o sintoma engana: envio manual da tela de conversas funciona, só a
  automação não. Motivo: a conversa guarda `lastMessageConversationProviderId` e o envio manual
  herda dele; o workflow usa o provider **padrão da subconta**. Para automação funcionar, o
  provider tem que ser do tipo "substituir o padrão" — criar SEM marcar "Is this a custom
  conversation provider" e escolher em Settings > Phone Numbers > Advanced Settings > SMS Provider.
  Diagnóstico rápido pela API: `messageType` da mensagem. `TYPE_CUSTOM_PROVIDER_SMS` = canal
  extra; `TYPE_CUSTOM_SMS` = provider padrão do app; `TYPE_SMS` com
  `conversationProviderId: null` = saiu pelo LC Phone/Twilio, cobrando SMS. **Correção de
  2026-08-17:** este bloco dizia que provider padrão gravaria `TYPE_SMS`. Não grava — grava
  `TYPE_CUSTOM_SMS` com o id dele. São três valores, não dois. Use o `conversationProviderId`
  para saber QUAL provider, e o `messageType` só para saber de que família ele é.
- **Confirmado por medição em 2026-08-17: com o provider PADRÃO, o `Send SMS` de workflow chega
  no Delivery URL, com o texto intacto** — inclusive `#`, acento e `\n` (nunca `\r\n`). Duas
  ressalvas medidas: espaço na borda do texto é aparado no caminho, e cada Enter do editor de
  workflow vira `\n\n`, porque ele é de parágrafos.
- **O payload do provider padrão NÃO traz `conversationProviderId` nem `customUserId`; `userId`
  vem presente até em envio de workflow.** Consequência: quem filtra entrega por
  `conversationProviderId` recusa toda automação. E a duplicata clássica ("cliente recebeu duas
  vezes") sai justamente do provider padrão — uma mensagem do composer é entregue AOS DOIS
  providers quando os dois apontam para a mesma Delivery URL. Duplicata e automação legítima
  chegam idênticas em todos os campos; só o par (texto, contato) repetido em segundos as separa.
  A duplicação não é sistemática: 10 entregas com provider e 1 sem, na janela medida.
- **Escolher o provider padrão da subconta NÃO é automatizável.** Existe só leitura —
  `GET /locations/:locationId/conversationChannels/:type` (scope `locations.readonly`), que
  devolve `defaults.SMS` com o id do provider ativo. Não há PUT/POST equivalente em toda a API
  pública. O painel usa `backend.leadconnectorhq.com/locations/:id/conversationChannels/SMS`,
  API interna com sessão de usuário do CRM — não aceita token de app. Consequência de produto:
  esse clique fica no onboarding manual do cliente; automatizável no máximo a **verificação**.
- **Provider criado depois da instalação não chega na subconta já instalada** — e, como não
  existe reinstalar (ver OAuth acima), a migração exige desinstalar e instalar de novo. Criar
  o provider ANTES do primeiro cliente instalar evita a dança inteira.
- Módulos do app (Conversation Providers, Custom JS, …) são aplicados **ao app, não à versão**:
  salvar altera produção mesmo com a versão em `draft`. O marketplace avisa e pede digitar
  `CONFIRM`.

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
