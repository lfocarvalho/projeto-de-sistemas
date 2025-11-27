![Logo da Minha Empresa](https://github.com/lfocarvalho/projeto-de-sistemas/blob/main/media/projeto_fotos/petcare%20logo.jpg)
# PetCare

O PetCare é um projeto que visa conectar tutores e o mercado pet, promovendo a acessibilidade à saúde do seu animal. Nesse aplicativo você encontra petshops e veterinários perto de você, com detalhes de fácil acesso, além de informações sobre campanhas de vacinação e tudo de relevante para a saúde do seu pet.

Este projeto foi desenvolvido como parte da disciplina de Projeto de Sistemas da Universidade Federal do Tocantins.

### Imagens do Projeto
![Tela de Login](https://github.com/lfocarvalho/projeto-de-sistemas/blob/main/media/projeto_fotos/tela_login.png)

![tela lojas](https://github.com/lfocarvalho/projeto-de-sistemas/blob/main/media/projeto_fotos/tela_lojas.png)

![Tela de Produtos](https://github.com/lfocarvalho/projeto-de-sistemas/blob/main/media/projeto_fotos/tela_produtos.png)

![Tela de Localizações](https://github.com/lfocarvalho/projeto-de-sistemas/blob/main/media/projeto_fotos/tela_localizacoes.png)

![Tela de Agendamentos](https://github.com/lfocarvalho/projeto-de-sistemas/blob/main/media/projeto_fotos/tela_agendamentos.png)

![Detalhes da Loja](https://github.com/lfocarvalho/projeto-de-sistemas/blob/main/media/projeto_fotos/loja_detalhes.png)

![Detalhes do Produto](https://github.com/lfocarvalho/projeto-de-sistemas/blob/main/media/projeto_fotos/produto_detalhes.png)

![Avaliações](https://github.com/lfocarvalho/projeto-de-sistemas/blob/main/media/projeto_fotos/avaliacao_loja.png)

![Perfil do Usuáro](https://github.com/lfocarvalho/projeto-de-sistemas/blob/main/media/projeto_fotos/tela_perfil_cliente.png)

### Links Rápidos
- [Vídeo Pitch – Liga Jovem](https://youtu.be/bO_F5-_RH-0?si=_H23I241z7CZnpjX)
- [Landing Page](https://petcarepage.netlify.app/)

## Funcionalidades Implementadas

* **Gestão de Usuários:**
    * Cadastro completo de novos usuários.
    * Avaliação de lojas e produtos e possibilidade de favoritar.
    * Encontrar lojas perto da sua localização.
    * Login pela conta do Google.

* **Gestão para Lojas:**
    * Registrar sua loja, permitindo que usuários a encontrem e suas informações (endereço, atendimento 24h, etc.).
    * Criação, edição e exclusão de produtos.
    * Visualização de consultas e serviços agendados em um dashboard interativo.
    * Visualizar avaliação de usuários à loja e produtos

* **Dashboard Interativo:**
    * Pesquisar e filtrar lojas.
    * Mapa com lojas cadastradas.

* **Administração:**
    * Painel de administrador para visualização de todos as lojas e produtos cadastrados no sistema, com possibilidade de alterar e deletar, além de criar novas categorias de produtos.


## Como Instalar e Executar o Projeto

1.  **Pré-requisitos:**
    * Python 3.10 ou superior.
    * Git.

2.  **Clone o repositório:**
    ```bash
    git clone [https://github.com/lfocarvalho/projeto-de-sistemas.git](https://github.com/lfocarvalho/projeto-de-sistemas.git)
    cd projeto-de-sistemas
    ```

3.  **Crie e ative o seu ambiente virtual :**
   Recomenda-se o uso de um ambiente virtual para gerenciar as dependências do projeto.
   * No Windows:
   ```bash
   python -m venv venv
   .\venv\Scripts\activate
   ````
   * No Linux/macOS:
```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

4.  **Instale as dependências:**
    Com o ambiente virtual ativo, instale o Bootstrap e Allauth.
   ```bash
   pip install django-bootstrap-v5
   ```
   ```bash
   pip install django-allauth
   pip install --upgrade PyJWTD
   pip install django-environ
   pip install jwt
   pip install requests
   ```

5.  **Configure o banco de dados:**
    Aplique as migrações para criar as tabelas necessárias no banco de dados.
   ```bash
   python manage.py migrate
   ```

6.  **Execute o servidor:**
   ```bash
   python manage.py runserver
   ```

7.  **Acesse a aplicação:**
   Abra o seu navegador e acesse o endereço indicado no terminal (geralmente a porta 8000):
  * URL: `http://127.0.0.1:8000/`

---


## Informações Acadêmicas

* **Universidade:** Universidade Federal do Tocantins
* **Curso:** Ciência da Computação
* **Disciplina:** Projeto de Sistemas - 2025.2
* **Professor:** Edeilson Milhomem da Silva

### Equipe

| Nome                              | Github                                           |
| --------------------------------- | ------------------------------------------------ |
| Isabela Barros de Oliveira       | [@isabelabarros-o](https://github.com/isabelabarros-o) |
| Luiz Fernando de Oliveira Carvalho | [@Lfocarvalho](https://github.com/lfocarvalho) |
| Mateus Leopoldo Santiago da Silva | [@MateusLeopoldo](https://github.com/MateusLeopoldo) |
| Natália Morais Nerys             | [@natalia-nerys](https://github.com/natalia-nerys)     |
| Ranor Victor dos Santos Araújo   | [@ranorvictor](https://github.com/ranorvictor)     |

[Link para o repositório do projeto](https://github.com/lfocarvalho/projeto-de-sistemas)
