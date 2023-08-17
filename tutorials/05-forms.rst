Formulários
===========


Adicionando um formulário
-------------------------

Para permitir que os usuários criem comentários, precisamos aceitar o
envio de um formulário. Os formulários HTML são o método mais comum usado
para aceitar a entrada do usuário em sites da Web e enviar esses dados
para um servidor. Podemos usar o `framework de formulários do Django`_ para esta tarefa.

.. _framework de formulários do Django: https://docs.djangoproject.com/en/4.2/topics/forms/

Primeiro vamos escrever alguns testes. Precisamos criar um blog ``Entry``
e um ``User`` para nossos testes. Vamos criar um método de `setup`_ para
nossos testes que cria uma entrada e a adiciona ao banco de dados.
O método de `setup`_ é chamado antes de cada teste na classe de teste
fornecida para que cada teste possa usar o ``User`` e ``Entry``.

.. _setup: https://docs.python.org/3/library/unittest.html#unittest.TestCase.setUpClass

.. code-block:: python

    class CommentFormTest(TestCase):

        def setUp(self):
            user = get_user_model().objects.create_user('zoidberg')
            self.entry = Entry.objects.create(author=user, title="My entry title")

Vamos nos certificar de que importamos ``CommentForm`` nosso arquivo de testes.
Nossas importações devem ficar assim:

.. code-block:: python

    from django.test import TestCase
    from django.contrib.auth import get_user_model

    from .forms import CommentForm
    from .models import Entry, Comment

Antes de começarmos a testar nosso formulário, lembre-se de que estamos escrevendo
nossos testes antes de realmente escrever nosso código de CommentForm. Em outras
palavras, estamos fingindo que já escrevemos nosso código da maneira que queremos que
funcione, então estamos escrevendo testes para esse código ainda não escrito. Depois
de ver que os testes falharam, escrevemos o código real. Por fim, executamos os testes
novamente em nosso código implementado e, se necessário, modificamos o código real para
que os testes sejam executados com sucesso.

Nosso primeiro teste deve garantir que nosso formulário ``__init__`` aceite um argumento ``entry``.

.. code-block:: python

    def test_init(self):
        CommentForm(entry=self.entry)

Qqueremos vincular nossos comentários às entradas, permitindo que nosso formulário aceite um argumento ``entry``.
Assumindo que nosso ``CommentForm`` foi escrito dessa forma, é assim que gostariamos de usar:
(**você não precisa digitar esse código em nenhuma parta**):

.. code-block:: pycon

    >>> form = CommentForm(entry=entry)  # Without form data
    >>> form = CommentForm(request.POST, entry=entry)  # with form data

Nosso próximo teste deve garantir que nosso formulário gere uma exceção
se um argumento ``entry`` não for especificado:

.. code-block:: python

    def test_init_without_entry(self):
        with self.assertRaises(KeyError):
            CommentForm()

Agora vamos rodar nossos testes

.. code-block:: bash

    $ python manage.py test blog

::

    ImportError: No module named 'blog.forms'

Ainda não criamos nosso arquivo de formulários, então nossa importação
está falhando. Vamos criar um arquivo ``blog/forms.py``.

Agora nós temos:

.. code-block:: bash

    $ python manage.py test blog

::

    ImportError: cannot import name 'CommentForm'

Precisamos criar nosso model de formulário ``CommentForm`` em ``blog/forms.py``.
Este formulário processará os dados enviados pelos usuários que tentam
comentar em uma entrada de blog e garantirá que eles possam ser salvos em
nosso banco de dados de blogs. Vamos começar com algo simples:

.. code-block:: python

    from django import forms

    from .models import Comment


    class CommentForm(forms.ModelForm):
        class Meta:
            model = Comment
            fields = ('name', 'email', 'body')

Aqui criamos um formulário simples associado ao nosso modelo de comentário
e especificamos que o formulário manuseia apenas um subconjunto de todos os
campos do comentário.

