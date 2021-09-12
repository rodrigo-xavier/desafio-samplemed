# **Samplemed**
## **Como executar a aplicação**
### **Requisitos**

* Docker
* 

> **_NOTE:_**  Cuidado ao utilizar no Windows, o projeto ocupará muito espaço e também muita memória RAM.

### **Configurações**

Primeiro de tudo, altere o arquivo `.env` da forma como desejar. O indicado é que apenas se alterem as portas que serão abertas, de forma que não haja conflito com outras aplicações.

### **Execução**

> **_NOTE:_**  A primeira execução pode levar alguns minutos para preparar as aplicações, devido à ter que fazer download das imagens docker e criação de novos containers.

Para executar o projeto, basta utilizar o comando `docker-compose up`.
o comando fará os seguintes procedimentos:

* Criará dois bancos de dados, sendo um para o projeto e outro para testes;
* Conectará o banco de dados do projeto ao PHPMyadmin;
* Criará um container django a partir do Dockerfile especificado;
* Executará o entrypoint especificado no docker-compose.yml:
  * O entrypoint fará a coleta de arquivos estáticos;
  * Criará novas migrations;
  * Aplicará as migrations ao banco de dados;
  * Fará testes unitários se a variável `DEBUG` estiver definida com `True` no `.env`;
  * Iniciará o servidor web;


Para acessar a aplicação no navegador, basta acessar o HOST especificado no arquivo `.env`, seguido da porta de cada container. Ex:

192.168.0.175:8000

<!-- TODO: Explicar commo acessar o shell do container -->
> **_NOTE:_**  Se desejar criar um super usuário, é necessário acessar o shell do container django.

### **Testes**

Para executar os testes unitários de acordo com as configurações do arquivo `pytest.ini`, basta utilizar o comando `pytest`.

> **_NOTE:_**  Necessário acessar o shell do container do django.


### **Debug**

Se a variável `DEBUG` estiver definida como `True` no `.env`, a aplicação irá rodar em modo debug, e o desenvolvedor terá acesso ao menu do pacote debug_toolbar na aplicação.


### **API**

Todos os endpoints da aplicação estão disponíveis na rota `api/`.

#### Endpoints

| API | METHOD | ENDPOINTS |
| ------ | ------ |------ |
| List of articles | GET | /api/article/ |
| Article description | GET | /api/article/<id_category>/ |
| New Article | POST | /api/article/ |
| Change Article | PUT | /api/article/<id_category>/ |
| List of users | GET | /api/user/ |
| User description | GET | /api/user/<id_question>/ |
| New User | POST | /api/user/ |
| Change User | PUT | user/<id_category>/ |
| List of keywords | GET | /api/keyword/ |
| Keyword description | GET | /api/keyword/<id_question>/ |
| New Keyword | POST | /api/keyword/ |
| Change Keyword | PUT | /api/keyword/<id_question>/ |

#### Postman collection
[![Run in Postman](https://run.pstmn.io/button.svg)](https://app.getpostman.com/run-collection/17469376-7c639712-42ba-4cda-9c21-077aa9f5b1c9?action=collection%2Ffork&collection-url=entityId%3D17469376-7c639712-42ba-4cda-9c21-077aa9f5b1c9%26entityType%3Dcollection%26workspaceId%3D614b6ab9-829c-49df-b5bd-faa1de2b5cd4)

[![View Postman Documentation](https://run.pstmn.io/button.svg)](https://documenter.getpostman.com/view/17469376/U16kr5Mh)
## **Estruturação da aplicação**
### **samplemed**

É onde se encontram as configurações do projeto, como as variáveis de ambiente, as configurações de banco de dados, etc.

### **tests**

Onde ficam os testes unitários, o arquivo conftest define o banco de dados de teste

### **blog**

Onde estão definidos o modelos do blog.

### **blog/api**

Onde estão definidas as APIs, o serializer e o viewsets do blog.

### **decisions.txt**

Neste arquivo estão definidas as respostas para as tomadas de decisão e codificação do projeto

### **DBML.txt**

Onde estão as regras para geração de tabela de classes no formato DBML

Clique na imagem:
[![Open in dbdiagram.io](https://img.icons8.com/office/16/000000/database.png)](https://dbdiagram.io/d/613e3a49825b5b0146fe4519)

## **Pontos a Melhorar**

* Poderia ser implementado um sistema de permissões, onde um usuário de hierarquia mais alta faria review do artigo de outros usuários. Com isso, seria necessário implementar regras para alteração de status de cada artigo.
* Poderiam ter sido realizados mais testes unitários.
* Testes parecem não estar acessando banco de testes por algum motivo (por isso eu troquei o banco de testes para o de produção.).


#### ESTOU À DISPOSIÇÃO PARA ESCLARECER DÚVIDAS SOBRE O PROJETO
