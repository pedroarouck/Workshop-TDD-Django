Views and Templates
===================

Agora podemos criar entradas de blog e vê-las na interface administrativa, mas ninguém mais pode ver nossas entradas de blog ainda.


O Teste da Página Inicial
-------------------------

Todo site deve ter uma página inicial. Vamos escrever um teste com falha para isso.

Podemos usar o `cliente de teste`_ Django para criar um teste para garantir que nossa página inicial retorne um código de status HTTP 200 (essa é a resposta padrão para uma solicitação HTTP bem-sucedida).

Vamos adicionar o seguinte ao nosso arquivo ``blog/tests.py``:

.. code-block:: python


    class ProjectTests(TestCase):

        def test_homepage(self):
            response = self.client.get('/')
            self.assertEqual(response.status_code, 200)


Se executarmos nossos testes agora, esse teste deve falhar porque ainda não criamos uma página inicial.


.. HINT::

    Há muito mais informações sobre o `protocolo de transferência de hipertexto`_ (HTTP)
    e seus vários `códigos de status`_ na Wikipedia. Referência rápida, 200 = OK;
    404 = Não encontrado; 500 = Erro do servidor

Template base e arquivos estáticos
----------------------------------

Vamos começar com modelos básicos baseados na fundação zurb. Primeiro baixe e extraia os `arquivos da Fundação Zurb`_ (`direct link`_).

Zurb Foundation é um framework CSS, HTML e JavaScript para construção do front-end de sites.
Em vez de tentar projetar um site totalmente do zero, o Foundation oferece um bom ponto de
partida para projetar e construir um site atraente e compatível com os padrões que funciona
bem em dispositivos como laptops, tablets e telefones.


Arquivos estáticos
~~~~~~~~~~~~~~~~~~

Crie um diretório ``static`` em nosso diretório top-level (aquele com o ``manage.py``). Copie o diretório ``css`` do arquivo da fundação Zurb para este novo diretório ``static``.

Agora vamos adicionar esta nova definição de diretório ``static`` ao nosso arquivo ``myblog/settings.py``:

.. code-block:: python

    STATICFILES_DIRS = [
        BASE_DIR / 'static',
    ]

Para mais detalhes, veja a documentação do Django sobre `arquivos estáticos`_.

.. IMPORTANT::

    Este workshop é focado em Python e Django e, por necessidade,
    vamos explicar um pouco sobre HTML, CSS e JavaScript. No entanto,
    praticamente todos os sites têm um front-end construído com esses
    blocos de construção fundamentais da web aberta.


Arquivos de Template
~~~~~~~~~~~~~~~~~~~~

Os `templates`_ são uma maneira de gerar dinamicamente vários documentos semelhantes,
mas com alguns dados ligeiramente diferentes. No sistema de blog que estamos construindo,
queremos que todas as nossas entradas de blog sejam visualmente semelhantes,
mas o texto real de uma determinada entrada de blog varia. Teremos um único template
para todas as nossas entradas de blog e o template conterá variáveis que serão substituídas
quando uma entrada de blog for renderizada. Essa reutilização com a qual o Django ajuda e
o conceito de manter as coisas em um único lugar é chamada de princípio DRY para Don't Repeat Yourself.


.. _templates: https://docs.djangoproject.com/en/4.2/topics/templates/#module-django.template

Crie um diretório ``templates`` em nosso diretório top-level. Nossa estrutura de diretórios deve se paracer com isso:

.. code-block:: bash

    ├── blog
    │   ├── admin.py
    │   ├── __init__.py
    │   ├── apps.py
    │   ├── migrations
    │   │   ├── 0001_initial.py
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
    ├── requirements.txt
    ├── static
    │   └── css
    │       ├── foundation.css
    │       ├── foundation.min.css
    │       └── app.css
    └── templates

Crie um arquivo HTML básico como este e nomeie-o ``templates/index.html``:

.. code-block:: html

    {% load static %}
    <!DOCTYPE html>
    <html>
    <head>
        <title>My Blog</title>
        <link rel="stylesheet" href="{% static "css/foundation.css" %}">
    </head>
    <body>
        <section class="grid-x ">
            <header class="cell">
                <h1 class="text-center">Welcome to My Blog</h1>
                <hr>
            </header>
        </section>
    </body>
    </html>

