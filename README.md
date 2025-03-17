# SescConsultaGMF

Este projeto automatiza a consulta de inscrições abertas para atividades de Ginástica Multifuncional no Sesc SP e envia notificações para um canal do Discord.

## Descrição

O script `SescConsultaGMF.py` utiliza Selenium WebDriver para automatizar o processo de login no site do Sesc SP, pesquisa por atividades de Ginástica Multifuncional e verifica se há inscrições abertas nas unidades selecionadas. Caso encontre inscrições abertas, o script envia uma mensagem para um webhook do Discord configurado.

## Requisitos

- Python 3.x
- Selenium
- Requests
- Geckodriver (para Firefox)

## Instalação

1. Clone o repositório:
    ```sh
    git clone https://github.com/seu-usuario/SescConsultaGMF.git
    cd SescConsultaGMF
    ```

2. Crie um ambiente virtual e ative-o:
    ```sh
    python -m venv .venv
    .venv\Scripts\activate  # No Windows
    source .venv/bin/activate  # No Linux/Mac
    ```

3. Instale as dependências:
    ```sh
    pip install -r requirements.txt
    ```

4. Configure o arquivo [config.ini](http://_vscodecontentref_/0) com suas informações:
    ```ini
    [DEFAULT]
    DISCORD_WEBHOOK_URL = https://discord.com/api/webhooks/your_webhook_url
    FIREFOX_BINARY_LOCATION = C:\Path\To\firefox.exe
    GECKODRIVER_LOCATION = C:\Path\To\geckodriver.exe
    USERNAME = seu_usuario
    PASSWORD = sua_senha
    PUBLICO_GERAL = True
    UNIDADES_SELECIONADAS = 24 de Maio, Av. Paulista, Belenzinho, Bom Retiro, Carmo, Consolação, Guarulhos, Ipiranga, Pinheiros, Pompeia, Santana, Santo Amaro, Vila Mariana
    ```

## Uso

Execute o script [SescConsultaGMF.py](http://_vscodecontentref_/1):
```sh
python SescConsultaGMF.py