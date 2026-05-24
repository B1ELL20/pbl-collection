# Fuga do Labirinto - Jogo de Aventura em Terminal Terminal

Este projeto foi desenvolvido como solução para o **Problema 02 do PBL (Problem-Based Learning)** da disciplina **MATA57 - Algoritmos e Programação** na Universidade Estadual de Feira de Santana (UEFS).

## 📌 Declaração de Autoria e Integridade

> ⚠️ **Aviso de Integridade Acadêmica:** 
> Código desenvolvido única e exclusivamente por **Gabriel Dantas Costa Carneiro** sem a utilização indevida de ferramentas de inteligência artificial ou plágio.

*   **Aluno:** Gabriel Dantas Costa Carneiro
*   **Matrícula:** 26111296
*   **Componente Curricular:** MI - Algoritmos
*   **Professora:** Michele Fúlvia Angelo
*   **Instituição:** Universidade Estadual de Feira de Santana (UEFS)

---

## 🎮 Sobre o Jogo

O **Fuga do Labirinto** é um jogo de aventura em tempo real renderizado diretamente no terminal. O mapa do labirinto é gerado de forma totalmente procedural e randômica utilizando **algoritmos recursivos**, garantindo que cada partida seja única. O objetivo principal do jogador é coletar recursos, sobreviver a ameaças e encontrar a chave para abrir o portal de saída antes que o tempo acabe.

### 🧵 Diferencial Técnico: Concorrência e Inputs Assíncronos
Diferente de sistemas de menu tradicionais que travam o terminal esperando um `input()`, este projeto utiliza **Programação Concorrente**:
1.  **Multi-Threading (`threading`):** Um cronômetro decrescente roda em segundo plano em uma Thread paralela, atualizando constantemente o HUD superior de status sem interromper a movimentação.
2.  **Captura Assíncrona de Teclado (`pynput`):** O jogo escuta comandos em tempo real de forma fluida usando as teclas `W`, `A`, `S`, `D`.

---

## 🗺️ Elementos e Ícones do Jogo

O jogo utiliza códigos de escape ANSI e caracteres Unicode especiais para estilizar o terminal:


| Ícone | Representação | Função / Interação |
| :---: | :--- | :--- |
| 🯆 | **Jogador (Verde)** | Personagem principal controlado pelas teclas `W`, `A`, `S`, `D`. |
| ■ | **Parede (Branca/Vermelha)**| Bloqueia a passagem. Se for vermelha, representa a **Porta Trancada**. |
| 🔑 | **Chave (Amarela)** | Item obrigatório para abrir a porta vermelha que protege a saída. |
| ⚔ | **Espada (Azul)** | Utilizada para derrotar monstros pelo caminho. |
| ⛏ | **Pickaxe/Picareta** | Permite quebrar paredes (destruir bloqueios). |
| ✦ | **Moeda (Amarela)** | Tesouros espalhados que somam pontos na pontuação do jogador. |
| 🕷 | **Monstro (Roxo)** | Causa perigo. Reduz `1 Vida` se o jogador não tiver uma espada. |
| ❦ | **Comida (Vermelha)** | Restaura ou adiciona pontos extras de vida. |
| ● | **Saída (Vermelha)** | O destino final do labirinto para vencer a partida. |

---

## ⚙️ Mecânica de Geração Procedural e Zonas

Para garantir uma distribuição justa dos itens, o algoritmo divide o labirinto gerado recursivamente em **três zonas baseadas na distância da largada**:
*   **Zona Perto:** Onde itens utilitários iniciais (como a picareta ou uma espada inicial) têm mais chances de surgir.
*   **Zona Meio:** Área onde a **Chave** é estrategicamente escondida para forçar a exploração.
*   **Zona Restante (Longe):** Onde ficam concentrados os perigos (Monstros), moedas e itens valiosos de sobrevivência.

A dificuldade (tamanho do mapa e quantidade de itens/ameaças) se adapta de acordo com as dimensões selecionadas pelo usuário (Ex: matrizes $15 \times 15$, $19 \times 19$ ou $23 \times 23$).

---

## 🚀 Como Jogar

### Pré-requisitos
O projeto necessita da biblioteca externa `pynput` para capturar os inputs do teclado de forma assíncrona.

Instale a dependência via terminal:
```bash
pip install pynput
```

### Executando o Jogo
1. Certifique-se de executar o jogo em um terminal nativo (como o Prompt de Comando do Windows ou o terminal do Linux) para que os comandos de limpeza de tela (`cls`/`clear`) e caracteres especiais funcionem corretamente.
2. Execute o arquivo do script:
   ```bash
   python main.py
   ```
3. Use as teclas **W, A, S, D** para se movimentar e **ESC** a qualquer momento para desistir e fechar o jogo.