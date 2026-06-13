# API de Produtos

## Subindo os bancos

```bash
docker-compose up -d
```

Verificar containers:

```bash
docker ps
```

---

## Executar testes

```bash
pytest -v
```

ou

```bash
pytest --cov=main -v
```

---

## Saída esperada

```text
=====================
12 passed, 1 warning in 0.53s
=====================
```

---

## Isolamento dos testes

A fixture client cria as tabelas antes de cada teste utilizando:

Base.metadata.create_all()

e remove tudo após o teste utilizando:

Base.metadata.drop_all()

Isso garante que nenhum teste dependa do estado deixado por outro teste.