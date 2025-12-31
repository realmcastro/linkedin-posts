# Como criar o executável .exe

Este projeto pode ser convertido em um executável Windows (.exe) usando PyInstaller.

## Pré-requisitos

- Python 3.8 ou superior instalado
- Pip (geralmente já vem com Python)

## Método 1: Usando o arquivo .bat (Mais fácil)

1. Dê dois cliques no arquivo `build.bat`
2. Aguarde o processo de build completar (inclui criação automática do ícone)
3. O executável será criado na pasta `dist/` com o ícone personalizado

## Método 2: Usando o terminal

### Passo 1: Instalar as dependências

```bash
pip install -r requirements.txt
```

### Passo 2: Executar o script de build

```bash
python build.py
```

### Passo 3 (opcional): Modo Debug

Se tiver problemas com o .env, use o modo debug para ver os logs:

```bash
python build.py --debug
```

Ou dê dois cliques em `build_debug.bat`

O executável debug (`NewsAPI_Automation_Debug.exe`) mostrará uma janela de console com informações de debug.

## Método 2: Usando o terminal

### Passo 1: Instalar as dependências

```bash
pip install -r requirements.txt
```

### Passo 2: Executar o script de build

```bash
python build.py
```

### Passo 3 (opcional): Usando PyInstaller diretamente

```bash
python -m PyInstaller --name=NewsAPI_Automation --windowed --onefile --add-data=".env;." --hidden-import=PIL._tkinter_finder main.py
```

## Ícone

O build cria automaticamente um ícone personalizado (ícone de jornal com fundo azul LinkedIn) usando o script [`create_icon.py`](create_icon.py:1-55).

Se você quiser usar seu próprio ícone:

1. Crie um arquivo `.ico` e coloque na raiz do projeto
2. Renomeie para `icon.ico`
3. Execute o build novamente

## Após o build

O executável será criado em: `dist/NewsAPI_Automation.exe` com o ícone personalizado.

**IMPORTANTE:** O arquivo `.env` é embutido automaticamente no executável! Não é necessário copiá-lo separadamente.

## Distribuição

Para distribuir o aplicativo, você só precisa incluir:

1. **NewsAPI_Automation.exe** - O executável principal (já contém o .env embutido)

### Pasta final para distribuição:

```
NewsAPI_Automation/
└── NewsAPI_Automation.exe
```

**Nota:** A pasta `images/` será criada automaticamente na primeira execução.

### Sobre o arquivo .env embutido:

- O `.env` é embutido dentro do executável durante o build
- Se você quiser alterar as chaves de API, pode colocar um arquivo `.env` externo na mesma pasta do `.exe` - ele terá prioridade sobre o embutido
- Isso permite distribuir o executável sem precisar do arquivo `.env` separado

## Solução de problemas

### Erro: "FileNotFoundError" ou "O sistema não pode encontrar o arquivo especificado"

Isso significa que o PyInstaller não está instalado. Execute:

```bash
pip install pyinstaller
```

Ou instale todas as dependências:

```bash
pip install -r requirements.txt
```

### Erro: "ModuleNotFoundError"

Se aparecer erro de módulo não encontrado, adicione o módulo ao comando usando `--hidden-import`:

```bash
python -m PyInstaller --name=NewsAPI_Automation --windowed --onefile --hidden-import=nome_do_modulo main.py
```

### Erro com imagens PIL

Se as imagens não carregarem no .exe, certifique-se de incluir:

```bash
--hidden-import=PIL._tkinter_finder
```

### Antivírus bloqueando

Alguns antivírus podem bloquear executáveis PyInstaller. Se isso acontecer:

- Adicione o .exe à lista de exceções do antivírus
- Ou assine digitalmente o executável

## Tamanho do executável

O executável terá aproximadamente 50-100 MB devido ao Python e todas as dependências serem incluídas.

## Opções do PyInstaller

| Opção              | Descrição                                                       |
| ------------------ | --------------------------------------------------------------- |
| `--windowed`       | Não mostra console (modo GUI)                                   |
| `--onefile`        | Cria um único arquivo .exe                                      |
| `--onedir`         | Cria uma pasta com todos os arquivos (mais rápido para iniciar) |
| `--icon=icone.ico` | Adiciona ícone personalizado ao .exe                            |
