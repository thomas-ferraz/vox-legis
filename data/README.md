# MAC6967-G6-NLP-juridico

Aqui estão os procedimentos para coleta de estatísticas dos datasets - número de arquivos, tamanho - e o processamento dos dados.

## Datasets
| Dataset                     | Número de arquivos | Tamanho   |
| --------------------------- |:------------------:| ---------:|
| Dataset 1 - Falências       | 5589               | 174.83 MB |
| Dataset 1 - Rec. Judiciais  | 2896               | 182.00 MB |
| Dataset 2 - Falências       | 12.917             | 121.77 GB |

## Requerimentos

Devido ao tamanho dos datasets e aproveitando o fato dos mesmos estarem no Google Drive da USP, o processamento está sendo feito na plataforma [Google Colaboratory](https://colab.research.google.com/) conhecida como Google Colab. Nela é fornecido acesso a um notebook Python e um host do Google, com acesso a arquivos no Drive. A partir de qualquer notebook do Colab é possível conectar ao Google Drive com o código:

```python
from google.colab import drive
drive.mount("/content/drive")
```

E então é possível acessar dados existentes no seu Google Drive, ou em dados compartilhados, desde que exista um atalho para este no seu Drive :

![Atalho no Google Drive](../MAC6967-G6-NLP-juridico/assets/driveshortcut.png)

```python
dataset1f = '/content/drive/My Drive/dataset2'
```

Pode-se acessar diretórios:
```python
%cd '/content/drive/My Drive'
```

Executar comandos git depois de configurar usuário:
```python
!git config user.email '<EMAIL>'
!git config user.name '<USERNAME>'
```

Para clonar o repositório, é necessário gerar um [token de acesso pessoal](https://docs.gitlab.com/ee/user/profile/personal_access_tokens.html) para validar o acesso:
```python
!git clone https://<USERNAME>:<TOKEN>@gitlab.com/thomas-ferraz/MAC6967-G6-NLP-juridico.git
```

Caso seja possível acesso local aos datasets, os notebook podem ser alterados para tal uso.