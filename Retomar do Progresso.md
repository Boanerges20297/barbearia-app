# 📌 Ponto de Retomada: Projeto Agendamento (Flask)

**Data:** [Data de Hoje]
**Status:** ✅ Estrutura Base (Skeleton) Funcionando
**Próxima Fase:** Implementação Lógica das Rotas (Fase 1 e 2)

---

## 1. O que foi Conquistado (A Base Sólida)
Superamos a "Paralisia de Configuração" e os erros de importação circular. A arquitetura atual respeita a **Inversão de Dependência**:

* **`app.py` (O Orquestrador):** Não contém lógica de negócio. Apenas inicializa o Flask, configura o Banco e registra os Blueprints.
* **`routes/` (Os Especialistas):** Estão isolados em Blueprints, sem depender diretamente da instância global `app`.
* **`database_manager.py` (A Persistência):** Inicializa o banco de forma independente.

**Teste de Fogo:** O servidor roda (`python app.py`) sem erros de `ImportError` e acessa a porta 5001.

---

## 2. A Missão Imediata (Ao abrir o código)

Não comece codificando aleatoriamente. O objetivo é implementar a rota de **Edição de Agendamento** seguindo a metodologia:

### Passo A: Definir o Contrato Funcional (Fase 1)
Antes de mexer em `routes/editar_agendamento.py`, responda mentalmente ou no papel:
1.  **Entrada:** O que chega do front-end? (JSON com ID e novos dados?)
2.  **Processamento:** Quais regras de negócio validam essa edição? (O ID existe? A data é futura?)
3.  **Saída:** O que devolvemos? (JSON `{success: true}` ou HTML renderizado?)

### Passo B: Codificação "Feia" (Fase 2)
Implementar a lógica apenas para fazer o contrato passar, sem se preocupar com otimização agora.

---

## 3. Dívida Técnica (Para a Fase 3 - Refatoração)
**NÃO ESQUECER:** Existem falhas de segurança propositais no `app.py` que precisam ser corrigidas antes do deploy final:

* [ ] **Segurança Crítica:** A `secret_key` está *hardcoded* (escrita no código). Mover para `.env`.
* [ ] **Ambiente:** O `debug=True` está fixo. Criar condicional para produção vs. desenvolvimento.
* [ ] **Validação:** Adicionar `try/except` robusto nas chamadas de banco de dados.

---

## 4. Comandos para Reiniciar
Para rodar o projeto ao voltar:

```bash
# 1. Ativar ambiente virtual (se houver)
# source venv/bin/activate  (Mac/Linux)
# venv\Scripts\activate     (Windows)

# 2. Rodar a aplicação
python app.py