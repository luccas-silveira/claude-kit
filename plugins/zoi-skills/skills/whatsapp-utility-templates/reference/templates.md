# Biblioteca T1–T8 — templates Utility prontos (Aliança Seguros)

Referência da skill `whatsapp-utility-templates`. Pontos de partida testados; adapte variáveis e
domínio ao tenant. Todos são Utility-safe (zero promo, variáveis transacionais, samples reais).

---

## T1. `alianca_cotacao_em_andamento_v1` (Utility)
**Gatilho:** cliente conversou com a IA, encerrou com `[FIM:dados_coletados]`.
```
Body:
Olá {{1}}! Seus dados para a cotação de {{2}} foram registrados em nosso sistema (protocolo {{3}}).
Um de nossos consultores vai analisar e retornar com as melhores opções em até {{4}}.
Se preferir, você pode acompanhar pelo nosso portal: {{5}}

Footer: Aliança Seguros & Consórcios
Buttons:
- Quick Reply: "Confirmar recebimento"
- URL: "Acompanhar cotação" → https://aliancasegura.com.br/cliente/{{6}}
```
Samples: `{{1}}`=Carlos · `{{2}}`=Seguro Auto · `{{3}}`=COT-2026-0042 · `{{4}}`=1 dia útil · `{{5}}`=https://aliancasegura.com.br/cliente · `{{6}}`=carlos-silva-2042

---

## T2. `alianca_cotacao_pronta_v1` (Utility)
**Gatilho:** consultor finalizou a cotação no Quiver.
```
Body:
Olá {{1}}! Sua cotação de {{2}} (protocolo {{3}}) está pronta.
Resumo:
• Seguradora: {{4}}
• Valor anual: R$ {{5}}
• Vigência sugerida: {{6}}
Posso enviar a proposta completa em PDF agora?

Buttons:
- Quick Reply: "Sim, enviar"
- Quick Reply: "Falar com consultor"
- URL: "Ver no portal" → https://aliancasegura.com.br/cliente/{{7}}
```
Samples: `{{1}}`=Carlos · `{{2}}`=Seguro Auto · `{{3}}`=COT-2026-0042 · `{{4}}`=Porto Seguro · `{{5}}`=2.480,00 · `{{6}}`=12 meses · `{{7}}`=carlos-silva-2042

---

## T3. `alianca_lembrete_retorno_v1` (Utility)
**Gatilho:** agendamento marcado no calendar GHL.
```
Body:
Olá {{1}}! Lembrete: nosso consultor {{2}} vai te ligar em {{3}} às {{4}} para falar sobre a sua cotação de {{5}} (protocolo {{6}}).
Se precisar reagendar, é só responder aqui.

Buttons:
- Quick Reply: "Confirmar horário"
- Quick Reply: "Reagendar"
```
Samples: `{{1}}`=Carlos · `{{2}}`=Marina · `{{3}}`=23/06/2026 · `{{4}}`=14h · `{{5}}`=Seguro Auto · `{{6}}`=COT-2026-0042

---

## T4. `alianca_renovacao_d30_v1` (Utility — limite na fronteira)
**Gatilho:** apólice ativa, vigência termina em 30 dias.
```
Body:
Olá {{1}}! Sua apólice de {{2}} (número {{3}}) vence em {{4}}.
Para evitar interrupção da cobertura, já iniciamos o processo de renovação. Nosso consultor vai retornar com a nova proposta em até {{5}}.
Algum ajuste no perfil (novo condutor, mudança de endereço, alteração de uso)?

Buttons:
- Quick Reply: "Sem alterações"
- Quick Reply: "Tenho atualizações"
- Quick Reply: "Falar com consultor"
```
Samples: `{{1}}`=Carlos · `{{2}}`=Seguro Auto · `{{3}}`=APO-2026-0042 · `{{4}}`=30/07/2026 · `{{5}}`=2 dias úteis
**Por que é Utility:** cita apólice específica (`{{3}}`), data exata de vencimento (`{{4}}`), refere transação ativa. Zero promo.
**Risco:** se mudar a redação para "Aproveite e renove com 10% off" → vira Marketing automaticamente.

---