Agora informe o Django sobre este novo diretório ``templates`` adicionando-o nosso arquivo ``myblog/settings.py``:

.. code-block:: python

    TEMPLATES = [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [BASE_DIR / "templates"],
            'APP_DIRS': True,
            'OPTIONS': {
                'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                ],
            },
        },
    ]


Para quase tudo o que há para saber sobre os templates do Django, leia
a `documentação sobre templates`_.

.. TIP::
    Em nossos exemplos, os templates serão usados para gerar
    páginas HTML. No entanto, o sistema de templates do Django pode ser usado para gerar
    qualquer tipo de documento de texto simples, como CSS, JavaScript, CSV ou XML.


Views
-----

Agora vamos criar uma página inicial usando o template ``index.html`` que adicionamos.

Vamos começar criando um arquivo de views: ``myblog/views.py`` referenciando o template ``index.html``:

.. code-block:: python

    from django.views.generic import TemplateView


    class HomeView(TemplateView):

        template_name = 'index.html'

.. IMPORTANT::

    Estamos criando este arquivo views no diretório do projeto``myblog`` (ao lado do arquivo ``myblog/urls.py`` que estamos prestes a alterar). Ainda **não** estamos alterando o arquivo ``blog/views.py``. Usaremos esse arquivo mais tarde.

O Django poderá encontrar este template na pasta ``templates`` devido à nossa configuração no ``TEMPLATE_DIRS``.
Agora precisamos rotear o URL da página inicial para a visualização inicial. Nosso arquivo de URL ``myblog/urls.py`` deve se parecer com isto:

.. code-block:: python

    from django.contrib import admin
    from django.urls import include, path
    from myblog import views


    urlpatterns = [
        path('admin/', admin.site.urls),
        path('', views.HomeView.as_view(), name='home'),
    ]

Agora vamos visitar http://localhost:8000/ em um navegador da web para verificar nosso trabalho.
(Reinicie seu servidor com o comando `python manage.py runserver`).
Agora vamos garantir que nosso novo teste passe:

.. code-block:: bash

    $ python manage.py test blog

::

    Found 3 test(s).
    Creating test database for alias 'default'...
    System check identified no issues (0 silenced).
    ...
    ----------------------------------------------------------------------
    Ran 3 tests in 0.020s

    OK
    Destroying test database for alias 'default'...


.. HINT::
    De uma perspectiva de fluxo de código, agora temos um exemplo funcional de como o Django
    cria páginas web dinâmicas. Quando uma requisição HTTP para um web site desenvolvido com
    Django é enviada, o arquivo ``urls.py`` contém uma série de padrões para corresponder a URL
    daquela requisição web. A URL correspondente delega a solicitação para uma visualização
    correspondente (ou para outro conjunto de URLs que mapeiam a solicitação para uma visualização).
    Por fim, a exibição delega a solicitação a um modelo para renderizar o HTML real.

    Na arquitetura de sites da Web, essa separação de preocupações é conhecida como arquitetura
    de três camadas ou arquitetura de model-view-controller.

Usando um Template Base
~~~~~~~~~~~~~~~~~~~~~~~

Os templates no Django geralmente são construídos a partir de peças menores. Isso permite que você inclua coisas como um cabeçalho e rodapé consistentes em todas as suas páginas. A convenção é chamar um de seus modelos ``base.html`` e ter tudo herdado disso. Aqui estão mais informações sobre `herança de template com blocos`_ .

.. _herança de template com blocos: https://docs.djangoproject.com/en/4.2/ref/templates/language/#template-inheritance

Começaremos colocando nosso cabeçalho e uma barra lateral em ``templates/base.html``:

.. code-block:: html

    {% load static %}
    <!DOCTYPE html>
    <html>
    <head>
        <title>My Blog</title>
        <link rel="stylesheet" href="{% static "css/foundation.css" %}">
    </head>
    <body>
        <section class="grid-x ">
            <header class="cell">
                <h1 class="text-center">Welcome to My Blog</h1>
                <hr>
            </header>
        </section>

        <section class="grid-x grid-padding-x align-center">

            <div class="cell large-8">
                {% block content %}{% endblock %}
            </div>

            <div class="cell large-4">
                <h3>About Me</h3>
                <p>I am a Python developer and I like Django.</p>
            </div>

        </section>

    </body>
    </html>

