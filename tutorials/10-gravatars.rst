Adicionando Gravatars
=====================

Não seria legal se pudéssemos mostrar os avatares dos usuários ao lado dos comentários?
Vamos usar o serviço gratuito `Gravatar`_ para isso. Como de costume, vamos começar com um teste.

De acordo com a `documentação do Gravatar`_, uma imagem de perfil do Gravatar pode ser solicitada assim:

    http://www.gravatar.com/avatar/HASH

Onde ``HASH`` é um hash MD5 do endereço de e-mail do usuário. Podemos usar o pacote
`hashlib`_ na biblioteca padrão do Python para gerar um hash MD5.

.. TIP::

    Existem muitas opções para exibir gravatars, como definir o tamanho
    de exibição da imagem e ter uma imagem padrão se não houver um Gravatar
    para um e-mail específico.

Primeiro, vamos escrever um teste para Gravatars. Este teste será adicionado
ao nosso teste  ``CommentModelTest`` já existente, pois o plano é adicionar um
método ao modelo ``Comment`` para obter a URL do Gravatar.

.. code-block:: python

    def test_gravatar_url(self):
        comment = Comment(body="My comment body", email="email@example.com")
        expected = "http://www.gravatar.com/avatar/5658ffccee7f0ebfda2b226238b1eb6e"
        self.assertEqual(comment.gravatar_url(), expected)

.. NOTE::

    Não calculamos esses hashes MD5 de cabeça. Você pode usar a
    biblioteca `hashlib`_ do Python para calcular o hash.

Ao executar nossos testes agora, veremos um erro, pois ainda não escrevemos um
método ``gravatar_url()`` para o modelo ``Comment``:

.. code-block:: bash

    $ python manage.py test blog
    Found 27 test(s).
    Creating test database for alias 'default'...
    System check identified no issues (0 silenced).
    ....E......................
    ======================================================================
    ERROR: test_gravatar_url (blog.tests.CommentModelTest.test_gravatar_url)
    ----------------------------------------------------------------------
    Traceback (most recent call last):
        ...
    AttributeError: 'Comment' object has no attribute 'gravatar_url'

    ----------------------------------------------------------------------
    Ran 27 tests in 0.466s

    FAILED (errors=1)
    Destroying test database for alias 'default'...


Adicionando gravatars de comentário
-----------------------------------

Vamos adicionar um método ``gravatar_url()`` em ``Comment`` para que nossos testes passem.
Isso envolve a edição ``models.py``:

.. code-block:: python

    def gravatar_url(self):
        # Get the md5 hash of the email address
        md5 = hashlib.md5(self.email.encode())
        digest = md5.hexdigest()

        return 'http://www.gravatar.com/avatar/{}'.format(digest)

.. NOTE::

    Lembre-se de importar a biblioteca ``hashlib`` no topo do nosso arquivo ``models.py``.

.. TIP::

    Se você nunca usou ``hashlib`` antes, isso pode parecer um pouco assustador.
    MD5_ é uma função hash criptográfica que pega uma string de qualquer tamanho
    e cria uma string binária de 128 bits. Quando processado como hexadecimal,
    é uma string de 32 caracteres..

Se você executar os testes neste ponto, verá que nosso caso de teste passou.


Exibindo gravatars no site
--------------------------

Agora, vamos exibir os Gravatars com os comentários.

Vamos adicionar as imagens do Gravatar em nosso bloco ``content`` em  ``templates/blog/entry_detail.html``:

.. code-block:: html

    {% for comment in entry.comment_set.all %}
        <p>
            <em>Posted by {{ comment.name }}</em>
            <img src="{{ comment.gravatar_url }}" align="left">
        </p>
        {{ comment|linebreaks }}
    {% empty %}
        No comments yet.
    {% endfor %}

Se você iniciar o servidor da Web de desenvolvimento e examinar uma entrada de blog específica,
deverá ver uma imagem para cada comentário.


.. _gravatar: http://gravatar.com/
.. _documentação do Gravatar: http://en.gravatar.com/site/implement/images/
.. _hashlib: https://docs.python.org/3/library/hashlib.html
.. _md5: http://en.wikipedia.org/wiki/MD5
.. _md5 email@example.com: https://duckduckgo.com/?q=md5+email%40example.com
