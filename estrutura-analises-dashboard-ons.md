# Estrutura Conceitual — Análises e Dashboard (Projeto ONS)

Como interpretar cada bloco de query, como organizar isso num dashboard Streamlit, e qual visualização usar em cada caso. Sem código de app aqui — é o design antes de construir.

---

## Parte 1 — Como interpretar e comunicar cada bloco de análise

A ideia central: ninguém lê 8 queries soltas. Você agrupa em 3 blocos, e pra cada bloco escreve **uma frase de achado** (com número real, depois de rodar) — isso é o que vira texto no README e legenda no dashboard.

### Bloco 1 — Perfil de Consumo (queries 1, 3, 4)

**O que essas três respondem juntas:** o tamanho e o comportamento da demanda de energia em cada região do país.

**O que procurar ao olhar o resultado:**
- Query 1 mostra o "tamanho" de cada subsistema — normalmente Sudeste/Centro-Oeste puxa a frente por concentrar mais população e indústria. Se isso não aparecer no seu resultado, vale investigar antes de seguir (pode ser sinal de erro na carga do dado).
- Query 3 mostra se a diferença entre dia útil e fim de semana é grande ou pequena — isso indica o quanto o consumo daquele subsistema é "industrial" (cai mais no fim de semana) ou "residencial/serviços" (cai menos).
- Query 4 mostra sazonalidade ao longo do ano — picos em períodos mais quentes (mais uso de ar-condicionado) costumam aparecer com clareza no Sudeste e Nordeste.

**Template do achado a escrever:** "O subsistema [X] apresenta a maior carga média do período ([valor] MWmed), [Y]% acima da carga em dias úteis comparado a fins de semana, com pico sazonal em [mês]."

### Bloco 2 — Matriz de Geração (queries 5, 7)

**O que essas duas respondem juntas:** de onde vem a energia em cada região, e o quanto essa composição varia ao longo do tempo.

**O que procurar:**
- Query 5 mostra a "assinatura energética" de cada subsistema — Sul e Nordeste tendem a ter mais eólica, Sudeste/Centro-Oeste mais hidráulica e térmica.
- Query 7 mostra a **intermitência** da eólica — a diferença entre o mês de maior e menor participação eólica é, sozinha, um dado interessante: quanto maior o intervalo, mais essa fonte varia (e mais o sistema depende de outras fontes pra compensar quando o vento cai).

**Template do achado:** "No subsistema [X], a fonte predominante é [fonte] ([Z]% em média). A participação eólica varia de [mínimo]% em [mês] a [máximo]% em [mês], evidenciando a intermitência da fonte."

### Bloco 3 — Qualidade do Dado (queries 6, 8) — o achado principal

**Por que esse bloco é o mais importante do projeto inteiro:** ele não descreve o setor elétrico, ele testa a confiabilidade da própria base de dados — que é exatamente a responsabilidade central listada na vaga.

**O que procurar:**
- Query 6 é um teste binário: existe ou não existe carga sem geração registrada. Mesmo zero ocorrências é um resultado válido e deve ser reportado ("nenhuma inconsistência desse tipo foi encontrada no período").
- Query 8 é um teste de magnitude: quantos dias, e quão grande é a divergência. Aqui o número importa mais que a existência — "3 dias com divergência" é uma nota de rodapé, "40% dos dias com divergência acima de 5%" é uma manchete.

**Template do achado:** "Em [N]% dos dias do período analisado, a soma das leituras horárias diverge em mais de 5% da carga diária consolidada — indicando [inconsistência de metodologia entre as duas bases / necessidade de tratamento adicional antes de qualquer análise que combine as duas fontes]."

Esse bloco deveria abrir o dashboard e o README, não fechar — é o diferencial do projeto.

---

## Parte 2 — Estrutura do dashboard Streamlit

### Organização geral da tela

```
┌─────────────────────────────────────────────┐
│  Cabeçalho: título + contexto do dataset     │
├─────────────────────────────────────────────┤
│  Linha de métricas-resumo (KPIs)             │
│  [Carga média nacional] [Subsistema líder]   │
│  [% dias com divergência de qualidade]       │
├─────────────────────────────────────────────┤
│  Abas: Consumo | Geração | Qualidade do Dado │
│  (conteúdo de cada bloco dentro da sua aba)  │
├─────────────────────────────────────────────┤
│  Rodapé: fonte dos dados, metodologia, link  │
└─────────────────────────────────────────────┘
```

**Por que KPIs no topo antes das abas:** quem abre o dashboard (recrutador, você numa entrevista) decide em 5 segundos se vale a pena explorar. O card de "% dias com divergência" ali em cima já entrega o achado mais forte sem precisar clicar em nada.

**Por que abas (`st.tabs`) e não tudo na mesma tela:** os três blocos respondem perguntas diferentes — misturar tudo numa rolagem única deixa o dashboard poluído e sem hierarquia. Abas deixam a navegação intencional: a pessoa escolhe qual pergunta quer investigar.

**Filtro global na barra lateral:** um seletor de subsistema (com opção "todos") e um seletor de intervalo de datas, aplicados a todas as abas — evita repetir o mesmo filtro dentro de cada aba.

### Conteúdo sugerido por aba

