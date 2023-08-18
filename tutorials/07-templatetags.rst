Tags de template personalizadas
===============================

Vamos fazer nosso blog listar entradas recentes na barra lateral.

Como vamos fazer isso? Poderíamos percorrer as entradas de blog em nosso template ``base.html``,
mas isso significa que precisaríamos incluir uma lista de nossas entradas de blog recentes no
contexto do template para todas as nossas exibições. Isso pode resultar em código duplicado e
não gostamos de código duplicado.

.. TIP::

    Se você não entendeu completamente o último parágrafo, tudo bem. `DRY`_ ou
    "Don't Repeat Yourself" é uma regra prática para uma boa prática de programação.
    Você pode querer ler a `documentação de template`_ Django novamente mais tarde.

Para evitar código duplicado, vamos criar uma `tag de template personalizadas`_
para nos ajudar a exibir entradas de blog recentes na barra lateral de todas as páginas

.. NOTE::
    Uma tag de template personalizada que aciona uma consulta SQL permite que nossos
    templates HTML adicionem mais consultas SQL à nossa visualização. Isso esconde
    algum comportamento. É muito cedo neste ponto, mas essa consulta deve ser armazenada
    em cache se esperamos usá-la com frequência.


Onde
-----

Vamos criar uma biblioteca de modelos chamada ``blog_tags``. Por quê ``blog_tags``?
Porque nomear nossa biblioteca de tags de acordo com nosso aplicativo tornará
nossas importações de modelo mais compreensíveis. Podemos usar esta biblioteca
de template em nossos templates escrevendo ``{% load blog_tags %}``  próximo ao
topo de nosso arquivo de template.

Crie um diretório ``templatetags`` em nosso aplicativo blog e crie
dois arquivos Python vazios dentro desse diretório: ``blog_tags.py``
(que conterá nosso código de biblioteca de modelos) e ``__init__.py``
(para transformar esse diretório em um pacote Python).

We should now have something like this::

    blog
    ├── admin.py
    ├── apps.py
    ├── forms.py
    ├── __init__.py
    ├── migrations
    │   ├── 0001_initial.py
    │   ├── 0002_auto_20141019_0232.py
    │   └── __init__.py
    ├── models.py
    ├── templatetags
    │   ├── blog_tags.py
    │   └── __init__.py
    ├── tests.py
    ├── urls.py
    └── views.py


Criando uma tag de inclusão
---------------------------

Vamos criar uma `tag de inclusão`_ para consultar entradas de blog recentes e renderizar
 uma lista delas. Vamos nomear nossa tag de modelo ``entry_history``.

Vamos começar renderizando um modelo vazio com um dicionário de contexto de modelo vazio.
Primeiro, vamos criar um arquivo ``templates/blog/_entry_history.html`` com algum texto fictício:

.. code-block:: html

    <p>Dummy text.</p>

Agora vamos criar nosso módulo ``blog/templatetags/blog_tags.py`` com nossa tag de template ``entry_history``:

.. code-block:: python

    from django import template

    register = template.Library()


    @register.inclusion_tag('blog/_entry_history.html')
    def entry_history():
        return {}

Vamos usar nossa tag em nosso arquivo de template base. Em nosso arquivo ``base.html``, importe nossa nova biblioteca de
template adicionando a linha ``{% load blog_tags %}`` próxima ao topo do arquivo.

Em seguida, modifique nossa segunda coluna para usar nossa tag de template ``entry_history``:

.. code-block:: html

    <div class="cell large-4">
        <h3>About Me</h3>
        <p>I am a Python developer and I like Django.</p>
        <h3>Recent Entries</h3>
        {% entry_history %}
    </div>

Reinicie o servidor e certifique-se de que nosso texto fictício apareça.

Fazendo funcionar
-----------------

Nós apenas escrevemos código sem escrever nenhum teste. Vamos escrever alguns testes agora.

No topo de ``blog/tests.py`` precisamos adicionar
``from django.template import Template, Context``. Precisamos dessas
importações porque iremos renderizar strings de modelo manualmente para
testar nossa tag de template.

Agora vamos adicionar um teste básico ao nosso arquivo ``blog/tests.py``:

.. code-block:: python

    class EntryHistoryTagTest(TestCase):

        TEMPLATE = Template("{% load blog_tags %} {% entry_history %}")

        def setUp(self):
            self.user = get_user_model().objects.create(username='zoidberg')

        def test_entry_shows_up(self):
            entry = Entry.objects.create(author=user, title="My entry title")
            rendered = self.TEMPLATE.render(Context({}))
            self.assertIn(entry.title, rendered)