.. IMPORTANT::
    Os `formulários Django`_ são uma maneira poderosa de lidar com formulários HTML.
    Eles fornecem uma maneira unificada de verificar os envios em relação às regras
    de validação e, no caso da subclasse ModelForm, compartilham qualquer um dos
    validadores do modelo associado. Em nosso exemplo, isso garantirá que o comentário
    email seja um endereço de e-mail válido.

    .. _formulários Django: https://docs.djangoproject.com/en/4.2/topics/forms/

Agora nossos testes devem falhar porque o argumento ``entry`` não é aceito nem obrigatório.

.. code-block:: bash

    $ python manage.py test blog

::

    Found 15 test(s).
    Creating test database for alias 'default'...
    System check identified no issues (0 silenced).
    EF.............
    ======================================================================
    ERROR: test_init (blog.tests.CommentFormTest.test_init)
    ----------------------------------------------------------------------
    Traceback (most recent call last):
        ...
    TypeError: BaseModelForm.__init__() got an unexpected keyword argument 'entry'

    ======================================================================
    FAIL: test_init_without_entry (blog.tests.CommentFormTest.test_init_without_entry)
    ----------------------------------------------------------------------
    Traceback (most recent call last):
        ...
    AssertionError: KeyError not raised

    ----------------------------------------------------------------------
    Ran 15 tests in 0.097s

    FAILED (failures=1, errors=1)
    Destroying test database for alias 'default'...


Nossos dois testes de formulário falham conforme o esperado. Vamos criar
mais alguns testes para nosso formulário antes de começar a corrigi-lo.
Devemos criar pelo menos dois testes para garantir que nossa validação
de formulário funcione:

1. Certifique-se de que ``form.is_valid()`` é ``True`` para um envio de formulário com dados válidos
2. Certifique-se de que ``form.is_valid()`` é ``False`` para um envio de formulário com dados inválidos
    (de preferência um teste separado para cada tipo de erro)

This is a good start:

.. code-block:: python

    def test_valid_data(self):
        form = CommentForm({
            'name': "Turanga Leela",
            'email': "leela@example.com",
            'body': "Hi there",
        }, entry=self.entry)
        self.assertTrue(form.is_valid())
        comment = form.save()
        self.assertEqual(comment.name, "Turanga Leela")
        self.assertEqual(comment.email, "leela@example.com")
        self.assertEqual(comment.body, "Hi there")
        self.assertEqual(comment.entry, self.entry)

    def test_blank_data(self):
        form = CommentForm({}, entry=self.entry)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors, {
            'name': ['required'],
            'email': ['required'],
            'body': ['required'],
        })

Geralmente é melhor testar demais do que testar de menos.

Agora vamos finalmente escrever nosso código de formulário.

.. code-block:: python

    from django import forms

    from .models import Comment


    class CommentForm(forms.ModelForm):

        class Meta:
            model = Comment
            fields = ('name', 'email', 'body')

        def __init__(self, *args, **kwargs):
            self.entry = kwargs.pop('entry')   # the blog entry instance
            super().__init__(*args, **kwargs)

        def save(self):
            comment = super().save(commit=False)
            comment.entry = self.entry
            comment.save()
            return comment

A classe ``CommentForm`` é instanciada passando a entrada do blog em que o comentário foi escrito,
bem como os dados HTTP POST contendo os campos restantes, como corpo do comentário e e-mail.
O método ``save`` é substituído aqui para definir a entrada de blog associada antes de salvar o comentário.

Vamos rodar os testes novamente:

.. code-block:: bash

    $ python manage.py test blog

::

    Found 17 test(s).
    Creating test database for alias 'default'...
    System check identified no issues (0 silenced).
    F................
    ======================================================================
    FAIL: test_blank_data (blog.tests.CommentFormTest.test_blank_data)
    ----------------------------------------------------------------------
    Traceback (most recent call last):
        ...
    AssertionError: {'name': ['This field is required.'], 'email': ['Thi[55 chars]d.']} != {'name': ['required'], 'email': ['required'], 'body': ['required']}

    ----------------------------------------------------------------------
    Ran 17 tests in 0.112s

    FAILED (failures=1)
    Destroying test database for alias 'default'...

Nosso teste para dados de formulário em branco está falhando porque não estamos
verificando as strings de erro corretas. Vamos corrigir isso e garantir que nossos testes passem:

.. code-block:: bash

    $ python manage.py test blog

::

    Found 17 test(s).
    Creating test database for alias 'default'...
    System check identified no issues (0 silenced).
    .................
    ----------------------------------------------------------------------
    Ran 17 tests in 0.102s

    OK
    Destroying test database for alias 'default'...


Exibindo o formulário de comentários
------------------------------------

Fizemos um formulário para criar comentários, mas ainda não temos como os
visitantes usarem o formulário. O cliente de teste Django não pode testar
envios de formulários, mas o `WebTest`_ pode. Usaremos o `django-webtest`_ para
testar o envio do formulário.

Vamos criar um teste para verificar se um formulário é exibido na
página de detalhes da entrada do blog.

Primeiro precisamos importar a classe ``WebTest`` (em ``blog/tests.py``):

.. code-block:: python

    from django_webtest import WebTest

Agora vamos fazer nossa classe ``EntryViewTest`` herdar de ``WebTest``.
Altere nosso ``EntryViewTest`` para herdar de ``WebTest`` em vez de ``TestCase``:

.. code-block:: python

    class EntryViewTest(WebTest):

.. CAUTION::

    **Não** crie uma nova classe ``EntryViewTest``. Já temos uma classe
    ``EntryViewTest`` com testes nela. Se criarmos uma nova, nossa classe
    antiga será substituída e esses testes não serão mais executados.
    Tudo o que queremos fazer é alterar a classe pai de nosso teste de
    ``TestCase`` para ``WebTest``.

Nossos testes devem continuar passando depois disso porque ``WebTest`` é
uma subclasse da classe Django ``TestCase`` que estávamos usando antes.

Agora vamos adicionar um teste a esta classe:

.. code-block:: python

        def test_view_page(self):
            page = self.app.get(self.entry.get_absolute_url())
            self.assertEqual(len(page.forms), 1)

Agora vamos atualizar nossa view ``EntryDetail`` (em ``blog/views.py``) para herdar ``CreateView``,
para que possamos usá-la para lidar com envios para um ``CommentForm``:

.. code-block:: python

    from django.shortcuts import get_object_or_404
    from django.views.generic import CreateView

    from .forms import CommentForm
    from .models import Entry


    class EntryDetail(CreateView):
        model = Entry
        template_name = 'blog/entry_detail.html'
        form_class = CommentForm

Now if we run our test we'll see 6 failures. Our blog entry detail view
is failing to load the page because we aren't passing an ``entry``
keyword argument to our form:

.. code-block:: bash

    $ python manage.py test
    Found 18 test(s).
    Creating test database for alias 'default'...
    System check identified no issues (0 silenced).
    ........EEEEEE....
    ======================================================================
    ERROR: test_basic_view (blog.tests.EntryViewTest.test_basic_view)
    ----------------------------------------------------------------------
        ...
    KeyError: 'entry'

    ----------------------------------------------------------------------
    Ran 18 tests in 0.323s

    FAILED (errors=6)
    Destroying test database for alias 'default'...


Vamos pegar o ``Entry`` do banco de dados e passá-lo para o nosso formulário.
Precisamos adicionar um método ``get_form_kwargs`` e um método ``get_context_data``
à nossa visão:

.. code-block:: python

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['entry'] = self.get_object()
        return kwargs

    def get_context_data(self, **kwargs):
        d = super().get_context_data(**kwargs)
        d['entry'] = self.get_object()
        return d

Agora, quando executarmos nossos testes, veremos um erro de asserção porque
ainda não adicionamos o formulário de comentário à página de detalhes do blog:

.. code-block:: bash

    $ python manage.py test blog

::

    Found 18 test(s).
    Creating test database for alias 'default'...
    System check identified no issues (0 silenced).
    .............F....
    ======================================================================
    FAIL: test_view_page (blog.tests.EntryViewTest.test_view_page)
    ----------------------------------------------------------------------
    Traceback (most recent call last):
        ...
    AssertionError: 0 != 1

    ----------------------------------------------------------------------
    Ran 18 tests in 0.120s

    FAILED (failures=1)
    Destroying test database for alias 'default'...