- **Aba "Consumo":** gráfico de barras (query 1) + gráfico de barras agrupadas (query 3) lado a lado ou empilhados verticalmente, seguido do gráfico de linha mensal (query 4) ocupando a largura toda.
- **Aba "Geração":** gráfico de barras empilhadas (query 5) e, abaixo, o gráfico de linha da participação eólica mensal (query 7) com os pontos de máximo/mínimo destacados.
- **Aba "Qualidade do Dado":** o card de destaque com o número principal, seguido da tabela de casos (query 6) e do gráfico de dispersão com os pontos de divergência (query 8).

---

## Parte 3 — Qual visualização usar em cada query

| Query | O que compara | Visualização recomendada | Por quê |
|---|---|---|---|
| 1 — Carga média por subsistema | Categorias (4 subsistemas) | Barras horizontais, ordenadas do maior pro menor | Comparação categórica simples; ordenar facilita leitura imediata do ranking |
| 2 — Data de pico por subsistema | Um registro por subsistema | Tabela ou `st.metric` (cards) | Não é uma série, é um "recorde pontual" — gráfico seria exagero |
| 3 — Dia útil x fim de semana | Duas séries por subsistema | Barras agrupadas (grouped bar) | Permite comparar as duas categorias lado a lado dentro de cada subsistema |
| 4 — Carga média mensal | Evolução no tempo, por subsistema | Linha, uma cor por subsistema | Série temporal — linha é sempre a escolha certa para "como isso muda mês a mês" |
| 5 — % de cada fonte por subsistema | Composição (partes de um todo), por subsistema | Barras empilhadas 100% | Evite pizza aqui — comparar 4 pizzas lado a lado é mais difícil de ler que barras empilhadas |
| 6 — Inconsistência geração zero | Existência/contagem de casos | `st.metric` (contagem) + tabela dos casos | É uma checagem binária/lista, não uma tendência — não force um gráfico |
| 7 — Mês de maior/menor eólica | Extremos dentro de uma série temporal | Linha mensal com marcadores destacados nos pontos de máximo/mínimo | Mostra o contexto (a série toda) e ainda assim destaca o achado específico |
| 8 — Divergência carga diária x soma horária | Relação entre dois valores que deveriam ser iguais | Dispersão (scatter), com linha de referência diagonal (y = x) | Pontos fora da diagonal são visualmente óbvios como divergência — mais direto que uma tabela de diferenças |

### Princípios gerais de apresentação

- **Cor consistente por subsistema em todos os gráficos** (ex: Sudeste sempre azul, Sul sempre verde) — sem isso, cada gráfico exige que quem olha reaprenda a legenda.
- **Reserve uma cor de alerta (vermelho/laranja) exclusivamente para os achados de qualidade de dado** — separa visualmente "isso é uma característica do sistema elétrico" de "isso é um problema na base".
- **Evite pizza/donut com mais de 3-4 fatias** — vira ilegível; barras empilhadas resolvem o mesmo problema com mais clareza.
- **Sempre rotule a unidade nos eixos** (MWmed, %, data) — um gráfico sem unidade obriga quem olha a adivinhar.
- **Ordene por valor, não por ordem alfabética**, em qualquer comparação categórica (query 1, por exemplo) — leitura fica imediata.

---
Datasets relevantes além dos que você já usa (carga/balanço):

- EAR Diário por Subsistema — energia armazenada nos reservatórios (%)
- ENA Diário por Subsistema — energia natural afluente (chuva/vazão convertida em energia)
- Intercâmbios Entre Subsistemas — fluxo de energia entre regiões
- CMO Semanal / CMO Semi-Horário — preço da energia (Custo Marginal de Operação)
- Interrupção de Carga — eventos reais de desligamento forçado, com causa
- Restrição de Operação por Constrained-off de Usinas Eólicas/Fotovoltaicas — energia "perdida" por restrição da rede
- Geração por Usina em Base Horária — granularidade por usina, não só por subsistema

Algumas ideias de análise que aproveitam ISSO.

| # | O que faria | Datasets | Por que é melhor que a antiga |
| --- | --- | --- | --- |
| <input type="checkbox"> | A	| Correlação entre ENA (chuva) e nível do reservatório (EAR) por subsistema ao longo do tempo | ENA + EAR diário |	Conta uma história real (seca/cheia afetando o sistema), não só uma checagem de qualidade de dado |
| <input type="checkbox"> | B	| Quais subsistemas mais "exportam" e mais "importam" energia via intercâmbio, e como isso mudou entre 2023-2025 | Intercâmbios Entre Subsistemas | Mostra a interdependência real do SIN — coisa que ninguém espera de um portfólio básico |
| <input type="checkbox"> | C	| Volatilidade do CMO (preço) por subsistema — quando e onde a energia ficou mais cara, cruzando com nível baixo de reservatório | 	CMO Semanal + EAR | Liga preço a causa física, mostra raciocínio de negócio, não só SQL |
| <input type="checkbox"> | D	| Curtailment eólico/solar: quanta energia deixou de ser gerada por restrição da rede, por subsistema e por ano | Constrained-off Eólica/Fotovoltaica | Tema atual (crescimento de renováveis no Brasil) , gráfico de tendência crescente é visualmente forte | 
| <input type="checkbox"> | E	| Causas mais comuns de interrupção de carga por subsistema/ano — isso sim captura os "eventos naturais" que você mencionou (enchente, vendaval etc.) | Interrupção de Carga | Substitui diretamente a ideia da query 8 (achar "divergência") por algo que de fato existe no dado: causas reais catalogadas | 