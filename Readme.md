# Gerenciador de Agendas

Um serviço WEB para gerenciar agendas e eventos.

#### Requisitos funcionais
1. Criar e visualizar agendas.
2. Ativar ou desativar uma agenda.
3. Criar, visualizar e excluir eventos.
4. Realizar inscrições em eventos.


#### Requisitos não funcionais
1. Ter instalado o interpretador python3
2. Ter instalado os módulos python especificados em 'requirements.txt'
3. Ser possível a criação do socket TCP com IP localhost e porta 5000
4. Ter criado um schema mysql 'mydb' com os dados contidos em 'mydb.sql'

#### Regras de negócio
1. Um evento deve começar e acabar na mesma data.
2. Somente o usuário autenticado pode configurar suas agendas ou eventos.
3. Um nome não pode estar inscrito em mais de um evento da mesma agenda.
4. Não deve ser possível criar eventos em datas passadas.
5. Só deve ser possível a visualização de agendas ativas de outros usuários.
6. As senhas do usuários devem ser guardadas no banco de dados criptografadas.

#### Preparando ambiente com virtualenv

```shell
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
#### Execução do programa
1. Preparar o ambiente atendendo os requisitos não funcionais.
2. Ir para o diretório raiz do projeto.
3. Executar o arquivo 'app.py' passando o usuário e senha do mysql com acesso ao schema mydb. Ex:
```shell
python3 app.py usuario senha
```
