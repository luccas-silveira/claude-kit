# Guia Master — Criação de Templates de Utilidade (WhatsApp / WABA)

Documento operacional para escrever templates que a Meta aprova como **Utility** sem
reclassificar para Marketing. Toda regra abaixo rastreia à política Meta (abril/2025 +
julho/2025) consolidada na fonte canônica `docs/WHATSAPP_TEMPLATES_UTILIDADE.md`.

> Estrutura e regras (Seções 0–6, 8–11) são neutras e servem a qualquer tenant. A Seção 7 usa
> a operação de seguros (Aliança) como biblioteca de exemplos trabalhados — adapte nomes,
> domínio e gatilhos ao seu tenant.

---

## 0. Por que Utility importa

A Meta classifica todo template em uma de 4 categorias, e a categoria define o preço:

| Categoria | Propósito | Preço |
|---|---|---|
| Marketing | Promoção, venda, awareness | Mais caro, **cobrado sempre** |
| **Utility** | Atualizar/responder ação que o usuário **já fez** | Médio fora da janela; **grátis dentro da janela ativa de 24h** |
| Authentication | Apenas OTP / 2FA | Mais barato |
| Service | Resposta dentro da janela aberta de 24h | Grátis na janela |

Dois fatos que justificam o cuidado deste guia:

1. **Utility é gratuito dentro da janela de 24h** de atendimento ativo e mais barato que
   Marketing fora dela. Marketing é cobrado em qualquer caso.
2. **A reclassificação é silenciosa.** Desde abril/2025 a fiscalização é automática: se o
   conteúdo falhar no teste de Utility, a Meta move o template para Marketing **sem aviso** e
   cobra a diferença. O template continua funcionando — você só descobre na fatura.

---

## 1. As 3 condições inegociáveis para ser Utility

A Meta avalia o trio. Se **qualquer uma** falhar, o template vira Marketing:

1. **Acionado por um evento real do usuário** — cotação solicitada, agendamento criado,
   pagamento feito, vigência de apólice ativa próxima do fim, sinistro aberto.
2. **Informa, confirma ou orienta sobre esse evento específico** — não introduz tópico novo,
   não muda de assunto.
3. **Linguagem neutra, factual e específica** — zero persuasão, zero oferta, zero CTA emocional.

Use cases que a Meta aceita como Utility: confirmação de pedido/cotação/agendamento;
atualização de status (envio, processamento, aprovação, vigência); lembrete de evento já
agendado; aviso de conta (saldo, limite, plano); alerta de fraude/segurança/recall; compliance;
pesquisa de satisfação **vinculada a uma transação específica**; notificação de
falha/inadimplência; suporte público (interrupção de serviço).

---

## 2. Limites técnicos

| Elemento | Regra |
|---|---|
| **Body** | Até **1024 caracteres**. Único componente obrigatório. |
| **Header** | Texto: 60 caracteres, **1 variável**. Ou mídia (imagem/vídeo/doc/location) com 1 sample no submit. |
| **Footer** | 60 caracteres, texto fixo, **sem variáveis**. |
| **Buttons** | Máx **3 no total** (limite global). Mix de Quick Reply / URL / Phone / Copy code / Flow / OTP. |
| **Variáveis** | `{{1}}` `{{2}}` — duas chaves, sem espaço, numeração sequencial sem pular. Cada uma com sample real no submit. Nunca no 1º/último caractere do body; nunca duas coladas. |
| **Nome** | `a-z 0-9 _`, lowercase, sem espaço/acento. Convenção `[empresa]_[contexto]_v[N]`. Evitar `test`, `temp`, `oferta`, `promo`. |
| **URL** | HTTPS do domínio próprio registrado no WABA. **Proibido** `bit.ly`, `tinyurl`, `wa.me`, `goo.gl`. |
| **Dado sensível** | Nunca pedir CPF/CNPJ/cartão/senha/RG completos. Últimos 4 dígitos OK, ou mover para formulário web. |
| **Idioma** | Um só por template (ex.: `pt_BR`). Sem misturar idiomas. PT-BR sem erro de ortografia/concordância (erro reprova). |

Tempo de aprovação: 15–30 min na automática; 24–48h em revisão manual.

---

## 3. Regra de variáveis

Variáveis tornam o template genérico — e genérico demais dispara reclassificação. Controles:

- **Densidade:** mínimo de palavras fixas ≈ **(3 × nº de variáveis) + 1**. Um body com 5
  variáveis precisa de ~16 palavras fixas de contexto.