As partes complicadas aqui são ``TEMPLATE``, ``Context({})`` e aquela chamada ``render()``. Tudo isso deve parecer um pouco
familiar do `tutorial do Django parte 3`_. ``Context({})``, neste caso, não passa dados para um ``Template`` que estamos
renderizando diretamente na memória. Essa última afirmação apenas verifica se o título da entrada está no texto.

Como esperado, nosso teste falha porque não estamos exibindo nenhuma entrada com nossa tag de template ``entry_history``:

.. code-block:: bash

    $ coverage run manage.py test blog
    Found 21 test(s).
    Creating test database for alias 'default'...
    System check identified no issues (0 silenced).
    .....F...............
    ======================================================================
    FAIL: test_entry_shows_up (blog.tests.EntryHistoryTagTest.test_entry_shows_up)
    ----------------------------------------------------------------------
    Traceback (most recent call last):
        ...
    AssertionError: 'My entry title' not found in ' <p>Dummy text.</p>'

    ----------------------------------------------------------------------
    Ran 21 tests in 0.404s

    FAILED (failures=1)
    Destroying test database for alias 'default'...

Vamos fazer com que nossa tag de template realmente exiba o histórico de entradas.
Primeiro, importaremos nosso modelo ``Entry`` no topo de nosso módulo de biblioteca de tags de template:

.. code-block:: python

    from ..models import Entry

.. NOTE::

    Para obter mais informações sobre a sintaxe ``..`` para importações, consulte a documentação do Python sobre `importações relativas`_.

Agora vamos enviar as últimas 5 entradas em nossa barra lateral:

.. code-block:: python

    def entry_history():
        entries = Entry.objects.all()[:5]
        return {'entries': entries}

Agora precisamos atualizar nosso arquivo ``_entry_history.html`` para exibir os
títulos dessas entradas de blog:

.. code-block:: html

    <ul>
        {% for entry in entries %}
            <li>{{ entry.title }}</li>
        {% endfor %}
    </ul>

Vamos executar nossos testes novamente e garantir que todos passem.

Tornando um pouco mais robusto
-------------------------------

O que acontece se ainda não tivermos nenhuma entrada de blog? A barra lateral
pode parecer um pouco estranha sem algum texto indicando que ainda não há entradas de blog.

Vamos adicionar um teste para quando não houver postagens no blog:

.. code-block:: python

    def test_no_posts(self):
        rendered = self.TEMPLATE.render(Context({}))
        self.assertIn("No recent entries", rendered)

O teste acima é para um caso extremo. Vamos adicionar um teste para outro caso extremo:
quando há mais de 5 entradas de blog recentes. Quando houver 6 postagens, apenas as
5 últimas devem ser exibidas. Vamos adicionar um teste para este caso também:

.. code-block:: python

    def test_many_posts(self):
        for n in range(6):
            Entry.objects.create(author=self.user, title="Post #{0}".format(n))
        rendered = self.TEMPLATE.render(Context({}))
        self.assertIn("Post #4", rendered)
        self.assertNotIn("Post #5", rendered)

A tag de template ``{% for %}`` nos permite definir uma tag ``{% empty %}``
que será exibida quando não houver entradas de blog (consulte a documentação de `for loops`_).

Atualize o template ``_entry_history.html`` para utilizar a tag ``{% empty %}``
e certifique-se de que os testes sejam aprovados.

.. code-block:: html

    <ul>
        {% for entry in entries %}
            <li>{{ entry.title }}</li>
        {% empty %}
            <li>No recent entries</li>
        {% endfor %}
    </ul>

.. _tag de template personalizadas: https://docs.djangoproject.com/en/dev/howto/custom-template-tags/#writing-custom-template-tags
.. _dry: https://en.wikipedia.org/wiki/Don%27t_repeat_yourself
.. _for loops: https://docs.djangoproject.com/en/dev/ref/templates/builtins/#for-empty
.. _documentação de template: https://docs.djangoproject.com/en/4.2/topics/templates/
.. _tag de inclusão: https://docs.djangoproject.com/en/1.6/howto/custom-template-tags/#howto-custom-template-tags-inclusion-tags
.. _tutorial do Django parte 3: https://docs.djangoproject.com/en/4.2/intro/tutorial03/
.. _importações relativas: https://docs.python.org/3/tutorial/modules.html#intra-package-references
