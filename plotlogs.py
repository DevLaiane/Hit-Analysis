import os
import csv
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

CSV_FOLDER_PATH = '/home/laiane/Documentos/optLogs(1)/optLogs/opt-logs-4bits/output/optall/'
OUTPUT_PDF_PATH = '/home/laiane/Documentos/optLogs(1)/optLogs/opt-logs-4bits/output/logs.pdf' 

QPS = ['LD 22', 'LD 27', 'LD 32', 'LD 37', 'RA 22', 'RA 27', 'RA 32', 'RA 37']

def ajustar_tamanho_fontes(bar, ax, fontsize=5):
    # ajusta o tamanho da fonte das porcentagens nas barras
    for b in bar:
        yval = b.get_height()
        ax.text(b.get_x() + b.get_width()/2, yval, f'{yval:.1f}%', ha='center', va='bottom', fontsize=fontsize, color='black')

def processa_arquivos():
    dados_videos = {}

    # percorre todos os arquivos csv
    for arquivo in sorted(os.listdir(CSV_FOLDER_PATH)):
        if arquivo.endswith('.csv'):
            partes_nome = arquivo.split('_')
            
            # verifica se o nome do arquivo tem 4 partes separadas por "_" pra não dar problema na leitura
            if len(partes_nome) < 4:
                print(f"[AVISO] Nome de arquivo inesperado: {arquivo}")
                continue
            
            video_nome = partes_nome[1]  # Nome do vídeo
            # extrai o QP e remove possíveis caracteres adicionais
            qp_nome = partes_nome[2]
            if len(partes_nome) > 3:
                qp_nome += ' ' + partes_nome[3].split('.')[0]
            qp_nome = qp_nome.split(' ')[0] + ' ' + qp_nome.split(' ')[1]  # Apenas 'LD 22' ou 'RA 22'
            
            caminho_arquivo = os.path.join(CSV_FOLDER_PATH, arquivo)
            
            # lê o CSV e extrai os valores
            with open(caminho_arquivo, 'r', newline='') as csvfile:
                reader = csv.reader(csvfile, delimiter=';')
                next(reader)  
                
                for linha in reader:
                    if len(linha) < 2:  # verifica se tem as duas colunas de pref-frac-hit e adj-mvs-pctg
                        print(f"[AVISO] Linha ignorada em {arquivo} devido a dados insuficientes: {linha}")
                        continue
                    
                    try:
                        # converte para porcentagem
                        pref_frac_hit = float(linha[0]) * 100  # primeira coluna (pref-frac-hit)
                        adj_mvs_pctg = float(linha[1]) * 100  # segunda coluna (adj-mvs-pctg)
                    except ValueError:
                        print(f"[AVISO] Linha ignorada em {arquivo} devido a valores inválidos: {linha}")
                        continue
                    
                    if video_nome not in dados_videos:
                        dados_videos[video_nome] = {qp: (0, 0) for qp in QPS}  # inicializa todos os QPs com (0, 0)
                    
                    if qp_nome in QPS:
                        dados_videos[video_nome][qp_nome] = (adj_mvs_pctg, pref_frac_hit)
                    else:
                        print(f"QP inesperado '{qp_nome}' no arquivo '{arquivo}'")
    
    return dados_videos

def plota_graficos(dados_videos, fontsize=8, title_fontsize=10, label_fontsize=8, legend_fontsize=8):
    with PdfPages(OUTPUT_PDF_PATH) as pdf:
        for video_nome, qps in dados_videos.items():
            print(f"Plotando gráfico do vídeo {video_nome}")
            
            # garante que todos os QPs tenham valores
            adj_mvs_pctgs = [qps.get(qp, (0, 0))[0] for qp in QPS]
            pref_frac_hits = [qps.get(qp, (0, 0))[1] for qp in QPS]
            
            # Verifica se todos os valores são zero
            if all(adj == 0 and pref == 0 for adj, pref in zip(adj_mvs_pctgs, pref_frac_hits)):
                print(f"[AVISO] Gráfico do vídeo {video_nome} ignorado por falta de dados válidos.")
                continue  # Pula este vídeo se não houver dados válidos
            
            fig, ax = plt.subplots(figsize=(10, 6))
            
            bar_width = 0.35
            index = range(len(QPS))
            
            # adiciona as barras para pref-frac-hit e adj-mvs-pctg (invertida a ordem)
            bars1 = ax.bar(index, pref_frac_hits, bar_width, label='pref-frac-hit', color='blue')
            bars2 = ax.bar([i + bar_width for i in index], adj_mvs_pctgs, bar_width, label='adj-mvs-pctg', color='orange')
            
            ax.set_xlabel('Low Delay Random Acc.', fontsize=label_fontsize)
            ax.set_ylabel('Hit ratio (%)', fontsize=label_fontsize)
            ax.set_title(f'{video_nome}', fontsize=title_fontsize)
            ax.set_xticks([i + bar_width / 2 for i in index])
            ax.set_xticklabels(QPS, fontsize=label_fontsize)
            ax.set_ylim(0, 100)
            ax.legend(fontsize=legend_fontsize)

            ajustar_tamanho_fontes(bars1, ax, fontsize)
            ajustar_tamanho_fontes(bars2, ax, fontsize)
            
            pdf.savefig(fig)
            plt.close(fig)

if __name__ == '__main__':
    dados_videos = processa_arquivos()
    
    # verifica se tá certo antes de plotar
    print(f"Dados processados: {dados_videos}")
    
    plota_graficos(dados_videos, fontsize=8, title_fontsize=10, label_fontsize=8, legend_fontsize=8)
