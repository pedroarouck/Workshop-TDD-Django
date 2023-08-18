Database Migrations
===================

Se você tiver um banco de dados, deverá usar `migrações`_ para gerenciar
alterações no esquema do banco de dados

Vamos aprender sobre migrações para preparar nosso site para o futuro
contra alterações no banco de dados.

Fazendo Migrations
-------------------

Criamos nosso projeto usando migrações, então vamos ver as migrações
que já temos.

No momento, temos apenas um aplicativo chamado ``blog``. Podemos encontrar
as migrações no pacote ``migrations`` desse aplicativo:

.. code-block:: bash

    migrations
    ├── 0001_initial.py
    ├── 0002_alter_entry_options_comment.py
    └── __init__.py

Agora vamos ver as migrações que temos até agora

.. code-block:: bash

    $ python manage.py showmigrations
    admin
     [X] 0001_initial
    auth
     [X] 0001_initial
    blog
     [X] 0001_initial
     [X] 0002_alter_entry_options_comment
    contenttypes
     [X] 0001_initial
    sessions
     [X] 0001_initial

Como as migrações são um recurso do próprio Django, cada aplicativo
reutilizável distribuído com o Django também contém migrações e
permitirá que você atualize automaticamente seu esquema de banco
de dados quando seus modelos mudarem.

Cada um desses arquivos de migração armazena instruções sobre
como alterar corretamente o banco de dados a cada alteração.

Usando Migrate
--------------

Sempre que fizermos uma alteração em nossos modelos que exija uma alteração
em nosso banco de dados (por exemplo, adicionar um modelo, adicionar um campo,
remover um campo etc.), precisamos criar um arquivo de migração de esquema para nossa alteração.

Para fazer isso, usaremos o comando ``makemigrations``. Vamos experimentar agora:

.. code-block:: bash

    $ python manage.py makemigrations blog
    No changes detected in app 'blog'

Nenhuma migração foi criada porque não fizemos nenhuma alteração em nossos modelos.

.. TIP::

    Para mais informações confira `migrações`_ na documentação do Django.

.. _migrações: https://docs.djangoproject.com/en/4.2/topics/migrations/
