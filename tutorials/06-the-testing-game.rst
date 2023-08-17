O jogo dos Testes
=================


Cobertura de testes
-------------------

É importante testar todo o seu código. A cobertura de código é freqüentemente
usada como uma medida para o sucesso de um desenvolvedor na criação de testes
de qualidade. A regra básica é que testes abrangentes devem executar cada linha de código.

`Coverage`_, uma ferramenta que mede a cobertura do código Python, será
usada para verificar qual porcentagem do código do tutorial está sendo testada.

Installing Coverage
------------------

Primeiro, vamos instalar o coverage

.. code-block:: bash

    $ pip install coverage

Antes de continuarmos, precisamos lembrar de adicionar essa nova dependência
ao nosso arquivo ``requirements.txt``. Vamos usar  ``pip freeze`` para descobrir a
versão do ``coverage`` que instalamos.

.. code-block:: bash

    $ pip freeze
    Django==4.2.4
    WebOb==1.8.7
    WebTest==3.0.0
    beautifulsoup4==4.12.2
    coverage==7.2.7
    django-webtest==1.9.10
    six==1.16.0
    sqlparse==0.4.4
    waitress==2.1.2

Agora vamos adicionar ``coverage`` ao nosso arquivo ``requirements.txt``.

    coverage==7.2.7
    Django==4.2.4
    WebTest==3.0.0
    django-webtest==1.9.10

Usando o Coverage
------------------

Agora vamos rodar nossos testes. À medida que executamos nossos testes na linha de comando,
``coverage`` registra e cria um relatório de cobertura:

.. code-block:: bash

    $ coverage run --include='./*' manage.py test
    Found 20 test(s).
    Creating test database for alias 'default'...
    System check identified no issues (0 silenced).
    ....................
    ----------------------------------------------------------------------
    Ran 20 tests in 0.412s

    OK
    Destroying test database for alias 'default'...

Vamos dar uma olhada em nosso relatório de cobertura de código:

.. code-block:: bash

    $ coverage report

    Name                                                  Stmts   Miss  Cover
    -------------------------------------------------------------------------
    blog\__init__.py                                          0      0   100%
    blog\admin.py                                             4      0   100%
    blog\apps.py                                              4      0   100%
    blog\forms.py                                            14      0   100%
    blog\migrations\0001_initial.py                           7      0   100%
    blog\migrations\0002_alter_entry_options_comment.py       5      0   100%
    blog\migrations\__init__.py                               0      0   100%
    blog\models.py                                           23      0   100%
    blog\tests.py                                            98      0   100%
    blog\urls.py                                              3      0   100%
    blog\views.py                                            18      0   100%
    manage.py                                                12      2    83%
    myblog\__init__.py                                        0      0   100%
    myblog\settings.py                                       19      0   100%
    myblog\urls.py                                            5      0   100%
    myblog\views.py                                           5      0   100%
    -------------------------------------------------------------------------
    TOTAL                                                   217      2    99%


Vamos dar uma olhada no relatório de cobertura. À esquerda, o relatório
mostra o nome do arquivo que está sendo testado. ``Stmts``, ou code statements,
indicam o número de linhas de código que podem ser testadas. ``Miss``, ou Missed lines,
indica o número de linhas que não são executadas pelos testes de unidade. ``Cover``,
ou Coverage, é a porcentagem de código coberta pelos testes atuais
(equivalente a ``(Stmts - Miss)/Stmts``). Por exemplo, ``myblog/views`` tem 18 declarações
de código que podem ser testadas. Vemos que nossos testes deixaram de testar
duas declarações para um código Cobertura de 99%.

.. IMPORTANT::

    Observe que a cobertura de código pode apenas indicar que você esqueceu os testes;
    não lhe dirá se seus testes são bons. Não use uma boa cobertura de código como
    desculpa para escrever testes de qualidade inferior.


Relatório de Cobertura HTML
---------------------------

Nossos relatórios de cobertura em linha de comando atuais são úteis,
mas não são muito detalhados. Felizmente, a coverage inclui um recurso
para gerar relatórios de cobertura HTML que demonstram visualmente a
cobertura colorindo nosso código com base nos resultados.

Vamos embelezar o relatório de cobertura acima em formato HTML executando o seguinte comando:

.. code-block:: bash

    $ coverage html

Este comando criará um diretório ``htmlcov`` contendo nossa cobertura de teste.
O ``index.html`` é o arquivo de visão geral que se vincula aos outros arquivos.
Vamos abrir nosso ``htmlcov/index.html`` em nosso navegador da web.


Cobertura das branchs
---------------------

Até agora, testamos a cobertura de instrução para garantir a execução de
cada linha de código durante nossos testes. Podemos fazer melhor garantindo que
todas as ramificações do código sejam tomadas. A documentação de cobertura contém
uma boa descrição da `cobertura de branch`_.

A partir de agora, adicionaremos o argumento ``--branch`` quando registrarmos a cobertura do código.
Vamos experimentá-lo em nossos testes:

.. code-block:: bash

    $ coverage run --include='./*' --branch manage.py test
    $ coverage report
    Name                                                  Stmts   Miss Branch BrPart  Cover
    ---------------------------------------------------------------------------------------
    blog\__init__.py                                          0      0      0      0   100%
    blog\admin.py                                             4      0      0      0   100%
    blog\apps.py                                              4      0      0      0   100%
    blog\forms.py                                            14      0      0      0   100%
    blog\migrations\0001_initial.py                           7      0      0      0   100%
    blog\migrations\0002_alter_entry_options_comment.py       5      0      0      0   100%
    blog\migrations\__init__.py                               0      0      0      0   100%
    blog\models.py                                           23      0      0      0   100%
    blog\tests.py                                            98      0      2      0   100%
    blog\urls.py                                              3      0      0      0   100%
    blog\views.py                                            18      0      0      0   100%
    manage.py                                                12      2      2      1    79%
    myblog\__init__.py                                        0      0      0      0   100%
    myblog\settings.py                                       19      0      0      0   100%
    myblog\urls.py                                            5      0      0      0   100%
    myblog\views.py                                           5      0      0      0   100%
    ---------------------------------------------------------------------------------------
    TOTAL                                                   217      2      4      1    99%

Observe as novas colunas ``Branch`` e ``BrPart`` e observe que está faltando
uma ramificação em nosso arquivo ``manage.py``. Vamos dar uma olhada nisso mais tarde.


Configuração do Coverage
------------------------

A Coverage nos permite especificar um arquivo de configuração (arquivos ``.coveragerc``)
para especificar os atributos de cobertura padrão. A documentação explica como o `.coveragerc`_ funciona.

Vamos adicionar um arquivo ``.coveragerc`` ao nosso projeto que se parece com este::

    [run]
    include = ./*
    branch = True

Agora podemos executar a cobertura sem nenhum argumento extra:

.. code-block:: bash

    $ coverage run manage.py test


.. _coverage: https://coverage.readthedocs.io/en/stable/
.. _cobertura de branch: https://coverage.readthedocs.io/en/stable/branch.html
.. _.coveragerc: https://coverage.readthedocs.io/en/stable/config.html
