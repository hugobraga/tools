# html2A4pdf

# Scripts para gerar pdf no formato A4 a partir do html gerado pelo Jira 

O objetivo destes scripts é possibilitar que, após imprimir um determinado card do Jira, o HTML gerado possa ser convertido em PDF que seja compatível com o formato A4, evitando que imagens e textos sejam cortados.

Existem dois arquivos, ambos contendo o mesmo código:

- **hyml2A4pdf.ipynb**: Jupyter notebook, cujo código foi escrito em python
- **hyml2A4pdf.py**: Script em python

Para ambos os scripts, assume-se que o html deve ser baixado antes de executar o script. Após imprimir o card no Jira, o usuário deve salvar localmente o html por meio do navegador sendo utilizado. 

Para ambos os scripts, alguns parâmetros devem ser configurados (no final do script):

- **RELATIVE_HTML_FILES_DIR**: o caminho relativo para a pasta contendo os arquivos de entrada (e saída).
- **HTML_FILE_NAME**: nome do arquivo html baixado.
- **OUTPUT_PDF_FILE_NAME**: nome do pdf gerado.
- **WKHTMLTOPDF_PATH**: caminho para o executável do [wkhtmltopdf](https://wkhtmltopdf.org/). Esta é uma ferramenta de linha de comando utilizada para renderizar html em PDF.