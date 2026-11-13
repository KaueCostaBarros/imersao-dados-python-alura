# Dashboard Interativo de Análise de Dados

Dashboard interativo desenvolvido durante a Imersão de Dados com Python da Alura, para explorar e visualizar dados por meio de filtros, gráficos e indicadores. Publicado online com Streamlit.

**[Acesse o projeto](https://imersao-dados-python-alura-kaue.streamlit.app/)**

![Preview do dashboard](https://github.com/user-attachments/assets/56014585-f006-4e90-8728-b3990fab379e)

## Sobre os dados

O dashboard analisa uma base de dados com 133.339 registros salariais de profissionais da área de dados, contemplando diferentes cargos, níveis de experiência, localidades e modalidades de trabalho ao longo dos anos. Desenvolvido em Python com Streamlit, permite comparar salários, identificar os cargos mais frequentes, analisar a distribuição salarial e explorar diferenças de remuneração entre profissionais da área.

## Funcionalidades

- Filtros para explorar as informações
- Gráficos interativos com Plotly
- Indicadores e métricas que se atualizam conforme os filtros
- Tratamento e manipulação dos dados com Pandas
- Interface criada com Streamlit

## Tecnologias

- Python
- Streamlit
- Pandas
- Plotly
- PyCountry

## Estrutura do projeto

```
imersao-dados-python-alura/
├── app.py
├── requirements.txt
├── README.md
├── assets/
│   └── dashboard.png
└── dados/
```

## Como executar

1. Clone o repositório:

```bash
git clone https://github.com/KaueCostaBarros/imersao-dados-python-alura.git
cd imersao-dados-python-alura
```

2. (Opcional) Crie um ambiente virtual:

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

3. Instale as dependências e execute:

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Autor

**Kauê Costa Barros**

- [LinkedIn](https://www.linkedin.com/in/kauebarros/)
- [GitHub](https://github.com/KaueCostaBarros)
