Models
======

Criando um app
---------------

Geralmente é uma boa prática separar seus projetos Django em vários aplicativos especializados (e às vezes reutilizáveis). Além disso, todo modelo Django deve residir em um aplicativo, portanto, você precisará de pelo menos um aplicativo para seu projeto.

Vamos criar um aplicativo para entradas de blog e modelos relacionados. Chamaremos o aplicativo de ``blog``:

.. code-block:: bash

    $ python manage.py startapp blog

Este comando deve ter criado um diretório ``blog`` com os seguintes arquivos e um subdiretório, migrations::

    __init__.py
    admin.py
    apps.py
    migrations
    models.py
    tests.py
    views.py

Vamos nos concentrar no arquivo ``models.py``.

Antes de podermos usar nosso aplicativo, precisamos adicioná-lo ao nosso ``INSTALLED_APPS`` em nosso arquivo de configurações (myblog/settings.py). Isso permitirá que o Django descubra os modelos em nosso arquivo ``models.py`` para que possam ser adicionados ao banco de dados ao executar a migração.

.. code-block:: python

    INSTALLED_APPS = [
        'blog.apps.BlogConfig',
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
    ]


.. NOTE::
    Apenas para ter certeza de que estamos na mesma página, a estrutura do seu projeto deve
    parece com isso:

    ::

        ├── blog
        │   ├── admin.py
        │   ├── apps.py
        │   ├── __init__.py
        │   ├── migrations
        │   │   └── __init__.py
        │   ├── models.py
        │   ├── tests.py
        │   └── views.py
        ├── db.sqlite3
        ├── manage.py
        ├── myblog
        │   ├── __init__.py
        │   ├── asgi.py
        │   ├── settings.py
        │   ├── urls.py
        │   └── wsgi.py
        └── requirements.txt


Criando um Model
----------------
Primeiro, vamos criar um model de entrada de blog escrevendo o código abaixo em nosso arquivo `blog/models.py`.
Models são objetos usados para fazer interface com seus dados e são descritos na `documentação do Django sobre models`_.
Nosso model corresponderá a uma tabela de banco de dados que conterá os dados para nossa entrada de blog.
Uma entrada de blog será representada por uma instância de nossa classe de model ``Entry`` e cada instância de model ``Entry``
identificará uma coluna em nossa tabela de banco de dados

.. _documentação do Django sobre models: https://docs.djangoproject.com/pt-br/4.2/topics/db/models/

.. code-block:: python

    from django.db import models


    class Entry(models.Model):
    title = models.CharField(max_length=500)
    author = models.ForeignKey('auth.User', on_delete=models.PROTECT)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    modified_at = models.DateTimeField(auto_now=True, editable=False)

Se você ainda não está familiarizado com bancos de dados, esse código pode ser um pouco assustador. Uma boa maneira de pensar sobre um model (ou uma tabela de banco de dados) é como uma folha em uma planilha. Cada campo como o ``title`` ou ``author`` é uma coluna na planilha e cada instância diferente do model (cada entrada de blog individual em nosso projeto) é uma linha na planilha.

Para criar a tabela de banco de dados para nosso modelo ``Entry``, precisamos fazer uma migração e a executar novamente:

.. code-block:: bash

    $ python manage.py makemigrations
    $ python manage.py migrate

Não se preocupe com os detalhes das migrações ainda, aprenderemos sobre elas em uma seção posterior do tutorial. Por enquanto, apenas pense nas migrações como a maneira do Django de gerenciar mudanças nos modelos e no banco de dados correspondente.

.. TIP::

    Se você notar, esse código é escrito de uma maneira muito particular. Há
    duas linhas em branco entre importações e definições de classe e o código é
    espaçado muito particularmente. Existe um guia de estilo para Python conhecido como
    `PEP8`_. Um princípio central do Python é que o código é lido com mais frequência
    do que está escrito. O estilo de código consistente ajuda os desenvolvedores a ler e
    entender um novo projeto mais rapidamente.

    .. _PEP8: https://peps.python.org/pep-0008/


