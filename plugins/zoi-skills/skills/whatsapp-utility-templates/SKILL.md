---
name: whatsapp-utility-templates
description: "Use para qualquer pergunta ou tarefa sobre templates de mensagem do WhatsApp Business (WABA, GHL, Meta) — a mensagem pré-aprovada enviada fora da janela de 24h, sobretudo na categoria Utility (transacional, mais barata que Marketing). Acione quando o usuário quiser escrever/criar um template (lembrete, confirmação, cotação, cobrança, boleto, parcela, renovação, agendamento, sinistro) para a Meta aprovar como utilidade; corrigir template rejeitado ou reclassificado como Marketing/promocional; escolher ou travar a categoria no GHL; disparar aviso transacional em massa sem pagar preço de Marketing; ou entender as regras — política de categorização (mudanças de 2025), aprovação e limites técnicos (caracteres do body, botões, variáveis, nome). NÃO use para: mensagem livre dentro da janela ativa de 24h; prompt de imagem; e-mail/post/legenda; ou dúvidas de API/webhook que não tocam o conteúdo nem a categoria do template."
---

# WhatsApp Business — Templates de Utilidade (WABA)

Torna o agente competente para **escrever e revisar** templates WABA que a Meta aprova como
**Utility** sem reclassificar para Marketing. Toda regra aqui rastreia à política Meta
(abril/2025 + julho/2025) consolidada em `reference/policy.md`. Não invente política: se a fonte
não cobre, diga "verificar na doc oficial da Meta".

## Postura (como agir — leia primeiro)

O usuário é o dono da decisão de categoria. Seu papel NÃO é bloquear: é entregar o melhor
template possível e informar o risco **uma vez**.

- **Entregue primeiro.** Sempre produza o template pedido no formato final. Nunca responda só
  com "não dá" nem com um sermão.
- **Conteúdo que não nasce Utility** (aniversário, saudação, agradecimento, promoção) → NÃO
  recuse. Aplique o **Reframe** (seção abaixo): reescreva a intenção do usuário em torno de um
  fato concreto real e entregue a versão com maior chance de passar como Utility.
- **Avise o risco UMA vez, curto.** Uma linha: a Meta classifica pelo conteúdo, não pelo rótulo,
  e pode reclassificar. Não repita a cada turno. Se o usuário entendeu e insiste, entregue e
  pare de alertar.
- **O usuário escolhe a categoria no submit.** Você recomenda; ele decide.

