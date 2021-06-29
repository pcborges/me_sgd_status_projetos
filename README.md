# Status Projetos SGD
Proposta de solução que visa automatizar a emissão de relatórios gerenciais sobre as startups do ME.
## Por onde começar
### Dependências
* Ter o python 3.9.x ou superior instalado
### Instalação
* Navegue até a pasta onde o projeto foi clonado e instale as dependências usando o comando abaixo:
```
pip install -r requirements.txt
```
* Crie arquivo com o nome 'google-credentials.json' na raiz do projeto, e adicione a chave de autenticação gerada pelo GoogleAuth com permissão ao BigQuery.

### Iniciando a aplicação
* Na raiz do projeto digite o comando
```
python app.py
```
* A aplicação será iniciada através do endereço: http://127.0.0.1:33507/