## T5. `alianca_sinistro_abertura_v1` (Utility)
**Gatilho:** sinistro registrado.
```
Body:
Olá {{1}}! Confirmamos a abertura do sinistro {{2}} na apólice {{3}}.
Próximos passos:
1. Análise inicial em até {{4}}
2. Vistoria (se aplicável)
3. Contato do regulador
Em caso de urgência, acesse: https://aliancasegura.com.br/servicos

Buttons:
- URL: "Acompanhar sinistro" → https://aliancasegura.com.br/sinistro/{{5}}
- Phone: "Falar com a central"
```
Samples: `{{1}}`=Carlos · `{{2}}`=SIN-2026-0117 · `{{3}}`=APO-2026-0042 · `{{4}}`=2 dias úteis · `{{5}}`=sin-2026-0117

---

## T6. `alianca_doc_pendente_v1` (Utility)
**Gatilho:** consultor identificou doc faltando.
```
Body:
Olá {{1}}! Para finalizar sua {{2}} (protocolo {{3}}), precisamos do seguinte documento:
• {{4}}
Pode nos enviar por aqui mesmo ou pelo portal seguro: https://aliancasegura.com.br/upload/{{5}}

Buttons:
- Quick Reply: "Vou enviar agora"
- Quick Reply: "Falar com consultor"
```
Samples: `{{1}}`=Carlos · `{{2}}`=contratação de Seguro Auto · `{{3}}`=COT-2026-0042 · `{{4}}`=CNH digitalizada (frente e verso) · `{{5}}`=carlos-silva-2042

---

## T7. `alianca_parcela_em_atraso_v1` (Utility)
**Gatilho:** parcela vencida sem pagamento.
```
Body:
Olá {{1}}! Identificamos que a parcela {{2}} da apólice {{3}} venceu em {{4}} e ainda não foi compensada (valor R$ {{5}}).
Para manter a cobertura ativa, o pagamento pode ser feito até {{6}} via:
• Boleto: {{7}}
• Pix: chave {{8}}

Buttons:
- URL: "2ª via do boleto" → https://aliancasegura.com.br/boleto/{{9}}
- Quick Reply: "Falar com financeiro"
```
Samples: `{{1}}`=Carlos · `{{2}}`=03/12 · `{{3}}`=APO-2026-0042 · `{{4}}`=15/06/2026 · `{{5}}`=248,00 · `{{6}}`=28/06/2026 · `{{7}}`=23793.38128 · `{{8}}`=financeiro@aliancasegura.com.br · `{{9}}`=apo-2026-0042-p3

---

## T8. `alianca_continuacao_pos_24h_v1` (Utility — uso defensivo)
**Gatilho:** conversa real ficou com pergunta pendente e passaram >24h.
```
Body:
Olá {{1}}! Sobre o {{2}} que conversamos no dia {{3}} (protocolo {{4}}), notei que sua resposta ficou em aberto.
Para seguir com a cotação, ainda preciso de: {{5}}
Quando você puder, me responde por aqui que eu sigo daí.

Buttons:
- Quick Reply: "Vou responder agora"
- Quick Reply: "Não tenho mais interesse"
```
Samples: `{{1}}`=Carlos · `{{2}}`=Seguro Auto · `{{3}}`=20/06/2026 · `{{4}}`=COT-2026-0042 · `{{5}}`=o ano do veículo
**Risco:** disparo em massa para leads frios → Meta reclassifica para Marketing. Usar **apenas**
quando houve conversa real e ficou pergunta pendente registrada.

---

## Variantes complementares (2º exemplo por gatilho)

Mesmos gatilhos dos T-templates, outra etapa do evento. Todas Utility-safe.

**Agendamento — `alianca_agendamento_confirmado_v1`** · gatilho: cliente acabou de escolher o horário.
```
Body:
Olá {{1}}! Seu retorno sobre {{2}} (protocolo {{3}}) ficou agendado para {{4}} às {{5}} com o consultor {{6}}.
Você vai receber um lembrete no dia. Para alterar, responda aqui.

Buttons: [Quick Reply] Está confirmado · [Quick Reply] Reagendar
```
Samples: `{{1}}`=Carlos · `{{2}}`=Seguro Auto · `{{3}}`=COT-2026-0042 · `{{4}}`=23/06/2026 · `{{5}}`=14h · `{{6}}`=Marina