- **Posição:** nunca começar nem terminar o body com `{{n}}`; sempre ter texto antes e depois.
- **Sem colagem:** nada de `{{1}}{{2}}` sem texto entre.
- **Conteúdo transacional:** cada variável deve carregar **número de pedido, valor, data,
  status ou ID** — nunca um gancho promocional.
  - ❌ `{{1}}` = `"Imperdível: 30% off"`
  - ✅ `{{1}}` = `"APO-2026-0042"`

---

## 4. Gatilhos de reclassificação Utility → Marketing

O que silenciosamente move o template para Marketing:

**4.1 Vocabulário promocional (banido no body):** desconto, oferta, promoção, exclusivo,
especial, limitado, imperdível, condição imperdível, aproveite, garanta já, últimas vagas,
compre agora, contrate agora, peça já, clique aqui, novidade, lançamento.

**4.2 CTA persuasivo / encorajamento de compra:**
- ❌ "Clique para renovar e garanta seu desconto"
- ❌ "Aproveite e contrate agora"
- ❌ "Veja nossas ofertas"

**4.3 Conteúdo misto.** Uma única linha promocional converte o template **inteiro** em
Marketing. Recibo + "confira nossos novos produtos" → Marketing.

**4.4 Saudação genérica desconexa:**
- ❌ "Olá {{1}}, tudo bem? 🎉"
- ❌ "Feliz aniversário!" sem contexto transacional
- ❌ "Como nos avaliaria?" sem referência a uma transação específica

**4.5 Renovação genérica** (a fronteira mais perigosa):
- ❌ "Sua apólice vence em breve, fale com a gente!" → Marketing (re-engajamento sem ação prévia).
- ✅ "Sua apólice {{1}} vence em {{2}}. Sua nova proposta com cobertura {{3}} está pronta para
  análise." → Utility (apólice existente + dados específicos + ação concreta sobre transação real).

---

## 5. Processo de criação passo a passo

1. **Identifique o evento-gatilho.** Qual ação do cliente precede o envio? Sem evento concreto
   → é Marketing, não Utility. Não rotule como Utility.
2. **Escolha o padrão mais próximo** na Seção 7 (80% dos casos mapeiam num existente com
   troca de variáveis).
3. **Escreva body + botões** respeitando as 3 condições (Seção 1) e a regra de variáveis (Seção 3).
4. **Rode o checklist de 12 itens** (Seção 6). Se 1 falhar, corrija antes de seguir.
5. **Defina nome, idioma e samples reais** de cada variável.
6. **Submeta** (Seção 10) e acompanhe o status.

---

## 6. Checklist de 12 itens (rode antes de submeter)

Se falhar 1 item, **não submeta**.

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
[ ] Template name segue convenção empresa_*_v* sem palavras suspeitas.
```

---

## 7. Biblioteca de padrões por gatilho

Cada gatilho traz ≥2 exemplos completos. Os primeiros (`T1`–`T8`) são os templates canônicos da
Aliança; os complementares são variantes Utility-safe do mesmo evento. Variáveis marcadas com
sample real.

### 7.1 Cotação

**T1 — `alianca_cotacao_em_andamento_v1`** · gatilho: IA encerrou com `[FIM:dados_coletados]`.
```
Olá {{1}}! Seus dados para a cotação de {{2}} foram registrados em nosso sistema (protocolo {{3}}).
Um de nossos consultores vai analisar e retornar com as melhores opções em até {{4}}.
Se preferir, acompanhe pelo nosso portal: {{5}}

Footer: Aliança Seguros & Consórcios
Buttons: [Quick Reply] Confirmar recebimento · [URL] Acompanhar cotação → https://aliancasegura.com.br/cliente/{{6}}
```
Samples: `{{1}}`=Carlos · `{{2}}`=Seguro Auto · `{{3}}`=COT-2026-0042 · `{{4}}`=1 dia útil · `{{5}}`=https://aliancasegura.com.br/cliente · `{{6}}`=carlos-silva-2042

**T2 — `alianca_cotacao_pronta_v1`** · gatilho: consultor finalizou a cotação no Quiver.
```
Olá {{1}}! Sua cotação de {{2}} (protocolo {{3}}) está pronta.
Resumo:
• Seguradora: {{4}}
• Valor anual: R$ {{5}}
• Vigência sugerida: {{6}}
Posso enviar a proposta completa em PDF agora?

