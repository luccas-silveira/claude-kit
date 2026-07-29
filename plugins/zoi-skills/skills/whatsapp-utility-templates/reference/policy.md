# Política completa — Templates WABA (categoria Utility)

Referência detalhada da skill `whatsapp-utility-templates`. Fonte: política Meta abril/2025 +
julho/2025, consolidada em `prompts_aliança_seguros/docs/WHATSAPP_TEMPLATES_UTILIDADE.md`.

## Índice
1. As 4 categorias e pricing
2. Definição operacional de Utility
3. O que tira o template de Utility (reclassificação)
4. Estrutura técnica
5. Top 10 razões de rejeição
6. Submissão e operação (GHL → Meta)

---

## 1. As 4 categorias e pricing

| Categoria | Propósito | Preço relativo | Quando usar |
|---|---|---|---|
| Marketing | Promoção, venda, awareness, retargeting | Mais caro | Ofertas, lançamentos, descontos, cart-abandonment, datas comemorativas, renovação genérica |
| Utility | Atualizar/responder ação que o usuário já fez | Médio | Confirmação de pedido, status, lembrete de agendamento, atualização de conta, alerta de fraude |
| Authentication | Apenas OTP / 2FA | Mais barato | Códigos de verificação. Proibido emoji, URL, mídia |
| Service | Resposta dentro da janela aberta de 24h | Grátis na janela | Atendimento humano em conversa ativa |

**Regra de pricing 2025:** Utility enviado **dentro da janela ativa de 24h é gratuito**. Fora da
janela, Utility custa menos que Marketing. Marketing é cobrado sempre.

## 2. Definição operacional de Utility

> "Utility templates share specific, useful updates related to an action the user already took." (Meta)

As 3 condições obrigatórias (a Meta avalia o trio):
1. Acionado por evento real do usuário (cotação solicitada, agendamento criado, pagamento feito,
   vigência próxima do fim).
2. Informa/confirma/orienta sobre **esse** evento específico — não introduz tópico novo.
3. Linguagem neutra, factual e específica — sem persuasão, oferta ou CTA emocional.

Use cases que a Meta aceita como Utility: confirmação de pedido/cotação/agendamento; atualização
de status (envio, processamento, aprovação, vigência); lembrete de evento já agendado; aviso de
conta (saldo, limite, plano); alerta de fraude/segurança/recall; compliance; pesquisa de
satisfação vinculada a transação específica; notificação de falha/inadimplência; suporte público.

## 3. O que tira o template de Utility (reclassificação para Marketing)

As atualizações de abril/2025 e julho/2025 tornaram a fiscalização automática. Gatilhos que
**silenciosamente** movem para Marketing e cobram a diferença:

**3.1 Vocabulário promocional** (banido no body): desconto, oferta, promoção, exclusivo, especial,
limitado, imperdível, condição imperdível, aproveite, garanta já, últimas vagas, compre agora,
contrate agora, peça já, clique aqui, novidade, lançamento.

**3.2 CTA persuasivo / encorajamento de compra:**
- ❌ "Clique para renovar e garanta seu desconto"
- ❌ "Aproveite e contrate agora"
- ❌ "Veja nossas ofertas"

**3.3 Conteúdo misto.** Qualquer linha promocional em template Utility converte o template inteiro
em Marketing. Ex.: recibo + "confira nossos novos produtos" → Marketing.

**3.4 Generalidade / vague placeholders:**
- ❌ Template iniciando ou terminando com `{{1}}`
- ❌ `{{1}}{{2}}` colado sem texto entre
- ❌ Densidade alta de variáveis sem texto fixo de contexto
- Regra prática: mínimo de palavras fixas ≈ **(3 × nº variáveis) + 1**

**3.5 Saudações genéricas desconexas:**
- ❌ "Olá {{1}}, tudo bem? 🎉"
- ❌ "Feliz aniversário!" sem contexto transacional
- ❌ "Como nos avaliaria?" sem referência a transação específica