Vamos adicionar um formulário de comentário ao final de nosso bloco ``content``
em nosso template de detalhes de entrada de blog (``templates/blog/entry_detail.html``):

.. code-block:: html

        <h5>Add a comment</h5>
        <form method="post">
            {{ form.as_table }}
            <input class="button" type="submit" value="Create Comment">
        </form>

Agora nossos testes passam novamente.

.. code-block:: bash

    $ python manage.py test

::

    Found 18 test(s).
    Creating test database for alias 'default'...
    System check identified no issues (0 silenced).
    ..................
    ----------------------------------------------------------------------
    Ran 18 tests in 0.237s

    OK
    Destroying test database for alias 'default'...

Vamos testar se nosso formulário realmente submete. Devemos escrever dois
testes em nosso ``EntryViewTest``: um para testar erros e outro para testar
um envio de formulário bem-sucedido.

.. code-block:: python

    def test_form_error(self):
        page = self.app.get(self.entry.get_absolute_url())
        page = page.form.submit()
        self.assertContains(page, "This field is required.")

    def test_form_success(self):
        page = self.app.get(self.entry.get_absolute_url())
        page.form['name'] = "Phillip"
        page.form['email'] = "phillip@example.com"
        page.form['body'] = "Test comment body."
        page = page.form.submit()
        self.assertRedirects(page, self.entry.get_absolute_url())

Now let's run our tests:

.. code-block:: bash

    $ python manage.py test blog

::

    Found 20 test(s).
    Creating test database for alias 'default'...
    System check identified no issues (0 silenced).
    ............EE......
    ======================================================================
    ERROR: test_form_error (blog.tests.EntryViewTest.test_form_error)
    ----------------------------------------------------------------------
    Traceback (most recent call last):
        ...
    webtest.app.AppError: Bad response: 403 Forbidden (not 200 OK or 3xx redirect for http://testserver/1/))
        ...

    ======================================================================
    ERROR: test_form_success (blog.tests.EntryViewTest.test_form_success)
    ----------------------------------------------------------------------
    Traceback (most recent call last):
        ...
    webtest.app.AppError: Bad response: 403 Forbidden (not 200 OK or 3xx redirect for http://testserver/1/))
        ...

    ----------------------------------------------------------------------
    Ran 20 tests in 0.202s

    FAILED (errors=2)
    Destroying test database for alias 'default'...

Recebemos um erro HTTP 403 porque esquecemos de adicionar o cross-site
request forgery token entre sites ao nosso formulário. Cada solicitação
HTTP POST feita em nosso site Django precisa incluir um token CSRF.
Vamos alterar nosso formulário para adicionar um campo de token CSRF a ele:

.. code-block:: html

        <form method="post">
            {% csrf_token %}
            {{ form.as_table }}
            <input class="button" type="submit" value="Create Comment">
        </form>

Agora apenas um teste falha:

.. code-block:: bash

    $ python manage.py test blog

::

    Found 20 test(s).
    Creating test database for alias 'default'...
    System check identified no issues (0 silenced).
    .............E......
    ======================================================================
    ERROR: test_form_success (blog.tests.EntryViewTest.test_form_success)
    ----------------------------------------------------------------------
    Traceback (most recent call last):
        ...
    AttributeError: 'Comment' object has no attribute 'get_absolute_url'

    During handling of the above exception, another exception occurred:

    Traceback (most recent call last):
        ...
    django.core.exceptions.ImproperlyConfigured: No URL to redirect to.  Either provide a url or define a get_absolute_url method on the Model.

    ----------------------------------------------------------------------
    Ran 20 tests in 0.225s

    FAILED (errors=1)
    Destroying test database for alias 'default'...

Vamos corrigir isso adicionando um ``get_success_url`` à nossa view, ``EntryDetail``, em ``blog/views.py``:

.. code-block:: python

    def get_success_url(self):
        return self.get_object().get_absolute_url()

Agora nossos testes passam novamente e podemos enviar comentários conforme o esperado.

.. _WebTest: https://pypi.org/project/WebTest/
.. _django-webtest: https://pypi.org/project/django-webtest/