Buttons: [Quick Reply] Sim, enviar · [Quick Reply] Falar com consultor · [URL] Ver no portal → https://aliancasegura.com.br/cliente/{{7}}
```
Samples: `{{1}}`=Carlos · `{{2}}`=Seguro Auto · `{{3}}`=COT-2026-0042 · `{{4}}`=Porto Seguro · `{{5}}`=2.480,00 · `{{6}}`=12 meses · `{{7}}`=carlos-silva-2042

### 7.2 Agendamento

**T3 — `alianca_lembrete_retorno_v1`** · gatilho: agendamento marcado no calendar GHL.
```
Olá {{1}}! Lembrete: nosso consultor {{2}} vai te ligar em {{3}} às {{4}} para falar sobre a sua cotação de {{5}} (protocolo {{6}}).
Se precisar reagendar, é só responder aqui.

Buttons: [Quick Reply] Confirmar horário · [Quick Reply] Reagendar
```
Samples: `{{1}}`=Carlos · `{{2}}`=Marina · `{{3}}`=23/06/2026 · `{{4}}`=14h · `{{5}}`=Seguro Auto · `{{6}}`=COT-2026-0042

**Complementar — `alianca_agendamento_confirmado_v1`** · gatilho: cliente acabou de escolher o horário.
```
Olá {{1}}! Seu retorno sobre {{2}} (protocolo {{3}}) ficou agendado para {{4}} às {{5}} com o consultor {{6}}.
Você vai receber um lembrete no dia. Para alterar, responda aqui.

Buttons: [Quick Reply] Está confirmado · [Quick Reply] Reagendar
```
Samples: `{{1}}`=Carlos · `{{2}}`=Seguro Auto · `{{3}}`=COT-2026-0042 · `{{4}}`=23/06/2026 · `{{5}}`=14h · `{{6}}`=Marina

### 7.3 Renovação (fronteira sensível — par contrastante obrigatório)

**T4 — `alianca_renovacao_d30_v1` (✅ Utility)** · gatilho: apólice ativa, vigência termina em 30 dias.
```
Olá {{1}}! Sua apólice de {{2}} (número {{3}}) vence em {{4}}.
Para evitar interrupção da cobertura, já iniciamos o processo de renovação. Nosso consultor vai retornar com a nova proposta em até {{5}}.
Algum ajuste no perfil (novo condutor, mudança de endereço, alteração de uso)?

Buttons: [Quick Reply] Sem alterações · [Quick Reply] Tenho atualizações · [Quick Reply] Falar com consultor
```
Samples: `{{1}}`=Carlos · `{{2}}`=Seguro Auto · `{{3}}`=APO-2026-0042 · `{{4}}`=30/07/2026 · `{{5}}`=2 dias úteis
**Por que é Utility:** cita apólice específica, data exata de vencimento, refere transação ativa. Zero promo.

**❌ Versão que vira Marketing** (mesmo gatilho, redação errada):
```
Olá {{1}}! 🎉 Aproveite e renove sua apólice com 10% de desconto antecipado. Oferta por tempo limitado — garanta já!
```
**Por que reprova:** vocabulário promocional ("aproveite", "desconto", "oferta", "limitado",
"garanta já") + CTA persuasivo. A Meta reclassifica para Marketing automaticamente (regra 4.1/4.2).

### 7.4 Sinistro

**T5 — `alianca_sinistro_abertura_v1`** · gatilho: sinistro registrado.
```
Olá {{1}}! Confirmamos a abertura do sinistro {{2}} na apólice {{3}}.
Próximos passos:
1. Análise inicial em até {{4}}
2. Vistoria (se aplicável)
3. Contato do regulador
Em caso de urgência, acesse: https://aliancasegura.com.br/servicos

Buttons: [URL] Acompanhar sinistro → https://aliancasegura.com.br/sinistro/{{5}} · [Phone] Falar com a central
```
Samples: `{{1}}`=Carlos · `{{2}}`=SIN-2026-0117 · `{{3}}`=APO-2026-0042 · `{{4}}`=2 dias úteis · `{{5}}`=sin-2026-0117

**Complementar — `alianca_sinistro_vistoria_v1`** · gatilho: vistoria agendada no sinistro aberto.
```
Olá {{1}}! Sobre o sinistro {{2}} (apólice {{3}}): a vistoria foi agendada para {{4}} às {{5}}, no endereço {{6}}.
O vistoriador {{7}} é o responsável. Para reagendar, responda aqui.

Buttons: [Quick Reply] Confirmar vistoria · [Quick Reply] Reagendar · [URL] Detalhes → https://aliancasegura.com.br/sinistro/{{8}}
```
Samples: `{{1}}`=Carlos · `{{2}}`=SIN-2026-0117 · `{{3}}`=APO-2026-0042 · `{{4}}`=25/06/2026 · `{{5}}`=10h · `{{6}}`=Rua X, 123 · `{{7}}`=João · `{{8}}`=sin-2026-0117

### 7.5 Documento pendente

**T6 — `alianca_doc_pendente_v1`** · gatilho: consultor identificou doc faltando.
```
Olá {{1}}! Para finalizar sua {{2}} (protocolo {{3}}), precisamos do seguinte documento:
• {{4}}
Pode nos enviar por aqui mesmo ou pelo portal seguro: https://aliancasegura.com.br/upload/{{5}}

