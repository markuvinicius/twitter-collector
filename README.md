# Twitter Collector
#### Coletor personalizado de dados do Twitter

## Features
Oferece coleta de dados do Twitter e persiste-os em uma base de dados NoSQL Cassandra para análise.

- **Query Configurável:** Permite o uso de qualquer parâmetro ou # (hashtag) de busca para filtro de conteúdo <br>
- **Filtragem por Idioma:** Permite a filtragem de conteúdo por idioma. A lista de idiomas suportados pode ser consultada <a href=https://developer.twitter.com/en/docs/developer-utilities/supported-languages/api-reference/get-help-languages.html> aqui </a> <br>
- **Limite de resultados:** Permite o controle da quantidade de resultados retornados pelo Twitter (default=100)
- **Persistência de Dados:** Persiste o retorno da consulta para análise posterior.

## Set-Up
### Apache Cassandra
A execução desta aplicação pré-supõe que o Apache Cassandra já esteja instalado e operante em ambiente local ou remoto.
Para maiores informações sobre como realizar a instalação do cassandra, consulte <a href=http://cassandra.apache.org/doc/latest/getting_started/installing.html> aqui </a>

- **Criação dos keyspaces:** Para criar os keyspaces/tabelas necessárias para a execução do projeto, execute o script: <br> `$CASSANDRA_HOME/bin/cqlsh [HOSTS] -u USERNAME -p PASSWORD -f $APP_DIR/ddl.cql` <br>
`$CASSANDRA_DIR` é o diretório de instalação do cassandra <br>
`[HOSTS]` é uma lista de endereços para conexão no cluster <br>
`USERNAME` é o login de conexao <br>
`PASSWORD` é a senha de conexão <br>
`$APP_DIR` é o diretório do projeto `twitter-collector` 


### Python
Esta aplicação foi construída/testada utilizando a versão 2.7 do Python.<br>
<a href=https://www.python.org/download/releases/2.7/>Instalação Python 2.7 </a>

### PyPi
A execução desta aplicação requer a instalação de pacotes e bibliotecas específicas. Recomenda-se o uso do `virtualenv` para segregar um ambiente virtual para execução e o pacote `pip` para a instalação dos pacotes.<br>
Mais informações sobre a instalação do `virtualenv` estão aqui <a href=https://virtualenv.pypa.io/en/stable/installation/>aqui</a>

- **Instalação com `virtualenv`-** Execute os seguintes comandos no terminal:<br>
    - `virtualenv --python=Python2.7 $VENV_DIR/venv` <br>
    Este comando criará um novo ambiente virtual Python chamado **venv** no diretório **$VENV_DIR**
    - `source $VENV_DIR/venv/bin/activate` <br>
    Este comando apontará o bash para o arquivo activate do ambiente virtual e carregará as bibliotecas necessárias para o ambiente.
    - `pip install -r $APP_DIR/requirements.txt` <br>
    Este comando instalará todas as dependências necessárias para a execução do projeto
    
### Config.ini
Neste arquivo deverão ser configuradas as credenciais de acesso ao **Twitter** bem como as configurações de conexão com o **Cassandra**

## Execução
Para facilitar a execução do projeto, é fornecido um script shell na em `scripts/twitter_extraction.sh`.