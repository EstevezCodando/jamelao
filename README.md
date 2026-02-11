# jamelao

# Estrutura

- [raiz] Captura de dados
- [tronco] Processamento de dados
- [ramos] CRUD
- [folha] Interface grafica

# Captura de dados

Esse componente deve pegar dados os sites e armazenar esses dados, ainda brutos, em um storage de facil acesso.

python + requests + beutifulsoup -> salvar um arquivo de texto (talvez HTML, talvez JSON)

## Exemplo

- https://remoteok.com/remote-engineer-jobs
- https://es.indeed.com/jobs?q=software+engineer&l=Barcelona%2C+Barcelona+provincia&radius=25&from=searchOnDesktopSerp%2Cwhereautocomplete&vjk=67e66f13e443843e

Principais campos:

- Titulo
- Empresa
- Link contato
- Subtitulo
- Descrição
- tags
- localidade
- modalidade (remoto/presencial)
- data da publicação

Metadados

- Data da coleta

# Processamento de dados

Não deve se conectar em sites. Deve pegar os dados capturados, conciliar com os dados existentes, e inserir na aplicação
final

# CRUD

Terá uma API REST para que o processador insira os dados

# Interface grafica

E tera uma interface grafica (SPA + REST), para navegar nos dados.