.. NOTE::

    Não explicaremos as classes CSS que usamos acima (por exemplo, ``large-8``, ``column``, ``row``). Mais informações sobre essas classes podem ser encontradas na documentação de `grid da Fundação Zurb`_.

Há muito código duplicado entre nosso ``templates/base.html`` e ``templates/index.html``.
Os templates do Django fornecem uma forma de fazer com que os templates herdem a estrutura de outros templates.
Isso permite que um modelo defina apenas alguns elementos, mas mantenha a estrutura geral de seu modelo pai.

Se atualizarmos nosso template ``index.html`` para estender ``base.html`` poderemos ver isso em ação.
Exclua tudo ``templates/index.html`` e substitua pelo seguinte:

.. code-block:: html

    {% extends "base.html" %}

    {% block content %}
    Page body goes here.
    {% endblock content %}


Agora, ``templates/index.html`` substitui o bloco ``content`` em ``templates/base.html``.
Para mais detalhes sobre este poderoso recurso do Django, você pode ler a documentação sobre `herança de template`_.

.. _herança de template: https://docs.djangoproject.com/en/4.2/ref/templates/language/#template-inheritance


ListViews
---------

Colocamos um título e um artigo hard-codados em nossa visualização de preenchimento. Essas informações de entrada devem vir de nossos models e banco de dados. Vamos escrever um teste para isso.

O ``cliente de teste`` do Django pode ser usado para um teste simples de se o texto aparece em uma página. Vamos adicionar o seguinte ao nosso arquivo ``blog/tests.py``:

.. code-block:: python

    from django.contrib.auth import get_user_model

    class HomePageTests(TestCase):

        """Test whether our blog entries show up on the homepage"""

        def setUp(self):
            self.user = get_user_model().objects.create(username='some_user')

        def test_one_entry(self):
            Entry.objects.create(title='1-title', body='1-body', author=self.user)
            response = self.client.get('/')
            self.assertContains(response, '1-title')
            self.assertContains(response, '1-body')

        def test_two_entries(self):
            Entry.objects.create(title='1-title', body='1-body', author=self.user)
            Entry.objects.create(title='2-title', body='2-body', author=self.user)
            response = self.client.get('/')
            self.assertContains(response, '1-title')
            self.assertContains(response, '1-body')
            self.assertContains(response, '2-title')

O qual tem que falhar assim:

.. code-block:: bash

    Found 5 test(s).
    Creating test database for alias 'default'...
    System check identified no issues (0 silenced).
    ..FF.
    ======================================================================
    FAIL: test_one_entry (blog.tests.HomePageTests.test_one_entry)
    ----------------------------------------------------------------------
    Traceback (most recent call last):
        ...
    AssertionError: False is not true : Couldn't find '1-title' in response

    ======================================================================
    FAIL: test_two_entries (blog.tests.HomePageTests.test_two_entries)
    ----------------------------------------------------------------------
    Traceback (most recent call last):
        ...
    AssertionError: False is not true : Couldn't find '1-title' in response

    ----------------------------------------------------------------------
    Ran 5 tests in 0.036s

    FAILED (failures=2)
    Destroying test database for alias 'default'...


Atualizando nossas Views
~~~~~~~~~~~~~~~~~~~~~~~~

Uma maneira fácil de obter todos os nossos objetos de entrada para listas é apenas usar um ``ListView``. Isso muda o nosso ``HomeView`` um pouco.

.. code-block:: python

    from django.views.generic import ListView

    from blog.models import Entry


    class HomeView(ListView):
        template_name = 'index.html'
        queryset = Entry.objects.order_by('-created_at')


.. IMPORTANT::

    Certifique-se de atualizar seu ``HomeView`` para herdar de ``ListView``. Lembre-se de que ainda é em ``myblog/views.py``.

Essa pequena alteração fornecerá um objeto ``entry_list`` ao nosso model ``index.html``, no qual podemos fazer um loop. Para alguma documentação rápida sobre todas as visões baseadas em classes no django, dê uma olhada em `Classy Class Based Views`_.

A última alteração necessária é apenas atualizar nosso modelo de página inicial para adicionar as entradas do blog. Vamos substituir nosso arquivo ``templates/index.html`` pelo seguinte:

