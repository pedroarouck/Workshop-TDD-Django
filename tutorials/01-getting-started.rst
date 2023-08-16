Aquecendo os Motores
====================

Verificando Setup
------------------

Antes de começarmos, vamos apenas garantir que o Python e o Django estejam
instalados corretamente e sejam as versões apropriadas

A execução do seguinte comando no terminal Mac OS ou Linux ou no prompt de
comando do Windows deve mostrar a versão do Python. Para este workshop,
você deve ter uma versão 3.x do Python.

.. code-block:: bash

    $ python -V

Você também deve ter o `pip`_ instalado em sua máquina. Pip é uma ferramenta
de gerenciamento de dependência para instalar e gerenciar dependências do
Python. Primeiro vamos instalar o Django.

.. code-block:: bash

    $ pip install django
    Collecting django
      Downloading Django-4.2.4-py3-none-any.whl (8.0 MB)
       7.4MB downloaded
    Installing collected packages: django
    Successfully installed django-4.2.4

.. HINT::
   Coisas que você deve digitar em seu terminal ou prompt de comando sempre
   começarão com ``$`` neste workshop. No entanto, não digite o ``$`` inicial.

A execução do próximo comando mostrará a versão do Django que você instalou.
Você deve ter o Django 4.2 instalado

.. code-block:: bash

    $ python -m django --version
    4.2.4

Criando o Projeto
--------------------

A primeira etapa ao criar um novo site Django é criar os arquivos boilerplate
do projeto.

.. code-block:: bash

    $ django-admin startproject myblog
    $ cd myblog

Executar esse comando cria um novo diretório chamado ``myblog/`` com alguns
arquivos e pastas. Notavelmente, há um arquivo ``manage.py`` que é usado para
gerenciar vários aspectos do seu aplicativo Django, como criar o banco de dados
e executar o servidor web de desenvolvimento. Dois outros arquivos-chave que
acabamos de criar são ``myblog/settings.py``, que contém informações de configuração
para o aplicativo, como como se conectar ao banco de dados, e ``myblog/urls.py``,
que mapeia as URLs chamadas por um navegador da Web para o código Python apropriado.

Configurando o Banco de Dados
-----------------------------

Uma arquitetura em comum de praticamente todos os sites que contêm conteúdo
gerado pelo usuário é um banco de dados. Bancos de dados facilitam uma boa
separação entre código (Python e Django neste caso), marcação e scripts
(HTML, CSS e JavaScript) e conteúdo real (banco de dados). Django e outras
frameworks ajudam a orientar os desenvolvedores a como separar cada porção
da aplicação.

Primeiro, vamos criar o banco de dados e uma conta de superusuário para acessar a
interface de administração que veremos em breve:

.. code-block:: bash

    $ python manage.py migrate
    Operations to perform:
      Apply all migrations: admin, contenttypes, auth, sessions
    Running migrations:
      ...
    $ python manage.py createsuperuser
    Username (leave blank to use 'pedro'):
    Email address:
    Password: ***
    Password (again): ***
    Superuser created successfully.

Depois de executar este comando, haverá um arquivo de banco de dados
``db.sqlite3`` no mesmo diretório que ``manage.py``. No momento, este banco
de dados possui apenas algumas tabelas específicas para Django. O comando
examina ``INSTALLED_APPS`` em ``myblog/settings.py`` e cria tabelas de banco de
dados para modelos definidos nos arquivos ``models.py`` desses aplicativos.

Mais adiante neste workshop, criaremos modelos específicos para o blog que
estamos escrevendo. Esses modelos manterão dados como entradas de blog e
comentários em entradas de blog.


.. HINT::
    SQLite é um mecanismo de banco de dados independente. É inadequado para um site
    multiusuário, mas funciona muito bem para o desenvolvimento. Em produção,
    você provavelmente usaria PostgreSQL ou MySQL. Para obter mais informações sobre
    o SQLite, consulte a `documentação do SQLite`_.

    .. _documentação do SQLite: https://sqlite.org/index.html