Buttons: [Quick Reply] Vou enviar agora · [Quick Reply] Falar com consultor
```
Samples: `{{1}}`=Carlos · `{{2}}`=contratação de Seguro Auto · `{{3}}`=COT-2026-0042 · `{{4}}`=CNH digitalizada (frente e verso) · `{{5}}`=carlos-silva-2042

**Complementar — `alianca_doc_recebido_v1`** · gatilho: documento pendente foi recebido.
```
Olá {{1}}! Recebemos o documento {{2}} referente à sua {{3}} (protocolo {{4}}).
Está tudo certo e seguimos com a análise. Próximo retorno em até {{5}}.

Buttons: [URL] Acompanhar → https://aliancasegura.com.br/cliente/{{6}}
```
Samples: `{{1}}`=Carlos · `{{2}}`=CNH digitalizada · `{{3}}`=contratação de Seguro Auto · `{{4}}`=COT-2026-0042 · `{{5}}`=1 dia útil · `{{6}}`=carlos-silva-2042

### 7.6 Parcela / pagamento

**T7 — `alianca_parcela_em_atraso_v1`** · gatilho: parcela vencida sem pagamento.
```
Olá {{1}}! Identificamos que a parcela {{2}} da apólice {{3}} venceu em {{4}} e ainda não foi compensada (valor R$ {{5}}).
Para manter a cobertura ativa, o pagamento pode ser feito até {{6}} via:
• Boleto: {{7}}
• Pix: chave {{8}}

Buttons: [URL] 2ª via do boleto → https://aliancasegura.com.br/boleto/{{9}} · [Quick Reply] Falar com financeiro
```
Samples: `{{1}}`=Carlos · `{{2}}`=03/12 · `{{3}}`=APO-2026-0042 · `{{4}}`=15/06/2026 · `{{5}}`=248,00 · `{{6}}`=28/06/2026 · `{{7}}`=23793.38128 · `{{8}}`=financeiro@aliancasegura.com.br · `{{9}}`=apo-2026-0042-p3

**Complementar — `alianca_parcela_paga_v1`** · gatilho: pagamento da parcela compensado.
```
Olá {{1}}! Confirmamos o pagamento da parcela {{2}} da apólice {{3}}, no valor de R$ {{4}}, recebido em {{5}}.
Sua cobertura segue ativa. Próxima parcela: {{6}}.

Footer: Aliança Seguros & Consórcios
```
Samples: `{{1}}`=Carlos · `{{2}}`=03/12 · `{{3}}`=APO-2026-0042 · `{{4}}`=248,00 · `{{5}}`=27/06/2026 · `{{6}}`=15/07/2026

### 7.7 Pós-24h (uso defensivo)

**T8 — `alianca_continuacao_pos_24h_v1`** · gatilho: conversa real ficou com pergunta pendente e passaram >24h.
```
Olá {{1}}! Sobre o {{2}} que conversamos no dia {{3}} (protocolo {{4}}), notei que sua resposta ficou em aberto.
Para seguir com a cotação, ainda preciso de: {{5}}
Quando você puder, me responde por aqui que eu sigo daí.

Buttons: [Quick Reply] Vou responder agora · [Quick Reply] Não tenho mais interesse
```
Samples: `{{1}}`=Carlos · `{{2}}`=Seguro Auto · `{{3}}`=20/06/2026 · `{{4}}`=COT-2026-0042 · `{{5}}`=o ano do veículo
**Risco:** disparo em massa para leads frios → Meta reclassifica para Marketing. Usar **apenas**
quando houve conversa real e ficou pergunta pendente registrada.

**Complementar — `alianca_continuacao_doc_pos24h_v1`** · gatilho: doc pendente não enviado, >24h.
```
Olá {{1}}! Sobre a sua {{2}} (protocolo {{3}}): ainda está pendente o documento {{4}} para a gente finalizar.
Pode enviar por aqui ou pelo portal: https://aliancasegura.com.br/upload/{{5}}