Criando entradas pela interface de administração
------------------------------------------------

Não queremos adicionar entradas manualmente ao banco de dados toda vez que queremos atualizar nosso blog. Seria bom se pudéssemos usar uma página da Web protegida por login para criar entradas de blog. Felizmente, a interface de administração do Django pode fazer exatamente isso.

Para criar entradas de blog a partir da `interface de administração`_, precisamos registrar nosso modelo de ``Entry`` na interface de administração. Podemos fazer isso modificando nosso arquivo ``blog/admin.py`` para registrar o modelo ``Entry`` com a interface administrativa:

.. _interface de administração: https://docs.djangoproject.com/en/4.2/ref/contrib/admin/

.. code-block:: python

    from django.contrib import admin

    from .models import Entry


    admin.site.register(Entry)

Agora, inicie o servidor de desenvolvimento novamente e navegue até a interface de administração (http://localhost:8000/admin/) e crie uma entrada de blog.

.. code-block:: bash

    $ python manage.py runserver


Nosso primeiro teste: método __str__
------------------------------------

Na lista de alterações do administrador, nossas entradas têm o título inútil *Entry object*.
Adicione outra entrada igual à primeira, elas ficarão idênticas. Podemos personalizar a
forma como os modelos são referenciados criando um método ``__str__`` em nossa classe de modelo.
Os modelos são um bom lugar para colocar esse tipo de código reutilizável que é específico de um modelo.

Vamos primeiro criar um teste demonstrando o comportamento que gostaríamos de ver.

Todos os testes para nosso aplicativo ficarão no arquivo ``blog/tests.py``. Exclua tudo nesse arquivo e comece novamente com um teste com falha:

.. code-block:: python

    from django.test import TestCase


    class EntryModelTest(TestCase):

        def test_string_representation(self):
            self.fail("TODO Test incomplete")

Agora execute o comando test para garantir que o teste único do nosso aplicativo falhe conforme o esperado:

.. code-block:: bash

    $ python manage.py test blog

::

    Found 1 test(s).
    Creating test database for alias 'default'...
    System check identified no issues (0 silenced).
    F
    ======================================================================
    FAIL: test_string_representation (blog.tests.EntryModelTest.test_string_representation)
    ----------------------------------------------------------------------
    Traceback (most recent call last):
    ...
    AssertionError: TODO Test incomplete

    ----------------------------------------------------------------------
    Ran 1 test in 0.002s

    FAILED (failures=1)
    Destroying test database for alias 'default'...


Se lermos a saída com cuidado, o comando ``manage.py test`` fez algumas coisas. Primeiro, ele criou um banco de dados de teste. Isso é importante porque não queremos que os testes realmente modifiquem nosso banco de dados real. Em segundo lugar, executou cada "teste" em ``blog/tests.py``. Se tudo correr bem, o executor de teste não é muito falador, mas quando ocorrem falhas como em nosso teste, o executor de teste imprime muitas informações para ajudá-lo a depurar seu teste com falha.

Agora estamos prontos para criar um teste real.

.. TIP::

    Existem muitos recursos sobre testes de unidade, mas um ótimo lugar para começar
    é a documentação oficial do Python no módulo `unittest`_ e os documentos
    `Testando aplicações Django`_. Eles também têm boas recomendações sobre convenções
    de nomenclatura, e é por isso que nossas classes de teste são nomeadas como
    SomethingTest e nossos métodos são denominados test_something. Como muitos projetos
    adotam convenções semelhantes, os desenvolvedores podem entender o código com mais facilidade.

    .. _unittest: https://docs.python.org/3/library/unittest.html
    .. _Testando aplicações Django: https://docs.djangoproject.com/en/4.2/topics/testing/

Vamos escrever nosso teste para garantir que a representação de string de uma entrada de blog seja igual ao seu título. Precisamos modificar nosso arquivo de testes da seguinte forma:

.. code-block:: python

    from django.test import TestCase

    from .models import Entry


    class EntryModelTest(TestCase):

        def test_string_representation(self):
            entry = Entry(title="My entry title")
            self.assertEqual(str(entry), entry.title)

Agora, vamos rodar os testes novamente:

.. code-block:: bash

    $ python manage.py test blog

::

    Found 1 test(s).
    Creating test database for alias 'default'...
    System check identified no issues (0 silenced).
    F
    ======================================================================
    FAIL: test_string_representation (blog.tests.EntryModelTest.test_string_representation)
    ----------------------------------------------------------------------
    Traceback (most recent call last):
    ...
    AssertionError: 'Entry object (None)' != 'My entry title'
    - Entry object (None)
    + My entry title


    ----------------------------------------------------------------------
    Ran 1 test in 0.002s

    FAILED (failures=1)
    Destroying test database for alias 'default'...

Nosso teste falha novamente, mas desta vez falha porque ainda não personalizamos nosso método ``__str__``, então a representação de string para nosso model ainda é o *Entry object* padrão.

Vamos adicionar um método ``__str__`` ao nosso modelo que retorna o título da entrada. Nosso arquivo ``models.py`` deve se parecer com isto:

.. code-block:: python

    from django.db import models


    class Entry(models.Model):
        title = models.CharField(max_length=500)
        author = models.ForeignKey('auth.User', on_delete=models.PROTECT)
        body = models.TextField()
        created_at = models.DateTimeField(auto_now_add=True, editable=False)
        modified_at = models.DateTimeField(auto_now=True, editable=False)

        def __str__(self):
            return self.title

Se você iniciar o servidor de desenvolvimento e verificar a interface administrativa (http://localhost:8000/admin/) novamente, verá os títulos das entradas na lista de entradas.

Agora, se executarmos nosso teste novamente, veremos que nosso único teste passa.

.. code-block:: bash

    $ python manage.py test blog

::

    Found 1 test(s).
    Creating test database for alias 'default'...
    System check identified no issues (0 silenced).
    .
    ----------------------------------------------------------------------
    Ran 1 test in 0.001s

    OK
    Destroying test database for alias 'default'...


Acabamos de escrever nosso primeiro teste e corrigimos nosso código para fazer nosso teste passar.

Test Driven Development (TDD) é sobre como escrever um teste com falha e, em seguida, fazê-lo passar. Se você escrevesse seu código primeiro e depois escrevesse os testes, seria mais difícil saber se o teste que você escreveu realmente testa o que você deseja.

Embora isso possa parecer um exemplo trivial, bons testes são uma maneira de documentar o comportamento esperado de um programa. Um ótimo conjunto de testes é um sinal de um aplicativo maduro, pois partes e partes podem ser alteradas facilmente e os testes garantirão que o programa ainda funcione como pretendido. A própria estrutura do Django possui um enorme conjunto de testes de unidade com milhares de testes.

Próximo Teste: Entrys
---------------------

Você notou que o plural de entry está escrito incorretamente na interface de administração? "Entrys" deve ser lida como "Entries". Vamos escrever um teste para verificar se o Django pluraliza corretamente "Entry" para "Entries".

Vamos adicionar um teste à nossa classe ``EntryModelTest``:

.. code-block:: python

    def test_verbose_name_plural(self):
        self.assertEqual(str(Entry._meta.verbose_name_plural), "entries")

.. NOTE::

    Este teste usa a classe ``_meta`` do modelo (criada com base na classe ``Meta`` que definiremos). Este é um exemplo de um recurso avançado do Django.

Agora vamos fazer nosso teste passar especificando o nome detalhado para nosso modelo.

Adicione uma classe interna ``Meta`` dentro do nosso modelo ``Entry``, assim:

.. code-block:: python

    class Entry(models.Model):

        # The rest of our model code

        class Meta:
            verbose_name_plural = "entries"

.. HINT::

    Consulte a documentação do Django para obter informações sobre `verbose_name_plural`_ na classe Meta.

.. _verbose_name_plural: https://docs.djangoproject.com/en/4.2/ref/models/options/#verbose-name-plural
