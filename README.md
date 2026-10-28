# Análise de Logs de Otimização de Codificação de Vídeo

Este repositório contém um script em Python desenvolvido para processar arquivos de log (`.csv`) gerados por um otimizador de codificação de vídeo. O script extrai métricas de acertos (hit ratios) e gera gráficos comparativos em formato PDF para análise de desempenho das predições.

## Sobre o Projeto

O objetivo principal é avaliar o comportamento de predição de vetores de movimento através de duas métricas principais extraídas dos logs:
*   **`pref-frac-hit`**: Fração de acertos preferenciais.
*   **`adj-mvs-pctg`**: Porcentagem de vetores de movimento adjacentes.

O script agrupa esses dados por vídeo e por configuração de QP (Quantization Parameter), gerando gráficos de barras para facilitar a visualização e comparação entre as configurações **Low Delay (LD)** e **Random Access (RA)**.

## Estrutura dos Dados

O script espera que os arquivos CSV estejam em uma pasta específica e sigam uma convenção de nomenclatura padrão.

*   **Nomenclatura do arquivo:** `[prefixo]_[nome_do_video]_[configuracao]_[QP].csv`
    *   *Exemplo:* `log_BQMall_LD_22.csv`
*   **Formato do CSV:** Delimitado por ponto e vírgula (`;`).
    *   *Coluna 1:* `pref-frac-hit`
    *   *Coluna 2:* `adj-mvs-pctg`

## Funcionalidades

*   **Leitura e Parsing:** Varre a pasta de logs, extrai o nome do vídeo e o QP a partir do nome do arquivo e lê as métricas do CSV.
*   **Conversão de Dados:** Converte os valores decimais em porcentagens (0 a 100%).
*   **Geração de Gráficos:** Cria gráficos de barras agrupadas (barras azuis para `pref-frac-hit` e laranjas para `adj-mvs-pctg`).
*   **Exportação em Lote:** Salva todos os gráficos gerados em um único arquivo PDF (`logs.pdf`) para facilitar a visualização e o compartilhamento.
*   **Tratamento de Exceções:** Ignora linhas mal formatadas ou arquivos com nomes fora do padrão, exibindo avisos no console.

## Como Usar

### Pré-requisitos
Certifique-se de ter o Python 3 instalado e a biblioteca `matplotlib`:

```bash
pip install matplotlib
