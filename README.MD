# Limpador de Downloads

Aplicativo desenvolvido em Python para organizar arquivos, analisar o espaço ocupado e facilitar a limpeza da pasta Downloads no Windows 11.

## Sobre o projeto

O **Limpador de Downloads** surgiu de uma necessidade do meu ambiente de trabalho.

No meu dia a dia, trabalho com a geração de comprovantes que podem conter documentos e informações pessoais. Por esse motivo, percebi a importância de manter a pasta Downloads organizada e evitar o acúmulo desnecessário de arquivos que possam conter dados sensíveis.

A partir dessa necessidade, decidi desenvolver uma ferramenta própria para automatizar a organização dos arquivos e facilitar a identificação de documentos antigos, contribuindo para uma rotina mais segura e eficiente.

O projeto também representa uma oportunidade de colocar em prática meus conhecimentos em Python, evoluindo de um programa executado pelo terminal para uma aplicação com interface gráfica.

## Objetivos

- Manter a pasta Downloads organizada automaticamente.
- Facilitar a identificação e a localização de arquivos.
- Identificar documentos antigos que podem ser revisados e removidos.
- Reduzir o acúmulo de arquivos com informações pessoais.
- Aplicar boas práticas de programação para resolver um problema real.

## Funcionalidades

- **Listagem de arquivos:** visualização de nomes, categorias, tamanhos e datas de modificação.
- **Organização automática:** separação dos arquivos em pastas conforme suas extensões, como Documentos, Imagens, Vídeos, Áudios, Compactados, Instaladores e Código.
- **Busca por extensão:** localização de arquivos específicos, incluindo os presentes em subpastas.
- **Análise de espaço:** consulta do espaço ocupado pelos arquivos, agrupados por categoria.
- **Limpeza de arquivos antigos:** identificação de arquivos cuja última modificação ocorreu há mais de sete dias, com possibilidade de enviá-los para a Lixeira do Windows.
- **Interface gráfica:** navegação por janelas e menus, sem depender do terminal durante o uso normal.

## Privacidade e LGPD

A preocupação com a privacidade e a proteção de dados pessoais é um dos principais motivos para o desenvolvimento deste projeto.

Como parte da minha rotina envolve a geração de comprovantes que podem conter documentação pessoal, manter esses arquivos organizados e evitar seu armazenamento desnecessário é uma medida importante de cuidado com as informações.

O aplicativo foi pensado para facilitar essa rotina, ajudando a identificar arquivos antigos e a manter a pasta Downloads organizada.

A ferramenta é um recurso auxiliar de organização e **não garante, isoladamente, a conformidade com a Lei Geral de Proteção de Dados (LGPD)**. A utilização adequada também depende das políticas da organização, dos prazos de retenção aplicáveis e dos procedimentos de segurança adotados.

## 🛠️ Tecnologias utilizadas

- **Python:** linguagem principal do projeto.
- **Tkinter:** desenvolvimento da interface gráfica.
- **Pathlib:** manipulação de caminhos e arquivos.
- **Shutil:** movimentação e organização dos arquivos.
- **Send2Trash:** envio de arquivos para a Lixeira do sistema operacional.
- **PyInstaller:** geração do executável para Windows.

## Evolução do projeto

O desenvolvimento começou com uma aplicação simples executada pelo terminal, com um menu de opções para realizar as operações principais.

Conforme as funcionalidades foram implementadas e testadas, o projeto evoluiu para uma aplicação com interface gráfica, tornando a utilização mais prática e acessível no dia a dia.

Essa evolução permitiu aplicar conceitos de Python, manipulação do sistema de arquivos, tratamento de erros, automação de tarefas e desenvolvimento de interfaces gráficas em uma solução voltada a uma necessidade real.

## Aprendizados

Durante o desenvolvimento, foram praticados conceitos como:

- Funções, estruturas condicionais e laços de repetição.
- Dicionários, conjuntos e listas.
- Manipulação de arquivos e diretórios.
- Organização e classificação por extensão.
- Tratamento de exceções.
- Desenvolvimento de interfaces com Tkinter.
- Empacotamento de aplicações com PyInstaller.

## Melhorias futuras

- Salvar as configurações do usuário entre execuções.
- Permitir personalizar as categorias e extensões.
- Implementar histórico de movimentações e opção de desfazer.
- Aprimorar a interface e a experiência de uso.
- Automatizar verificações periódicas da pasta Downloads.

---

**Projeto pessoal desenvolvido em Python com foco em automação, organização de arquivos, aprendizado prático e cuidado com a privacidade dos dados.**