.. code-block:: html

    {% extends "base.html" %}

    {% block content %}
        {% for entry in entry_list %}
            <article class="card text-center" >
                <div class="card-divider" style="justify-content: center;">
                    <h2 ><a href="{{ entry.get_absolute_url }}" >{{ entry.title }}</a></h2>
                </div>
                <div class="card-section">
                    <p class="subheader">
                        <time>{{ entry.modified_at|date }}</time>
                    </p>

                    <p>
                        {{ entry.body|linebreaks }}
                    </p>
                </div>
            </article>
        {% endfor %}
    {% endblock content %}

.. NOTE::

    A referência ``entry.get_absolute_url`` ainda não faz nada. Posteriormente, adicionaremos um método ``get_absolute_url`` ao modelo de entrada que fará com que esses links funcionem.

.. TIP::

    Observe que não especificamos o nome ``entry_list`` em nosso código. As visualizações genéricas baseadas em classe do Django geralmente adicionam variáveis nomeadas automaticamente ao seu contexto de template com base nos nomes de seu modelo. Nesse caso específico, o nome do objeto de contexto foi definido automaticamente pelo método `get_context_object_name`_ no ``ListView``. Em vez de referenciar ``entry_list`` em nosso template, poderíamos também ter referenciado a variável de contexto do modelo ``object_list``.

Fazendo os testes aqui vemos que todos os testes passam!

.. NOTE::

    Leia a documentação de `filtros e tags de modelo integrados`_ do Django para obter mais detalhes sobre quebras de linha e filtros de modelo de data.

E agora, se adicionarmos algumas entradas em nosso admin, elas devem aparecer na página inicial. O que acontece se não houver entradas? Devemos adicionar um teste para isso:

.. code-block:: python

    def test_no_entries(self):
        response = self.client.get('/')
        self.assertContains(response, 'No blog entries yet.')

Este teste nos dá a falha esperada

.. code-block:: bash

    Found 6 test(s).
    Creating test database for alias 'default'...
    System check identified no issues (0 silenced).
    ..F...
    ======================================================================
    FAIL: test_no_entries (blog.tests.HomePageTests.test_no_entries)
    ----------------------------------------------------------------------
    Traceback (most recent call last):
        ...
    AssertionError: False is not true : Couldn't find 'No blog entries yet.' in response

    ----------------------------------------------------------------------
    Ran 6 tests in 0.060s

    FAILED (failures=1)
    Destroying test database for alias 'default'...

A maneira mais fácil de implementar esse recurso é usar a cláusula `empty`_:

.. code-block:: html

    {% extends "base.html" %}

    {% block content %}
        {% for entry in entry_list %}
            <article class="card text-center" >
                <div class="card-divider" style="justify-content: center;">
                    <h2 ><a href="{{ entry.get_absolute_url }}" >{{ entry.title }}</a></h2>
                </div>
                <div class="card-section">
                    <p class="subheader">
                        <time>{{ entry.modified_at|date }}</time>
                    </p>

                    <p>
                        {{ entry.body|linebreaks }}
                    </p>
                </div>
            </article>
            {% empty %}
                <p>No blog entries yet.</p>
        {% endfor %}
    {% endblock content %}

.. HINT::
    Lembre-se de que a frase na cláusula empty deve conter a mesma frase que verificamos em nosso teste ("No blog entries yet.").

Que tal ver uma entrada individual no blog?

Entradas no blog, URLs e Views
------------------------------

Para simplificar, vamos concordar com uma diretriz de projeto para formar nossos urls para parecer ``http://myblog.com/ID/`` onde ID é o ID do banco de dados da entrada de blog específica que queremos exibir. Nesta seção, criaremos uma página de `detalhes de entrada de blog` e usaremos a diretriz de URL do nosso projeto.

Antes de criarmos esta página, vamos mover o conteúdo do template que exibe nossas entradas de blog em nossa página inicial (``templates/index.html``) para um novo arquivo de template separado para que possamos reutilizar a lógica de exibição de entrada de blog em nossa página de `detalhes de entrada de blog`.

Vamos criar um arquivo de template chamado ``templates/_entry.html`` e colocar o seguinte nele:

.. code-block:: html

    <article class="card text-center" >
        <div class="card-divider" style="justify-content: center;">
            <h2 ><a href="{{ entry.get_absolute_url }}" >{{ entry.title }}</a></h2>
        </div>
        <div class="card-section">
            <p class="subheader">
                <time>{{ entry.modified_at|date }}</time>
            </p>

            <p>
                {{ entry.body|linebreaks }}
            </p>
        </div>
    </article>