Buttons: [Quick Reply] Vou enviar agora · [Quick Reply] Falar com consultor
```
Samples: `{{1}}`=Carlos · `{{2}}`=contratação de Seguro Auto · `{{3}}`=COT-2026-0042 · `{{4}}`=CNH digitalizada · `{{5}}`=carlos-silva-2042

---

## 8. O que SEMPRE é Marketing (nunca Utility)

- ❌ "Olá! Você sabia que a Aliança tem seguro auto a partir de R$ 80/mês?" → cold outreach, sem ação prévia.
- ❌ "Aproveite nossa condição de Black Friday em seguros residenciais!" → promo pura.
- ❌ "Renove sua apólice com 5% de desconto antecipado!" → promo embutida.
- ❌ "Bom dia, {{1}}! 🎉 Como podemos te ajudar hoje?" → saudação genérica sem evento.
- ❌ "Sua cotação está pronta — e temos uma surpresa pra você 🎁" → mistura Utility + promo.
- ❌ "Feliz aniversário, {{1}}! Que tal aproveitar essa data com a gente?" → data comemorativa.

Regra-resumo: prospecção fria, oferta sem transação ativa e datas comemorativas são sempre Marketing.

---

## 9. Diagnóstico de rejeição e de reclassificação

### 9.1 Rejeição (template volta como REJECTED)

| # | Causa | Fix |
|---|---|---|
| 1 | Linguagem promocional ou caps lock / `!!!` | Tom factual, sem ênfase artificial |
| 2 | Variável no início ou fim do body | Adicionar texto fixo antes/depois |
| 3 | URL com encurtador | Trocar por HTTPS do domínio próprio |
| 4 | Pede dado sensível completo (CPF, cartão, senha, RG) | Últimos 4 dígitos OU formulário web |
| 5 | Conteúdo vago / ambíguo | Especificar contexto + ação |
| 6 | Mistura PT + EN | Versões separadas, idioma único cada |
| 7 | Body > 1024 caracteres | Cortar / mover para Flow ou link |
| 8 | Categoria errada (Utility com promo) | Remover promo OU reclassificar para Marketing |
| 9 | Sample value ausente em mídia/variável | Subir sample no submit |
| 10 | Nome com `test`, `temp`, `oferta` | Renomear pela convenção |

### 9.2 Reclassificação Utility → Marketing (APPROVED, mas categoria mudou)

1. Compare o body com os gatilhos da Seção 4.
2. Destaque a(s) frase(s) ofensora(s) — geralmente vocabulário promocional, CTA persuasivo,
   saudação desconexa ou renovação genérica.
3. Reescreva mantendo o objetivo de negócio, sem o sinal promocional.
4. Se o objetivo **exige** linguagem promocional, é Marketing mesmo: separe em dois templates
   (um Utility transacional + um Marketing para a oferta).

---

## 10. Submissão (GHL → Meta)

1. GHL: `Conversations → Templates → New`.
2. Categoria **Utility** (a Meta pode sobrescrever — é sugestão).
3. Nome na convenção, idioma `pt_BR`, body, botões, samples reais.
4. Submeter. Auto-review em 15–30 min; status visível na lista de Templates do GHL
   (`APPROVED` / `REJECTED` / `PAUSED` / `PENDING`).
5. Se `REJECTED`: ler o motivo, corrigir, resubmeter com `_v2`, `_v3`.
6. Se `APPROVED` mas reclassificado para Marketing: funciona, mas custa mais — reescreva para
   remover os sinais promocionais e resubmeta.

Notas operacionais:
- **Quality rating** (High/Medium/Low) por número: rating baixo + Utility ruim = throttle de envio. Monitorar no Business Manager.
- **PAUSED** por excesso de block-by-user: reduzir frequência, revisar conteúdo, resubmeter.
- **Janela de 24h:** depois que o cliente responde, qualquer mensagem livre (não-template) é
  gratuita por 24h. Usar essa janela poupa custo de template.

---

## 11. Fontes

- Fonte canônica do projeto: `prompts_aliança_seguros/docs/WHATSAPP_TEMPLATES_UTILIDADE.md`
- Skill `whatsapp-utility-templates` (política + checklist + T1–T8)
- [Meta — Template categorization](https://developers.facebook.com/documentation/business-messaging/whatsapp/templates/template-categorization)
- [Meta — Utility templates](https://developers.facebook.com/documentation/business-messaging/whatsapp/templates/utility-templates/utility-templates/)
- [Meta — Template fundamentals](https://developers.facebook.com/documentation/business-messaging/whatsapp/templates/overview)
- [YCloud — July 2025 category guidelines update](https://www.ycloud.com/blog/whatsapp-api-message-template-category-guidelines-update)
- [Sanuker — Template categories 2025 guide](https://sanuker.com/guideline-to-whatsapp-template-message-categories/)
- [AiSensy — Top 10 rejection reasons](https://m.aisensy.com/blog/whatsapp-template-approval-process/)