**Renovação — versão que vira Marketing (❌ contraexemplo)** · mesmo gatilho do T4, redação errada:
```
Olá {{1}}! 🎉 Aproveite e renove sua apólice com 10% de desconto antecipado. Oferta por tempo limitado — garanta já!
```
Reprova: vocabulário promocional ("aproveite", "desconto", "oferta", "limitado", "garanta já") +
CTA persuasivo. A Meta reclassifica para Marketing automaticamente.

**Sinistro — `alianca_sinistro_vistoria_v1`** · gatilho: vistoria agendada no sinistro aberto.
```
Body:
Olá {{1}}! Sobre o sinistro {{2}} (apólice {{3}}): a vistoria foi agendada para {{4}} às {{5}}, no endereço {{6}}.
O vistoriador {{7}} é o responsável. Para reagendar, responda aqui.

Buttons: [Quick Reply] Confirmar vistoria · [Quick Reply] Reagendar · [URL] Detalhes → https://aliancasegura.com.br/sinistro/{{8}}
```
Samples: `{{1}}`=Carlos · `{{2}}`=SIN-2026-0117 · `{{3}}`=APO-2026-0042 · `{{4}}`=25/06/2026 · `{{5}}`=10h · `{{6}}`=Rua X, 123 · `{{7}}`=João · `{{8}}`=sin-2026-0117

**Documento — `alianca_doc_recebido_v1`** · gatilho: documento pendente foi recebido.
```
Body:
Olá {{1}}! Recebemos o documento {{2}} referente à sua {{3}} (protocolo {{4}}).
Está tudo certo e seguimos com a análise. Próximo retorno em até {{5}}.

Buttons: [URL] Acompanhar → https://aliancasegura.com.br/cliente/{{6}}
```
Samples: `{{1}}`=Carlos · `{{2}}`=CNH digitalizada · `{{3}}`=contratação de Seguro Auto · `{{4}}`=COT-2026-0042 · `{{5}}`=1 dia útil · `{{6}}`=carlos-silva-2042

**Parcela — `alianca_parcela_paga_v1`** · gatilho: pagamento da parcela compensado.
```
Body:
Olá {{1}}! Confirmamos o pagamento da parcela {{2}} da apólice {{3}}, no valor de R$ {{4}}, recebido em {{5}}.
Sua cobertura segue ativa. Próxima parcela: {{6}}.

Footer: Aliança Seguros & Consórcios
```
Samples: `{{1}}`=Carlos · `{{2}}`=03/12 · `{{3}}`=APO-2026-0042 · `{{4}}`=248,00 · `{{5}}`=27/06/2026 · `{{6}}`=15/07/2026

**Pós-24h — `alianca_continuacao_doc_pos24h_v1`** · gatilho: doc pendente não enviado, >24h.
```
Body:
Olá {{1}}! Sobre a sua {{2}} (protocolo {{3}}): ainda está pendente o documento {{4}} para a gente finalizar.
Pode enviar por aqui ou pelo portal: https://aliancasegura.com.br/upload/{{5}}

Buttons: [Quick Reply] Vou enviar agora · [Quick Reply] Falar com consultor
```
Samples: `{{1}}`=Carlos · `{{2}}`=contratação de Seguro Auto · `{{3}}`=COT-2026-0042 · `{{4}}`=CNH digitalizada · `{{5}}`=carlos-silva-2042

---

## O que NUNCA mandar como Utility (vira Marketing)
- ❌ "Olá! Você sabia que a Aliança tem seguro auto a partir de R$ 80/mês?" → cold outreach.
- ❌ "Aproveite nossa condição de Black Friday em seguros residenciais!" → promo pura.
- ❌ "Renove sua apólice com 5% de desconto antecipado!" → promo embutida.
- ❌ "Bom dia, {{1}}! 🎉 Como podemos te ajudar hoje?" → saudação genérica sem evento.
- ❌ "Sua cotação está pronta — e temos uma surpresa pra você 🎁" → mistura Utility + promo.
- ❌ "Feliz aniversário, {{1}}! Que tal aproveitar essa data com a gente?" → data comemorativa.
