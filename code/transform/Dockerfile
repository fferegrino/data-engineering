FROM python:3.11-alpine

RUN pip install setuptools --upgrade

RUN pip install dbt-core==1.9.3 dbt-postgres==1.9.0

WORKDIR /dbt

COPY ./project/ /dbt

RUN dbt deps

CMD ["dbt", "run"]