.. TIP::

    O nome do arquivo do nosso modelo inclusivel começa com ``_`` por convenção. Essa convenção de nomenclatura é recomendada por Harris Lapiroff em An Architecture for Django Templates.

Agora vamos alterar nosso template de página inicial (``templates/index.html``) para incluir o arquivo de template que acabamos de criar:

.. code-block:: html

    {% extends "base.html" %}

    {% block content %}
        {% for entry in entry_list %}
            {% include "_entry.html" with entry=entry only %}
        {% empty %}
            <p>No blog entries yet.</p>
        {% endfor %}
    {% endblock content %}

.. TIP::

    Usamos a convenção ``with entry=entry only`` em nossa tag ``include`` para um melhor encapsulamento. Verifique a documentação do Django para mais informações sobre a `tag include`_.

Agora, vamos escrever um teste para nossas novas páginas de entrada de blog:

.. code-block:: python

    class EntryViewTest(TestCase):

        def setUp(self):
            self.user = get_user_model().objects.create(username='some_user')
            self.entry = Entry.objects.create(title='1-title', body='1-body',
                                              author=self.user)

        def test_basic_view(self):
            response = self.client.get(self.entry.get_absolute_url())
            self.assertEqual(response.status_code, 200)

Este teste falha porque não definimos o método ``get_absolute_url`` para nosso modelo ``Entry`` (`Django Model Instance Documentation`_). Vamos precisar de um URL absoluto para corresponder a uma entrada de blog individual.

Precisamos criar um URL e uma view para as páginas de entrada do blog. Faremos um novo arquivo ``blog/urls.py`` e o referenciaremos no arquivo``myblog/urls.py``.

Nosso aquivo ``blog/urls.py`` é bem breve:

.. code-block:: python

    from django.urls import path

    from . import views

    urlpatterns = [
    path('<int:pk>/', views.EntryDetail.as_view(), name='entry_detail'),
    ]



O urlconf em ``myblog/urls.py`` precisa referenciar ``blog.urls``:

.. code-block:: python

    from django.contrib import admin
    from django.urls import include, path
    from myblog import views
    import blog.urls


    urlpatterns = [
        path('admin/', admin.site.urls),
        path('', views.HomeView.as_view(), name='home'),
        path('', include(blog.urls)),
    ]

Lembre-se, estamos trabalhando para criar uma maneira de ver entradas individuais.
Agora precisamos definir uma classe de exibição ``EntryDetail`` em nosso arquivo ``blog/views.py``.
Para implementar nossa página de entrada de blog, usaremos outra visualização genérica baseada em classe:
a `DetailView`_. A ``DetailView`` é uma visualização para exibir os detalhes de uma instância de um modelo
e renderizá-la em um template. Vamos substituir o conteúdo do arquivo  ``blog/views.py`` pelo seguinte:

.. code-block:: python

    from django.views.generic import DetailView
    from .models import Entry


    class EntryDetail(DetailView):
        model = Entry


Vejamos como criar a função ``get_absolute_url()`` que deve retornar o URL individual e absoluto do detalhe da entrada para cada entrada do blog. Devemos criar um teste primeiro. Vamos adicionar o seguinte teste à nossa classe ``EntryModelTest``:
Let's look at how to create the ``get_absolute_url()`` function which should return the individual, absolute entry detail URL for each blog entry. We should create a test first.  Let's add the following test to our ``EntryModelTest`` class:

.. code-block:: python

    def test_get_absolute_url(self):
        user = get_user_model().objects.create(username='some_user')
        entry = Entry.objects.create(title="My entry title", author=user)
        self.assertIsNotNone(entry.get_absolute_url())

Agora precisamos implementar nosso método ``get_absolute_url`` em nossa classe ``Entry`` (encontrada em ``blog/models.py``):

.. code-block:: python

    from django.core.urlresolvers import reverse

    # And in our Entry model class...

    def get_absolute_url(self):
        return reverse('entry_detail', kwargs={'pk': self.pk})

.. TIP::
    Para ler mais sobre a função utilitária, reverse, veja a documentação do Django
    em `django.core.urlresolvers.reverse`_.

    .. _django.core.urlresolvers.reverse: https://docs.djangoproject.com/en/4.2/ref/urlresolvers/#reverse

