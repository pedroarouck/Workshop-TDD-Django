URLs legíveis
=============

Nossa estrutura de URL atual não nos diz muito sobre as entradas do blog,
então vamos adicionar informações de data e título para ajudar os usuários e
também os mecanismos de pesquisa a identificar melhor a entrada.

Para isso, vamos usar o esquema de URL:
``/year/month/day/pk-slug/``

Slug é um termo cunhado pela indústria jornalística para um pequeno identificador de um artigo de jornal.
No nosso caso, usaremos o método slugify_ do Django para converter nosso título de texto em uma versão slugificada.
Por exemplo, "Este é um título de teste" seria convertido em letras minúsculas com espaços substituídos por hífens,
resultando em “este é um título de teste” e o URL completo pode ser "/2014/03/15/6-este-e-um-titulo-de-teste/".

.. _slugify: https://docs.djangoproject.com/en/4.2/ref/utils/#django.utils.text.slugify


Primeiro, vamos atualizar nosso modelo para lidar com o novo campo slug.


Modelo
------

Em nosso modelo ``Entry``, precisamos criar ou atualizar automaticamente
o slug da entrada após salvá-la. Primeiro, vamos adicionar o campo slug
ao nosso modelo ``Entry``. Adicione isto após a declaração de campo ``modified_at``:

.. code-block:: python

    slug = models.SlugField(default='')


Em seguida, atualizamos a função salvar. Importamos o método slugify na parte superior do arquivo:

.. code-block:: python

    from django.template.defaultfilters import slugify

Agora crie um método save em nosso modelo ``Entry`` que slugifica o título ao salvar:

.. code-block:: python

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)


Depois disso, atualizaremos nosso método ``get_absolute_url()`` para fazer um reverse
da nova URL usando nossos novos parâmetros de ano, mês, dia e slug:

.. code-block:: python

    def get_absolute_url(self):
        kwargs = {'year': self.created_at.year,
                  'month': self.created_at.month,
                  'day': self.created_at.day,
                  'slug': self.slug,
                  'pk': self.pk}
        return reverse('entry_detail', kwargs=kwargs)

Agora temos que migrar o banco de dados, pois alteramos o modelo.
Execute o comando para migrar seu banco de dados. Primeiro, criamos a nova migração
(supondo que você tenha terminado o tutorial anterior onde criou sua migração inicial):

.. code-block:: bash

    $ python manage.py makemigrations blog

Em seguida, executamos a nova migração que acabamos de criar:

.. code-block:: bash

    $ python manage.py migrate blog


Escrever o Teste
----------------

O primeiro passo é definir nosso teste para o título. Para isso, iremos:

#) Criar uma nova entrada de blog
#) Encontrar o slug para a entrada do blog
#) Executar uma solicitação HTTP GET para o novo URL ``/year/month/day/pk-slug/`` para a entrada do blog
#) Verificar se a solicitação foi bem-sucedida com um código 200

Primeiro precisamos importar o pacote Python ``datetime`` e a função ``slugify`` para nosso arquivo de testes:

.. code-block:: python

    from django.template.defaultfilters import slugify
    import datetime

Agora vamos escrever nosso teste na classe ``EntryViewTest``:

.. code-block:: python

    def test_url(self):
        title = "This is my test title"
        today = datetime.date.today()
        entry = Entry.objects.create(title=title, body="body", author=self.user)
        slug = slugify(title)
        url = "/{year}/{month}/{day}/{pk}-{slug}/".format(
            year=today.year,
            month=today.month,
            day=today.day,
            slug=slug,
            pk=entry.pk,
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='blog/entry_detail.html')

Tente executar os testes novamente e você verá algumas falhas:

.. code-block:: bash

    $ python manage.py test blog


Padrão de URL
-------------

Em seguida, vamos alterar nosso arquivo ``blog/urls.py``. Substitua seu código por este:

.. code-block:: python

    from django.urls import path


    from . import views

    urlpatterns = [
    path('<int:year>/<int:month>/<int:day>/<int:pk>-<slug:slug>/', views.EntryDetail.as_view(), name='entry_detail'),
    ]

Agora salve o arquivo e tente executar os testes novamente. Você deve ver todos os testes passando.

.. IMPORTANT::

    As entradas anteriores à mudança de padrão de URL pode causar com que
    o site não suba por não terem os parametros necessários para montar a nova URL.
    Nesse caso, entre na ``interface de adminstração``, exclua as entradas antigas e
    crie novas entradas.

Outro Teste
------------

O que aconteceria se mudássemos o slug ou uma data inválida fosse fornecida na URL?
Isso não deveria importar, porque verificamos apenas o modelo ``pk``.

Vamos escrever mais alguns testes para este caso para garantir que a
página correta seja exibida neste caso e para quando o id não existir.
Nossos testes devem ficar assim:

.. code-block:: python

    def test_misdated_url(self):
        entry = Entry.objects.create(
            title="title", body="body", author=self.user)
        url = "/0000/00/00/{0}-misdated/".format(entry.id)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, template_name='blog/entry_detail.html')

    def test_invalid_url(self):
        entry = Entry.objects.create(
            title="title", body="body", author=self.user)
        response = self.client.get("/0000/00/00/0-invalid/")
        self.assertEqual(response.status_code, 404)

Agora vamos executar nossos testes e garantir que eles ainda sejam aprovados.


.. TIP::

    Se você tentar adicionar uma entrada no admin, notará que deve escrever um slug
    (não é opcional), mas o que quer que você escreva será substituído no
    método ``Entry.save()``. Existem algumas maneiras de resolver isso,
    mas uma maneira é definir o ``SlugField`` em nosso modelo ``Entry`` para
    ``editable=False`` e ocultá-lo no administrador ou em outros formulários:

    .. code-block:: python

        slug = SlugField(editable=False)

    Consulte os documentos do Django em editáveis_ para obter detalhes.

    .. _editáveis: https://docs.djangoproject.com/en/4.2/ref/models/fields/#editable
