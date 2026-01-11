# 💅 Julia Ellen Nails - Website & CMS

Sistema de gerenciamento de portfólio e site institucional para o estúdio [**Julia Ellen Nails**](https://julianails.com.br). 
Desenvolvido em **Django**, o projeto funciona como um CMS (Content Management System) personalizado, permitindo a gestão fácil de serviços, horários e galeria de fotos.

## 🚀 Funcionalidades

- **Gerenciamento de Site (Singleton):** Configure telefone, WhatsApp, endereço e textos "Sobre" via painel administrativo sem tocar no código.
- **Catálogo de Serviços:** Adicione, edite e remova serviços, definindo preços, promoções e destaques.
- **Portfólio Dinâmico:** Upload de fotos de trabalhos realizados.
- **Configuração de Agenda:** Exibição dos horários de funcionamento.
- **Painel Administrativo:** Interface completa do Django Admin customizada.

## 🛠️ Tecnologias Utilizadas

- **Python** 3.12+
- **Django** 5.x
- **UV** (Gerenciador de pacotes e projetos)
- **Pytest** (Suíte de testes automatizados)
- **SQLite** (Desenvolvimento) / **PostgreSQL** (Produção - *Sugerido*)
- **HTML5 / TailwindCSS / VanillaJS** (Frontend)

---

## ⚙️ Instalação e Configuração

Este projeto utiliza o [uv](https://github.com/astral-sh/uv) para gerenciamento de dependências. Certifique-se de tê-lo instalado.

### 1. Clone o repositório
```bash
git clone [https://github.com/matheusbraga-dev/julianails.git](https://github.com/matheusbraga-dev/julianails.git)
cd julianails
```

### 2. Instale as dependências
O uv criará o ambiente virtual e instalará tudo automaticamente.

```bash
uv sync
```

### 3. Configuração do Ambiente (.env)
Crie um arquivo .env na raiz do projeto baseado no .env.example e defina as variáveis:

```ini
DEBUG=True
SECRET_KEY='sua-chave-secreta-aqui'
ALLOWED_HOSTS=127.0.0.1,localhost
```

### 4. Configuração do Banco de Dados
Aplique as migrações para criar as tabelas:

```bash
uv run python manage.py migrate
```

### 5. Criar Superusuário
Crie um acesso para entrar no painel administrativo:

```bash
uv run python manage.py createsuperuser
```

---

## 🎨 Frontend e TailwindCSS
O projeto utiliza TailwindCSS v4 compilado via CLI, sem uso de CDN em produção.

### 1. Estrutura de CSS
O arquivo de entrada do Tailwind fica em:

```bash
core/templates/static/css/input.css
```
Com o seguinte cabeçalho:

```css
@config "../../../../tailwind.config.js";
@import "tailwindcss";
```

O caminho em @config é relativo ao próprio input.css e garante que o Tailwind v4 carregue o arquivo tailwind.config.js, 
já que ele não é detectado automaticamente nessa versão.

O CSS gerado é salvo em:

```bash
core/templates/static/css/output.css
```

E é incluído nos templates Django via:

```html
{% load static %}
<link rel="stylesheet" href="{% static 'css/output.css' %}">
```

### 2. Scripts de build
As dependências de frontend estão definidas em package.json:

```json
{
  "dependencies": {
    "@tailwindcss/cli": "^4.1.18",
    "tailwindcss": "^4.1.18"
  },
  "scripts": {
    "dev": "npx @tailwindcss/cli -i ./core/templates/static/css/input.css -o ./core/templates/static/css/output.css --watch",
    "build": "npx @tailwindcss/cli -i ./core/templates/static/css/input.css -o ./core/templates/static/css/output.css --minify"
  }
}
```

Para ambiente de desenvolvimento (recompila a cada alteração):

```bash
npm install
npm run dev
```

Para build de produção:

```bash
npm run build
```

Após o build, basta coletar os arquivos estáticos com Django (collectstatic) e servir o output.css via a infraestrutura de estáticos do projeto.

---

## 🧪 Testes Automatizados
O projeto possui uma cobertura de testes unitários garantindo a integridade dos Models e Views principais.

Para rodar todos os testes:

```bash
uv run pytest
```
Para rodar testes com saída detalhada:

```bash
uv run pytest -v
```

---

## ▶️ Executando o Projeto
Para iniciar o servidor de desenvolvimento:

```bash
uv run python manage.py runserver
```
Acesse em seu navegador:

Site: http://127.0.0.1:8000/

Admin: http://127.0.0.1:8000/admin/

---

## 📂 Estrutura Principal
core/: Configurações principais do projeto (settings, urls).

portfolio/:

models.py: Regras de negócio (BusinessConfig, Service, PortfolioItem).

views.py: Lógica de apresentação.

tests/: Testes automatizados separados por contexto.

---

## 📄 Licença
Este projeto é de uso privado para Julia Ellen Nails.