Vamos fazer com que a página de exibição de detalhes da entrada do blog realmente exiba uma entrada do blog. Primeiro vamos escrever alguns testes em nossa classe ``EntryViewTest``:

.. code-block:: python

    def test_title_in_entry(self):
        response = self.client.get(self.entry.get_absolute_url())
        self.assertContains(response, self.entry.title)

    def test_body_in_entry(self):
        response = self.client.get(self.entry.get_absolute_url())
        self.assertContains(response, self.entry.body)


Agora veremos alguns erros de ``TemplateDoesNotExist`` ao executar nossos testes.

.. code-block:: bash

    $ python manage.py test blog

::

    Found 10 test(s).
    Creating test database for alias 'default'...
    System check identified no issues (0 silenced).
    ...EEE....
    ======================================================================
    ERROR: test_basic_view (blog.tests.EntryViewTest.test_basic_view)
    ----------------------------------------------------------------------
    Traceback (most recent call last):
        ...
    django.template.exceptions.TemplateDoesNotExist: blog/entry_detail.html

    ======================================================================
    ERROR: test_body_in_entry (blog.tests.EntryViewTest.test_body_in_entry)
    ----------------------------------------------------------------------
    Traceback (most recent call last):
        ...
    django.template.exceptions.TemplateDoesNotExist: blog/entry_detail.html

    ======================================================================
    ERROR: test_title_in_entry (blog.tests.EntryViewTest.test_title_in_entry)
    ----------------------------------------------------------------------
    Traceback (most recent call last):
        ...
    django.template.exceptions.TemplateDoesNotExist: blog/entry_detail.html

    ----------------------------------------------------------------------
    Ran 10 tests in 0.158s

    FAILED (errors=3)
    Destroying test database for alias 'default'...

Esses erros estão nos dizendo que estamos referenciando um template``blog/entry_detail.html``, mas ainda não criamos esse arquivo.

Estamos muito perto de poder ver os detalhes individuais da entrada do blog. Vamos fazê-lo. Primeiro, crie um ``templates/blog/entry_detail.html`` como nosso template de exibição de detalhes de entrada de blog. O ``DetailView`` usará uma variável de contexto ``entry`` para referenciar nossa instância de modelo ``Entry``. Nosso novo modelo de exibição de detalhes de entrada de blog deve ser semelhante a este:

.. code-block:: html

    {% extends "base.html" %}

    {% block content %}
        {% include "_entry.html" with entry=entry only %}
    {% endblock %}

Agora nossos testes devem passar:

.. code-block:: bash

    $ python manage.py test blog

::

    Found 10 test(s).
    Creating test database for alias 'default'...
    System check identified no issues (0 silenced).
    ..........
    ----------------------------------------------------------------------
    Ran 10 tests in 0.083s

    OK
    Destroying test database for alias 'default'...


.. _cliente de teste: https://docs.djangoproject.com/en/4.2/topics/testing/tools/#the-test-client
.. _arquivos da Fundação Zurb: https://get.foundation/
.. _grid da Fundação Zurb: https://get.foundation/sites/docs/xy-grid.html
.. _direct link: https://static.foundationcss.com/sites-css-latest
.. _arquivos estáticos: https://docs.djangoproject.com/pt-br/4.2/howto/static-files/
.. _protocolo de transferência de hipertexto: http://en.wikipedia.org/wiki/Hypertext_Transfer_Protocol
.. _códigos de status: http://en.wikipedia.org/wiki/List_of_HTTP_status_codes
.. _documentação sobre templates: https://docs.djangoproject.com/en/4.2/topics/templates/
.. _filtros e tags de modelo integrados: https://docs.djangoproject.com/en/4.2/ref/templates/builtins/
.. _get_context_object_name: https://docs.djangoproject.com/en/4.2/ref/class-based-views/mixins-single-object/#django.views.generic.detail.SingleObjectMixin.get_context_object_name
.. _Classy Class Based Views: http://ccbv.co.uk
.. _Django Model Instance Documentation: https://docs.djangoproject.com/en/4.2/ref/models/instances/
.. _DetailView: http://ccbv.co.uk/projects/Django/1.7/django.views.generic.detail/DetailView/
.. _tag include: https://docs.djangoproject.com/en/4.2/ref/templates/builtins/#std-templatetag-include
.. _empty: https://docs.djangoproject.com/en/1.7/ref/templates/builtins/#for-empty
