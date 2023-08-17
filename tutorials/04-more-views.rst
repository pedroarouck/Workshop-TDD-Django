Mais Views
==========

Vamos acrescentar interatividade, os visitantes devem conseguir comentar em cada postagem.

Adicionando um modelo de comentário
-----------------------------------

Primeiro precisamos adicionar um modelo ``Comment`` em ``blog/models.py``.

.. code-block:: python

    class Comment(models.Model):
        entry = models.ForeignKey(Entry, on_delete=models.PROTECT)
        name = models.CharField(max_length=100)
        email = models.EmailField()
        body = models.TextField()
        created_at = models.DateTimeField(auto_now_add=True, editable=False)
        modified_at = models.DateTimeField(auto_now=True, editable=False)


Como adicionamos um novo modelo, também precisamos garantir que esse modelo
seja sincronizado com nosso banco de dados SQLite.

.. code-block:: bash

    $ python manage.py makemigrations
    Migrations for 'blog':
        blog\migrations\0002_alter_entry_options_comment.py
        - Change Meta options on entry
        - Create model Comment
    $ python manage.py migrate
    Operations to perform:
        Apply all migrations: admin, auth, blog, contenttypes, sessions
    Running migrations:
        Applying blog.0002_alter_entry_options_comment... OK


Antes de criarmos um método ``__str__`` para nosso modelo ``Comment``,
semelhante ao que adicionamos anteriormente para nosso modelo ``Entry``, vamos criar um teste em ``blog/tests.py``.

Nosso teste deve ser muito semelhante ao teste ``__str__`` que escrevemos no
``EntryModelTest`` anteriormente.

.. code-block:: python

    class CommentModelTest(TestCase):

        def test_string_representation(self):
            comment = Comment(body="My comment body")
            self.assertEqual(str(comment), "My comment body")

Não esqueça de importar o nosso modelo ``Comment``:

.. code-block:: python

    from .models import Entry, Comment


Agora vamos executar nossos testes para garantir que nosso novo teste falhe:
.. code-block:: bash

    $ python manage.py test blog

::

    Found 11 test(s).
    Creating test database for alias 'default'...
    System check identified no issues (0 silenced).
    F..........
    ======================================================================
    FAIL: test_string_representation (blog.tests.CommentModelTest.test_string_representation)
    ----------------------------------------------------------------------
    Traceback (most recent call last):
        ...
    AssertionError: 'Comment object (None)' != 'My comment body'
    - Comment object (None)
    + My comment body


    ----------------------------------------------------------------------
    Ran 11 tests in 0.075s

    FAILED (failures=1)
    Destroying test database for alias 'default'...


Portanto, parece que nosso teste falhou. Agora devemos implementar o método ``__str__`` para o corpo do comentário.
Depois de implementar o método, execute o teste novamente para vê-lo passar:

.. code-block:: python

    class Comment(models.Model):

        #others methods

        def __str__(self):
            return self.body



.. code-block:: bash

    $ python manage.py test blog

::

    Found 11 test(s).
    Creating test database for alias 'default'...
    System check identified no issues (0 silenced).
    ...........
    ----------------------------------------------------------------------
    Ran 11 tests in 0.076s

    OK
    Destroying test database for alias 'default'..

Adicionando comentários pela interface de administração
-------------------------------------------------------

Vamos adicionar o modelo Comment ao admin assim como fizemos com o modelo Entry.
Isso envolve a edição ``blog/admin.py`` para ficar assim:

.. code-block:: python

    from django.contrib import admin

    from .models import Entry, Comment


    admin.site.register(Entry)
    admin.site.register(Comment)

Se você iniciar o servidor de desenvolvimento novamente, verá o model Comment na
interface de administração e poderá adicionar comentários às entradas do blog.
No entanto, o objetivo de um blog é permitir que outros usuários e não apenas o
administrador publiquem comentários.


Exibição de comentários no site
--------------------------------

Agora podemos criar comentários na interface de administração, mas ainda não podemos vê-los no site. Vamos exibir comentários na página de detalhes para cada entrada de blog.

Vamos começar com os testes. Podemos adicionar um teste para garantir que os comentários apareçam na página de entrada do blog e um teste para garantir que a mensagem “No comments yet” seja exibida apropriadamente. Esses testes devem ser adicionados à nossa classe EntryViewTest.

.. code-block:: python

    def test_comment_list(self):
        Comment.objects.create(
            entry=self.entry,
            name="Phillip",
            email="phillip@example.com",
            body="Test comment body.",
        )
        response = self.client.get(self.entry.get_absolute_url())
        self.assertContains(response, "Posted by Phillip")
        self.assertContains(response, "Test comment body.")
        self.assertNotContains(response, "No comments yet.")

    def test_empty_comment_list(self):
        response = self.client.get(self.entry.get_absolute_url())
        self.assertContains(response, "No comments yet.")

Após o elemento ``<hr>`` dentro do nosso bloco de conteúdo, em ``templates/blog/entry_detail.html`` vamos adicionar o seguinte:

.. code-block:: html

    <hr>
    <h4>Comments</h4>
    {% for comment in entry.comment_set.all %}
        <p><em>Posted by {{ comment.name }}</em></p>
        {{ comment|linebreaks }}
    {% empty %}
        No comments yet.
    {% endfor %}

Agora, a gente consegue ver os comentários no nosso website.
