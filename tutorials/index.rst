Workshop: Test-Driven Web Development with Django
=================================================

Este material faz parte do workshop `San Diego Python <http://pythonsd.org/>`_ sobre testes orientados a
desenvolvimento com o framework web `Django <https://www.djangoproject.com/>`_. Neste workshop de um dia,
você aprenderá a construir um site bem testado e baseado em Django.

Este workshop foi possível graças a uma doação da `Python Software Foundation <http://python.org/psf/>`_
`Comitê de Extensão e Educação <https://www.python.org/psf/workgroups/#outreach-education-work-group>`_.


Por que desenvolvimento orientado a testes?
-------------------------------------------

Ao criar um novo aplicativo, a princípio você pode não precisar de testes. Os testes
podem ser difíceis de escrever no início e levam tempo, mas podem salvar uma
enorme quantidade de tempo de solução manual de problemas.

À medida que seu aplicativo cresce, fica mais difícil crescer e refatorar
seu código. Há sempre o risco de que uma mudança em uma parte do seu
aplicação irá quebrar outra parte. Uma boa coleção de testes automatizados que
acompanha um aplicativo pode verificar se as alterações feitas em uma parte do
o software não quebra outro.


Prerequisites
-------------

* `Python <http://www.python.org/download/>`_ 3 (3.11 is recommended)
* `Install Django <https://www.djangoproject.com/download/>`_ 4.2
* `Django tutorials <https://docs.djangoproject.com/en/4.2/intro/tutorial01/>`_

Você não precisa ser um especialista em Django para participar deste workshop ou encontrar este
documento útil. No entanto, o objetivo de obter um site funcional com testes em
um único dia é grandioso e por isso pedimos que os participantes venham com Python
e Django instalado. Nós também encorajamos as pessoas a passarem pelo Django
tutoriais de antemão, a fim de tirar o máximo proveito do workshop.


O Projeto: construindo um blog
------------------------------

O rito de passagem para a maioria dos desenvolvedores da web é seu próprio sistema de blog.
Existem centenas de soluções por aí. As características e requisitos são
geralmente bem compreendida. Escrever um com TDD torna-se uma espécie de `code kata
<http://codekata.com/>`_ que pode ajudá-lo a trabalhar com todos os tipos de
aspectos do framework Django.


Conteúdo
--------

.. toctree::
   :maxdepth: 2

   01-getting-started
   02-models
   03-views
   04-more-views
   05-forms
   06-the-testing-game
   07-templatetags
   08-migrations
   09-readable-urls
   10-gravatars


Obtendo ajuda e contribuindo
----------------------------

Arquivos de origem Markdown e exemplos de código de trabalho para esses tutoriais podem ser
encontrado no `Github <https://github.com/pythonsd/test-driven-django-development>`_.
Se você encontrou um bug ou tem uma sugestão para melhorar ou estender os tutoriais,
por favor, abra um issue ou um pull request.

Esses tutoriais são fornecidos sob uma licença Creative Commons (CC BY-SA 3.0).
