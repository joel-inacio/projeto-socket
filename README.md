# Trabalho - Programação Socket (Smart Home)

Aplicação cliente/servidor em Python (socket TCP) para controlar dispositivos de uma casa inteligente.

Autores: Joel Inácio e João Victor Justino

## Arquivos
- `servidor.py` – servidor central (multithread)
- `cliente_lampada.py`, `cliente_tomada.py`, `cliente_presenca.py`, `cliente_ar.py`, `cliente_termometro.py` – um cliente para cada tipo de dispositivo
- `consumo.txt` – arquivo de registro do consumo (criado automaticamente pelo servidor)

## Como executar
Precisa apenas do Python 3. Abra um terminal para cada programa, na pasta do trabalho:

```
python servidor.py            # sempre primeiro
python cliente_lampada.py
python cliente_ar.py
python cliente_tomada.py
python cliente_presenca.py
python cliente_termometro.py
```

Para ver o registro de consumo: abra o arquivo `consumo.txt` (ou use `cat consumo.txt` / `type consumo.txt`).
