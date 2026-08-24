# ONS Data: Dados Abertos do Sistema Elétrico Brasileiro

### O que é ONS?
O Operador Nacional do Sistema Elétrico (ONS) — a entidade que coordena a operação da geração e transmissão de energia elétrica no Brasil — mantém um portal de dados abertos (lançado em 2021) com séries históricas do setor elétrico nacional, em CSV, de acesso livre.

Dentro deste pequena análise, foram selecionados conjuntos específicos dentro do portfólio do ONS:

- **Balanço de Energia por Subsistema**: Informações da carga e oferta de energia verificados em periodicidade horária por subsistema. A oferta é representada pelos valores de geração das usinas hidráulicas, térmicas, eólicas e fotovoltaicas, em MWmed.

- **Carga de Energia diária**: Dados de carga por subsistema em base diária, medida em MWmed.

- **Intercâmbio de energia entre Subsistemas**:Dados de intercâmbio entre subsistemas em base horária, em MWmed. As grandezas representam a soma das medidas de fluxo de potência ativa nas linhas de transmissão de fronteira entre os subsistemas.

- **CMO Semanal**: Valores do custo, por unidade de energia produzida, para atender ao incremento de uma unidade de carga no SIN, chamado de Custo Marginal de Operação – CMO. Valores para cada semana operativa por subsistema, e por patamar de carga, além da média semanal, estimados pelo modelo Decomp.

- **ENA diário por Subsistema**: Dados das grandezas de energia natural afluente (ENA) dos reservatórios com periodicidade diária por Subsistemas.

A Energia Natural Afluente (ENA) Bruta representa a energia produzível pela usina e é calculada pelo produto das vazões naturais aos reservatórios com as produtividades a 65% dos volumes úteis. A ENA Armazenável considera as vazões naturais descontadas das vazões vertidas nos reservatórios.

- **EAR diário por Subsistema**: Dados das grandezas de energia armazenada (EAR) em periodicidade diária por Subsistemas.

A Energia Armazenada (EAR) representa a energia associada ao volume de água disponível nos reservatórios que pode ser convertido em geração na própria usina e em todas as usinas à jusante na cascata. A grandeza de EAR leva em conta nível verificado nos reservatórios na data de referência. A grandeza de EAR máxima representa a capacidade de armazenamento caso todos os reservatórios do sistema estivessem cheios. A grandeza de EAR para o subsistema à jusante considera a utilização da água do reservatório para produzir energia em uma usina à jusante que está em um subsistema diferente.