Limite duro (NUNCA cruze): não **fabrique um evento que não aconteceu** ("sua revisão está
pronta" se não está) e não **prometa aprovação garantida** — você não controla o classificador
da Meta. Maximize a chance honestamente; não minta.

## Onde está cada coisa (consulta progressiva)

Este `SKILL.md` resolve o caso comum sozinho. Os arquivos em `reference/` são camadas mais
profundas — abra só a que a tarefa pedir, para não gastar contexto à toa:

- `reference/policy.md` — política completa (categorias, limites, Top 10 razões de rejeição, submissão).
- `reference/templates.md` — biblioteca T1–T8 + variantes complementares (corpos, samples, botões).
- `reference/guia-completo.md` — **o doc detalhado**: mesma política, porém com o racional por trás
  de cada regra, pares contrastantes ✅/❌ e o diagnóstico passo a passo de rejeição e de
  reclassificação. Existe para o **caso difícil**.

**Consulte `reference/guia-completo.md` quando** a decisão não é óbvia e o conteúdo inline não basta:
- o template fica na fronteira Utility/Marketing (renovação, pós-24h, pesquisa de satisfação) e você
  precisa do critério fino para não errar a categoria;
- o motivo de rejeição da Meta não bate com as Top 10 de `policy.md`;
- o gatilho do usuário não tem padrão pronto em `templates.md` e você precisa derivar um novo;
- o usuário pede o porquê de uma regra, o passo a passo de diagnóstico, ou um par contrastante.

**Não abra o guia para o caso comum** — escrever um template que mapeia direto num T1–T8, ou
responder uma dúvida de limite técnico, já está resolvido aqui e em `policy.md`. Ler o arquivo
inteiro sem necessidade só consome contexto.

Ao aplicar uma regra vinda do guia, **cite a seção** (ex.: "guia §4 — gatilhos de reclassificação")
para o usuário poder conferir a origem.

## Quando usar / quando NÃO usar

**Use** para: criar um template WABA novo (qualquer categoria); revisar um template rejeitado;
diagnosticar reclassificação Utility→Marketing; preparar lembrete/confirmação/alerta/atualização
para envio fora da janela de 24h via GHL.

**NÃO use** quando o usuário só quer mandar uma mensagem livre **dentro** da janela de 24h —
isso é texto comum e gratuito, não exige template.

## Por que Utility importa (decore)

A Meta classifica todo template em **uma** de 4 categorias, e a categoria define o preço:

| Categoria | Propósito | Preço |
|---|---|---|
| Marketing | Promoção, venda, awareness | Mais caro, cobrado sempre |
| **Utility** | Atualizar/responder ação que o usuário **já fez** | **Grátis na janela ativa de 24h**; menor que Marketing fora dela |
| Authentication | Apenas OTP / 2FA | Mais barato |
| Service | Resposta dentro da janela aberta de 24h | Grátis na janela |

**Reclassificação é silenciosa.** Desde abril/2025 a fiscalização é automática: se o conteúdo
falhar no teste de Utility, a Meta move o template para Marketing **sem aviso** e cobra a
diferença. O template continua funcionando — você só descobre na fatura.

### Limites técnicos (decore)

| Elemento | Regra |
|---|---|
| Body | Até **1024 caracteres**. Único componente obrigatório. |
| Header | Texto: 60 chars, 1 variável. Ou mídia com 1 sample no submit. |
| Footer | 60 chars, **sem variáveis**. |
| Buttons | Máx **3 no total**. Mix de Quick Reply / URL / Phone / Copy code / Flow / OTP. |
| Variáveis | `{{1}}` `{{2}}` — sequencial, sample real no submit; nunca no 1º/último char; nunca duas coladas. |
| Nome | `a-z 0-9 _`, lowercase, convenção `[tenant]_[contexto]_v[N]`. Evitar `test`, `temp`, `oferta`, `promo`. |
| URL | HTTPS do domínio próprio. Proibido `bit.ly`, `tinyurl`, `wa.me`, `goo.gl`. |
| Dado sensível | Nunca CPF/CNPJ/cartão/senha/RG completos. Últimos 4 OK. |
| Idioma | Um só por template (ex.: `pt_BR`), sem erro de português. |

Aprovação: 15–30 min automática; 24–48h manual. Detalhe completo em `reference/policy.md`.

## As 3 condições inegociáveis para ser Utility

A Meta avalia o trio. Se **qualquer uma** falhar, vira Marketing:

1. **Acionado por um evento real do usuário** — cotação solicitada, agendamento criado,
   pagamento feito, vigência de apólice ativa próxima do fim, sinistro aberto.
2. **Informa/confirma/orienta sobre esse evento específico** — não introduz tópico novo.
3. **Linguagem neutra, factual, específica** — zero persuasão, zero oferta, zero CTA emocional.

## Reframe — quando o pedido não nasce Utility

Pedido como "feliz aniversário", "agradecimento" ou "saudação" não tem evento transacional →
sozinho, é Marketing. Em vez de recusar, **ancore num fato concreto real** e reescreva em torno
dele. O classificador olha o **propósito dominante do body**: quanto mais o texto for sobre o
fato concreto (item reservado, prazo, voucher, status) e menos sobre a celebração, maior a
chance de passar como Utility.

Procedimento:
1. Identifique (ou pergunte ao usuário) se existe um fato concreto real ligado à intenção: um
   brinde reservado em nome do cliente, um voucher liberado, um benefício de programa, um item
   disponível para retirada, um prazo.
2. Reescreva o body como **notificação desse fato** — propósito dominante transacional. A
   intenção original (ex.: aniversário) entra no máximo como o motivo de uma frase, nunca como o
   tema do texto.
3. Corte o que derruba para Marketing: "presente", "aproveite", convite genérico à loja, emojis
   de festa, CTA emocional.
4. Quando útil, entregue 2 variantes: **(A)** máxima chance (sem a palavra sensível) e **(B)**
   mais próxima da intenção (carrega a palavra, risco um pouco maior). Diga qual tem mais chance.
5. Só se NÃO houver fato concreto e o usuário não fornecer um → diga em uma linha que resta o
   caminho Marketing e entregue como Marketing.

Exemplo (aniversário → notificação de brinde reservado):
- ❌ "Feliz aniversário! Tenho um presente, passa na loja tomar um café." → Marketing.
- ✅ "Olá, {{1}}! Separamos um brinde em seu nome, disponível para retirada até {{2}}. Para
  combinar o melhor dia, responda por aqui." → maior chance de Utility.

## Gatilhos de reclassificação Utility → Marketing

O que silenciosamente move o template para Marketing:

- **Vocabulário promocional** (banido no body): desconto, oferta, promoção, exclusivo, especial,
  limitado, imperdível, aproveite, garanta já, últimas vagas, compre agora, contrate agora,
  peça já, clique aqui, novidade, lançamento.
- **CTA persuasivo:** "Clique para renovar e garanta seu desconto", "Aproveite e contrate agora".
- **Conteúdo misto:** uma única linha promocional converte o template **inteiro** em Marketing
  (recibo + "confira nossos novos produtos" → Marketing).
- **Saudação genérica desconexa:** "Olá {{1}}, tudo bem? 🎉"; "Feliz aniversário!" sem contexto
  transacional; "como nos avaliaria?" sem referência a transação específica.
- **Renovação genérica** (a fronteira mais perigosa): ❌ "Sua apólice vence em breve, fale com a
  gente!" → Marketing. ✅ "Sua apólice {{1}} vence em {{2}}. Sua nova proposta com cobertura
  {{3}} está pronta para análise." → Utility.
- **Variáveis não-transacionais:** cada `{{n}}` deve ser número/valor/data/status/ID, nunca gancho
  promocional. ❌ `{{1}}`="Imperdível: 30% off"; ✅ `{{1}}`="APO-2026-0042".
- **Densidade de variáveis:** mínimo de palavras fixas ≈ **(3 × nº de variáveis) + 1**.

## Checklist de 12 itens (rode antes de submeter)

Se falhar 1 item, **sinalize ao usuário** antes do submit (ele decide se sobe assim mesmo).

```
[ ] O evento que gera o envio é claramente uma ação do cliente
    (cotação, agendamento, vencimento de apólice ativa, sinistro aberto).
[ ] Conteúdo é específico — cita apólice, data, número, status.
[ ] Zero palavras promocionais (desconto, oferta, aproveite, exclusivo...).
[ ] Zero saudação desconexa do tópico transacional.
[ ] Body entre 60 e 1024 chars.
[ ] Toda variável tem sample real (ex.: APO-2026-0042, não "exemplo").
[ ] Nenhuma variável encosta no início ou fim do body.
[ ] URLs em HTTPS do domínio próprio (sem bit.ly).
[ ] Botões com labels factuais (Confirmar, Reagendar, Falar com consultor).
[ ] Idioma pt_BR consistente, sem erro de português.
[ ] Não pede CPF/cartão/senha completa.
[ ] Template name segue convenção [tenant]_*_v* sem palavras suspeitas.
```

## Fluxo operacional

### Escrever um template novo
1. **Identifique o evento-gatilho.** Se há ação concreta do cliente, siga direto. Se não há
   (aniversário, saudação, promoção), NÃO recuse — vá para a seção **Reframe** e ancore num fato
   concreto real antes de escrever.
2. **Escolha o T-template mais próximo** na tabela abaixo (80% dos casos mapeiam num existente
   com troca de variáveis). Detalhes completos em `reference/templates.md`.
3. **Escreva body + botões** seguindo as 3 condições.
4. **Rode o checklist de 12 itens** explicitamente na resposta — marque cada `[x]`/`[ ]`. Se algo
   falhar, corrija antes de mostrar ao usuário.
5. **Mostre o template final** com nome, categoria, body, footer, botões e sample de cada variável.
6. **Sinalize riscos de fronteira** — se alguma frase encosta na borda Utility/Marketing, diga
   explicitamente ("se trocar X por Y vira Marketing").

### Revisar um template rejeitado
1. Peça o motivo da rejeição (está na UI do GHL/WABA).
2. Cruze com as Top 10 razões de rejeição em `reference/policy.md`.
3. Proponha a versão corrigida com diff.
4. Rode o checklist de 12 itens na correção. Resubmeta como `_v2`, `_v3`.

### Diagnosticar reclassificação Utility → Marketing
1. Compare o body com os gatilhos de reclassificação acima.
2. Destaque a(s) frase(s) ofensora(s).
3. Reescreva preservando o objetivo de negócio, sem o sinal promocional.
4. Se o objetivo **exige** linguagem promocional, é Marketing mesmo: separe em dois templates
   (um Utility transacional + um Marketing para a oferta).

## Biblioteca T1–T8

Pontos de partida para a operação de seguros (Aliança). Corpos completos, samples e botões em
`reference/templates.md`.

| # | Nome | Gatilho | Categoria |
|---|---|---|---|
| T1 | `alianca_cotacao_em_andamento_v1` | IA encerrou com `[FIM:dados_coletados]` | Utility |
| T2 | `alianca_cotacao_pronta_v1` | Consultor finalizou cotação no Quiver | Utility |
| T3 | `alianca_lembrete_retorno_v1` | Agendamento marcado no calendar GHL | Utility |
| T4 | `alianca_renovacao_d30_v1` | Apólice ativa, vigência −30 dias | Utility (fronteira) |
| T5 | `alianca_sinistro_abertura_v1` | Sinistro registrado | Utility |
| T6 | `alianca_doc_pendente_v1` | Consultor pediu doc | Utility |
| T7 | `alianca_parcela_em_atraso_v1` | Parcela vencida | Utility |
| T8 | `alianca_continuacao_pos_24h_v1` | Conversa retomada após >24h | Utility (defensivo) |

## Casos de fronteira — entregue, não bloqueie

Pedido do usuário por um conteúdo específico **não** é antipadrão — é o trabalho. Para conteúdo
que não nasce Utility (promoção, aniversário, saudação, agradecimento, prospecção), NÃO recuse:
aplique o **Reframe**, entregue a melhor versão Utility-viável e avise o risco **uma vez**. Sem
fato concreto pra ancorar → entregue como Marketing, sem ladainha.

Para referência, o que de fato não nasce Utility e precisa de reframe (ou vira Marketing):
prospecção fria, oferta sem transação ativa, datas comemorativas (Black Friday, aniversário),
saudação genérica, mistura recibo+promo.

Os ÚNICOS limites duros (NUNCA cruze):
- **Não fabrique evento falso.** Ancore só em fato real informado pelo usuário.
- **Não prometa aprovação garantida.** Você não controla o classificador da Meta.
- **Não peça dado sensível completo** (CPF/CNPJ/cartão/senha) — limite técnico da Meta.

## Adaptação multi-tenant

O default assume **Aliança Seguros** (domínio `aliancasegura.com.br`, tenant `alianca`). Para
outros tenants:
- Troque `alianca_*` por `[tenant_id]_*` nos nomes e o domínio nas URLs.
- Adapte os gatilhos T1–T8 ao pipeline do tenant (ex.: agenda de test-drive, inspeção, booking).
- Mantenha as 3 condições + checklist de 12 itens independente do tenant.

## Fontes

- `reference/policy.md` — política completa (categorias, limites, rejeição, submissão).
- `reference/templates.md` — T1–T8 com corpos, samples e botões.
- `reference/guia-completo.md` — guia detalhado (racional, pares ✅/❌, diagnóstico passo a passo).
- [Meta — Template categorization](https://developers.facebook.com/documentation/business-messaging/whatsapp/templates/template-categorization)
- [Meta — Utility templates](https://developers.facebook.com/documentation/business-messaging/whatsapp/templates/utility-templates/utility-templates/)
- [Meta — Template fundamentals](https://developers.facebook.com/documentation/business-messaging/whatsapp/templates/overview)
- [YCloud — July 2025 category guidelines](https://www.ycloud.com/blog/whatsapp-api-message-template-category-guidelines-update)
- [AiSensy — Top 10 rejection reasons](https://m.aisensy.com/blog/whatsapp-template-approval-process/)
