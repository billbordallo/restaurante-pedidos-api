# Pedidos para Restaurantes - API
_versão: 1.0_

Este é um sistema escrito em Python que tem como objetivo agilizar a comunicação entre o salão do restaurante e a cozinha, centralizando os pedidos, seu status e eventuais observações. Dessa forma, todos os envolvidos no atendimento ao público — garçons, gerentes e equipe de cozinha — podem visualizar a qualquer momento os pedidos realizados e seu status.

O sistema permite a inclusão de novos pedidos, exclusão, alteração de status e visualização de todos os pedidos. Também é possível visualizar o menu completo do restaurante.

## Como executar 

Os requisitos para rodar o sistema são ter o **Python** instalado e as libs listadas no arquivo `requirements.txt`.

> É recomendado usar um ambiente virtual para rodar o sistema. Veja aqui como instalar o [virtualenv](https://virtualenv.pypa.io/en/latest/installation.html).

Após clonar o repositório, é necessário ir ao diretório raiz, pelo terminal, para poder executar os comandos descritos abaixo.

```
(env)$ pip install -r requirements.txt
```

Para executar a API  basta executar:

```
(env)$ flask run --host 0.0.0.0 --port 5000
```

Em modo de desenvolvimento é recomendado executar utilizando o parâmetro reload, que reiniciará o servidor
automaticamente após uma mudança no código fonte. 

```
(env)$ flask run --host 0.0.0.0 --port 5000 --reload
```

Abra o [http://localhost:5000/#/](http://localhost:5000/#/) ou [http://127.0.0.1:5000/#/](http://127.0.0.1:5000/#/) no navegador para verificar o status da API em execução.