**3.6 Renovação genérica** (caso direto de seguros):
- ❌ "Sua apólice vence em breve, fale com a gente!" → Marketing (re-engajamento sem ação prévia).
- ✅ "Sua apólice {{1}} vence em {{2}}. Sua nova proposta com cobertura {{3}} está pronta para
  análise. Responda 1 para confirmar, 2 para revisar." → Utility (apólice existente + dados
  específicos + ação concreta sobre transação real).

**3.7 Vínculo de variáveis com dados transacionais reais.** Variáveis devem ser número de pedido,
valor, data, status ou ID — nunca gancho promocional.
- ❌ `{{1}}` = "Imperdível: 30% off"
- ✅ `{{1}}` = "APO-2026-0042"

## 4. Estrutura técnica

### 4.1 Componentes (todos opcionais exceto Body)

| Componente | Conteúdo | Limites |
|---|---|---|
| Header | Texto curto OU mídia (imagem, vídeo, doc, location) | Texto: 60 chars, 1 variável. Mídia: 1 sample no submit |
| Body | Texto principal | Até 1024 chars. Variáveis `{{1}}` `{{2}}` |
| Footer | Texto fixo curto | 60 chars, sem variáveis |
| Buttons | Quick Reply / URL / Phone / Copy code / Flow / OTP | Máx 3 totais, mix permitido |

### 4.2 Sintaxe de variáveis
- Formato exato `{{1}}` `{{2}}` — duas chaves, sem espaço, numeração sequencial sem pular.
- Cada variável precisa de sample value no submit.
- Proibido variável no primeiro/último caractere do body.
- Proibido duas variáveis coladas.

### 4.3 Nome do template
- Apenas `a-z 0-9 _`, lowercase, sem espaço/acento.
- Convenção `[tenant]_[contexto]_v[N]` → `alianca_cotacao_pronta_v1`.
- Evitar palavras que disparam revisão: `test`, `temp`, `oferta`, `promo`.

### 4.4 URLs
- HTTPS completo, domínio próprio registrado no WABA. Sem `bit.ly`, `tinyurl`, `wa.me`, `goo.gl`.

### 4.5 Botões — boas práticas Utility
- Quick Reply: Confirmar, Reagendar, Detalhes, Falar com consultor.
- URL: link de track / portal cliente / agendamento. Nunca link de produto.
- Labels factuais, nunca "Compre já" / "Aproveite".

### 4.6 Idioma
- Selecionar código exato (`pt_BR`). Não misturar idiomas. PT-BR sem erro gramatical (reprova).

## 5. Top 10 razões de rejeição (Meta API)

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

Aprovação: 15–30 min automática; 24–48h manual.

## 6. Submissão e operação (GHL → Meta)

1. GHL: `Conversations → Templates → New`.
2. Categoria Utility (a Meta pode sobrescrever — é sugestão).
3. Nome na convenção, idioma `pt_BR`, body, botões, samples reais.
4. Submeter. Status na lista de Templates do GHL: `APPROVED` / `REJECTED` / `PAUSED` / `PENDING`.
5. Se `REJECTED`: ler motivo, corrigir, resubmeter com `_v2`, `_v3`.
6. Se `APPROVED` mas reclassificado para Marketing: funciona, mas custa mais — reescreva sem os
   sinais promocionais e resubmeta.

Notas operacionais:
- **Quality rating** (High/Medium/Low) por número: rating baixo + Utility ruim = throttle. Monitorar no Business Manager.
- **PAUSED** por excesso de block-by-user: reduzir frequência, revisar conteúdo, resubmeter.
- **Janela de 24h:** depois que o cliente responde, qualquer mensagem livre (não-template) é
  gratuita por 24h. Usar a janela poupa custo de template.

## Fontes oficiais
- https://developers.facebook.com/documentation/business-messaging/whatsapp/templates/template-categorization
- https://developers.facebook.com/documentation/business-messaging/whatsapp/templates/utility-templates/utility-templates/
- https://developers.facebook.com/documentation/business-messaging/whatsapp/templates/overview
- https://www.ycloud.com/blog/whatsapp-api-message-template-category-guidelines-update
- https://sanuker.com/guideline-to-whatsapp-template-message-categories/
- https://m.aisensy.com/blog/whatsapp-template-approval-process/