A Interface de Administração
----------------------------
Um dos melhores recursos que o Django fornece é uma interface administrativa.
Uma interface de administração é uma maneira de um administrador de um site
interagir com o banco de dados por meio de uma interface da web que os visitantes
regulares do site não têm permissão para usar. Em um blog, este seria o lugar
onde o autor escreve novas entradas de blog.

Vamos verificar nosso progresso executando o servidor de teste Django e
visitando a interface de administração.

Em seu terminal, execute o servidor de desenvolvimento Django:

.. code-block:: bash

    $ python manage.py runserver

Agora visite a interface de administração em seu navegador (http://localhost:8000/admin/).


.. HINT::
    O servidor de desenvolvimento Django é um servidor web simples usado para
    desenvolvimento rápido e não para uso em produção de longo prazo. O
    servidor de desenvolvimento é recarregado sempre que o código é alterado,
    mas algumas ações, como adicionar arquivos, não acionam uma recarga e o
    servidor precisará ser reiniciado manualmente.

    Leia mais sobre o servidor de desenvolvimento na `documentação oficial`_.

    Saia do servidor segurando a tecla ctrl e pressionando C


Arquivo de requisitos do pacote Python
--------------------------------------

Queremos usar mais alguns pacotes Python além do Django. Planejaremos usar o
`WebTest`_ e o `django-webtest`_ para nossos testes funcionais. Vamos instalá-los também:

.. code-block:: bash

    $ pip install webtest django-webtest
    Collecting webtest
      Downloading WebTest-2.0.16.zip (88kB): 88kB downloaded
        ...
    Collecting django-webtest
      Downloading django-webtest-1.7.7.tar.gz
        ...
    Successfully installed WebOb-1.8.7 beautifulsoup4-4.12.2 django-webtest-1.9.10 waitress-2.1.2 webtest-3.0.0

Não queremos instalar manualmente nossas dependências todas as vezes. Vamos criar
um `arquivo de requisitos`_ listando nossas dependências para que não tenhamos que digitá-los
toda vez que configurarmos nosso site em um novo computador ou sempre que uma versão do pacote
for atualizada.

Primeiro vamos usar o `pip freeze`_ para listar nossas dependências e suas versões:

.. code-block:: bash

    $ pip freeze
    Django==4.2.4
    WebOb==1.8.7
    WebTest==3.0.0
    beautifulsoup4==4.12.2
    django-webtest==1.9.10
    six==1.16.0
    waitress==2.1.2

Nós nos preocupamos com as linhas ``Django``, ``WebTest`` e ``django-webtest`` que apareceram.
Os demais pacotes são subdependências que foram instaladas automaticamente e não precisa se preocupar com eles.
Vamos criar nosso arquivo  ``requirements.txt`` com instruções para instalar esses pacotes com as versões que instalamos agora:

    Django==4.2.4
    WebTest==3.0.0
    django-webtest==1.9.10

Este arquivo nos permitirá instalar todas as dependências do Python de uma só vez com apenas um comando.
Sempre que nossos arquivos de dependência forem atualizados ou se configurarmos um novo ambiente de
desenvolvimento para nosso site Django, basta executar:

.. code-block:: bash

    $ pip install -r requirements.txt

.. NOTE::
    Observe que não precisamos digitar este comando agora, pois já instalamos todas as dependências.


.. _documentação oficial: https://test-driven-django-development.readthedocs.io/en/latest/01-getting-started.html
.. _WebTest: https://docs.pylonsproject.org/projects/webtest/en/latest/
.. _django-webtest: https://pypi.org/project/django-webtest/
.. _pip: https://pip.pypa.io/en/stable/installation/
.. _pip freeze: https://pip.pypa.io/en/latest/cli/pip_freeze/
.. _arquivo de requisitos: https://pip.pypa.io/en/latest/user_guide/#requirements-files
