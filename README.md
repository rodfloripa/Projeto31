# Projeto31
Avaliando RAG com Ragas

<p align="justify">Neste projeto a RAG do Projeto30 foi avaliada com Ragas</p>
<p align="justify">O arquivo dataset.json contém perguntas sobre o documento com as respostas que devem ser dadas.</p>
<p align="justify">Ragas cria o arquivo de saida re.csv com perguntas e métricas.</p>

# Melhorias na RAG

<p align="justify">1. Aumento do top_k (Janela de busca)</p>
<p align="justify">No código anterior, o sistema buscava apenas os 3 pedaços de texto mais similares. Se a resposta sobre o decorador @step estivesse no quarto ou quinto parágrafo mais relevante, ela era descartada antes mesmo de chegar à IA. A correção: Alteramos para top_k=5, aumentando a rede de captura de informações do PDF.</p>

---

<p align="justify">2. Implementação de Overlap (Sobreposição de texto)</p>
<p align="justify">Antes, o texto era cortado de forma seca a cada 1000 caracteres. Isso poderia "serrar" o termo @step ao meio (ex: @st em um bloco e ep no outro), impedindo que a busca semântica o encontrasse. A correção: Introduzimos um overlap de 200 caracteres. Agora, o final de um bloco se repete no início do próximo, garantindo que termos técnicos fiquem íntegros em pelo menos um dos pedaços.</p>

---

<p align="justify">3. Correção do Campo de Contextos (Entrega ao Ragas)</p>
<p align="justify">O motivo do  log mostrar Context not provided by API era uma falha de comunicação. A API respondia a pergunta, mas não estava devolvendo a lista de trechos do PDF usados na resposta. A correção: No novo app.py, garantimos que o JSON de resposta contenha a chave 'contextos': retrieved_contexts. Sem esses textos, o Ragas não tem como comparar a resposta da IA com o PDF, resultando matematicamente em Recall 0.</p>

---

<p align="justify">4. Ajuste de Temperatura e Prompt</p>
<p align="justify">A IA estava "alucinando" (inventando @pipeline para uma pergunta sobre tarefas) porque o prompt era muito permissivo. A correção: Reduzimos a temperature para 0.1 (tornando a IA mais literal e menos criativa) e adicionamos uma instrução rígida: "Se a resposta não estiver no contexto, diga que não encontrou".</p>

---

# Resultados

<p align="justify">Aqui está a tabela completa com todas as métricas calculadas para as  20 perguntas, extraídas diretamente dos resultados do  processo de avaliação com Ragas.</p>

![Tab1. Resultados](URL_da_imagem)

<p align="justify">Note que o sistema de busca está excelente (Recall 1.0), mas o desafio atual é a Fidelidade (Faithfulness) em algumas questões técnicas onde a IA se confundiu.</p>

---

### O que esses números nos ensinam?

<p align="justify"> Context Recall (1.0 constante): O  banco de dados vetorial (Redis + Embeddings) está perfeito. Ele sempre encontra a página certa do PDF.</p>

<p align="justify"> Faithfulness (O gargalo): Onde você vê 0.0 ou 0.33 (como nas questões 6, 7 e 9), significa que a IA tinha a informação no contexto, mas "alucinou" ou ignorou partes do texto.</p>

<p align="justify"> Answer Relevancy (Sempre alto): Isso mostra que a IA é "boa de papo". Mesmo quando ela erra o conteúdo técnico, ela escreve uma resposta que parece fazer sentido e está no formato correto.</p>

---

### Resumo Estatístico da sua RAG:

<p align="justify"> Capacidade de Recuperação: 100% (Recall 1.0)</p>
<p align="justify"> Precisão da Resposta: ~78% (Média de Faithfulness)</p>

---





