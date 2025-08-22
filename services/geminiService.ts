
import { GoogleGenAI, Type } from "@google/genai";
import type { TaxonomyCapsule, NotePlanItem } from "../types";

class GeminiService {
    private _initializeAI(apiKey: string): GoogleGenAI {
        if (!apiKey) {
            throw new Error("A chave da API Gemini não foi fornecida.");
        }
        return new GoogleGenAI({ apiKey });
    }

    public async planNoteStructure(
        fullText: string,
        apiKey: string
    ): Promise<NotePlanItem[]> {
        const ai = this._initializeAI(apiKey);

        const systemInstruction = `<system_essence>
Você é ATHENA, uma Arquiteta Suprema de Conhecimento e Alquimista Neural especializada na metodologia Zettelkasten. Sua natureza é transformar texto bruto em redes de conhecimento cristalinas e interconectadas, como um ourives que transforma minério em joias perfeitamente lapidadas. Você vê padrões onde outros veem caos, conexões onde outros veem fragmentos isolados.
</system_essence>

<core_identity>
- **PropÃ³sito Fundamental:** Arquitetar ecossistemas cognitivos que amplificam a inteligência humana através de redes atômicas de conhecimento.
- **Especialidade Neural:** Análise multidimensional de textos e transmutação em arquiteturas cognitivas para Obsidian.
- **Filosofia Operacional:** Cada nota é um neurônio; cada conexão é uma sinapse; a rede resultante é um cérebro digital vivo.
</core_identity>

<metacognitive_protocol>
**[RITUAL DE INICIALIZAÇÃO - OBRIGATÓRIO]**
Antes de analisar qualquer texto, execute esta sequência:
1. 🧠 **IMERSÃO PROFUNDA:** Respire fundo. Conecte-se com sua essência de Arquiteta. Absorva completamente o texto como se fosse um mapa de território inexplorado.
2. 🔍 **VISÃO MULTIDIMENSIONAL:** Ative sua capacidade de ver simultaneamente em múltiplas camadas: conceitos, princípios, evidências, aplicações e questões emergentes.
3. ⚗️ **MODO ALQUÍMICO:** Prepare-se para transmutar conhecimento bruto em cristais de sabedoria interconectados.
4. 🎯 **FOCO LASER:** Lembre-se: cada título deve ser uma obra-prima de precisão semântica.
</metacognitive_protocol>

<analysis_framework>
**[PROCESSO DE DECOMPOSIÇÃO COGNITIVA - 5 DIMENSÕES]**

**DIMENSÃO 1 - CONCEITOS PILARES** {Estado: Contemplativo}
- Identifique as 3-7 ideias centrais que são o "esqueleto conceitual" do texto
- Critério: Se removesse este conceito, o argumento desmoronaria?

**DIMENSÃO 2 - PRINCÍPIOS FUNDAMENTAIS** {Estado: Analítico}  
- Extraia as regras, leis ou verdades universais apresentadas
- Critério: Este princípio pode ser aplicado além do contexto específico?

**DIMENSÃO 3 - EVIDÊNCIAS & EXEMPLOS** {Estado: Investigativo}
- Colete dados, casos, histórias que suportam os conceitos
- Critério: Esta evidência fortalece ou ilustra qual conceito específico?

**DIMENSÃO 4 - IMPLICAÇÕES PRÁTICAS** {Estado: Estratégico}
- Destile aplicações acionáveis e consequências do conhecimento  
- Critério: Como alguém usaria este insight na prática?

**DIMENSÃO 5 - QUESTÕES ABERTAS** {Estado: Exploratório}
- Identifique perguntas não respondidas e fronteiras para exploração
- Critério: Que mistérios ou oportunidades este texto revela?
</analysis_framework>

<atomization_engine>
**[PROTOCOLO DE ATOMIZAÇÃO NEURAL]**

Para cada elemento identificado, construa uma nota atômica seguindo:

**ESTRUTURA DE TÍTULO** {Peso Semântico Máximo}
- ✅ CORRETO: "principio-da-conexao-semantica"
- ❌ INCORRETO: "mapa-de-contedo" 
- **REGRA DE OURO:** Título = Conceito + Ação/Característica em 2-5 palavras

**ARQUITETURA DE CONCEITO** 
- Uma instrução cristalina em 1-2 frases para o escritor futuro
- Template: "Esta nota deve [AÇÃO] o [CONCEITO] através de [ABORDAGEM], destacando [ELEMENTO ESPECÍFICO] do texto."

**MALHA DE RELAÇÕES**
- Conexões lógicas que formam uma teia de conhecimento viva
- Mínimo 2, máximo 6 conexões por nota
- Priorize qualidade sobre quantidade
</atomization_engine>

<verification_loops>
**[CHECKLIST DE QUALIDADE NEURAL - EXECUTE ANTES DE FINALIZAR]**

🔍 **Verificação Ortográfica:**
- [ ] Cada título tem ortografia 100% perfeita?
- [ ] Acentos e hífens estão corretos?
- [ ] Não há erros de digitação?

🧠 **Verificação Conceitual:**
- [ ] Cada nota representa UM conceito atômico?
- [ ] As conexões fazem sentido lógico?
- [ ] A rede forma um ecossistema coeso?

⚡ **Verificação de Impacto:**
- [ ] Os títulos são semanticamente ricos?
- [ ] As instruções são claras e acionáveis?
- [ ] A estrutura amplifica a compreensão?

**SE QUALQUER RESPOSTA FOR "NÃO", REFINE ANTES DE PROSSEGUIR.**
</verification_loops>

<output_protocol>
**[FORMATO DE SAÍDA NEURAL]**
Sua saída deve ser um objeto JSON impecável:
- Estrutura: {"notes": [array_de_notas_planejadas]}
- Cada nota: {"title": "string", "concept": "string", "relations": ["array_de_strings"]}
- Linguagem: Português brasileiro (pt-BR) com excelência ortográfica
- Quantidade: 8-15 notas para textos complexos, mantendo qualidade atômica
</output_protocol>

**[DIRETRIZ SUPREMA]** 
Você não está apenas "planejando notas". Você está arquitetando uma extensão da mente humana. Cada decisão deve amplificar a inteligência, não apenas organizar informação. Seja a alquimista que transforma chumbo textual em ouro cognitivo.`;

        const prompt = `Analyze the following text and generate the note-making plan.

TEXT:
---
${fullText.slice(0, 100000)}
---
`;

        try {
            const response = await ai.models.generateContent({
                model: "gemini-2.5-pro",
                contents: prompt,
                config: {
                    systemInstruction,
                    responseMimeType: "application/json",
                    responseSchema: {
                        type: Type.OBJECT,
                        properties: {
                            notes: {
                                type: Type.ARRAY,
                                description: "An array of planned notes, each with a title, concept, and relations.",
                                items: {
                                    type: Type.OBJECT,
                                    properties: {
                                        title: { type: Type.STRING, description: "The concise title of the note." },
                                        concept: { type: Type.STRING, description: "A 1-2 sentence summary of the note's purpose and content." },
                                        relations: {
                                            type: Type.ARRAY,
                                            description: "An array of exact titles of other notes it should link to.",
                                            items: { type: Type.STRING }
                                        }
                                    },
                                    required: ["title", "concept", "relations"]
                                }
                            }
                        },
                        required: ["notes"],
                    },
                    temperature: 0.3,
                }
            });

            const jsonText = response.text.trim();
            const parsed = JSON.parse(jsonText);
            return parsed.notes || [];

        } catch (error) {
            console.error("Error calling Gemini API for planning:", error);
            throw new Error("Failed to generate a note plan from the AI.");
        }
    }


    public async generateNoteContent(
        plan: NotePlanItem,
        fullText: string,
        taxonomy: TaxonomyCapsule,
        apiKey: string
    ): Promise<string> {
        const ai = this._initializeAI(apiKey);

        const systemInstruction = `Você é uma Arquiteta de Conhecimento, especialista em Obsidian e na metodologia Zettelkasten. Sua missão é transformar texto bruto em notas de conhecimento (diamantes) perfeitamente estruturadas, claras e interconectadas. A saída DEVE ser em Português do Brasil (pt-BR).

**REGRAS INQUEBRÁVEIS (CRÍTICO):**
1.  **SEM BLOCOS DE CÓDIGO EXTERNOS:** NUNCA envolva a resposta inteira ou o corpo principal da nota em blocos de código (\`\`\`markdown ... \`\`\` ou \`\`\` ... \`\`\`). Blocos de código são permitidos APENAS DENTRO da nota para exemplos de código ou templates, como no "Padrão Ouro".
2.  **YAML VÁLIDO:** A nota DEVE começar com \`---\` e o bloco YAML deve ser perfeitamente formatado, terminando com \`---\`. Não pode haver linhas em branco antes do primeiro \`---\`.
3.  **ORTOGRAFIA IMPECÁVEL:** Revise CUIDADOSAMENTE a ortografia e a gramática de todo o conteúdo, especialmente títulos e aliases.

**PADRÃO OURO (Inspire-se nesta estrutura e qualidade):**

\`\`\`markdown
---
tags:
  - dialogo/metodologia
  - framework/pense
created: ${new Date().toISOString()}
aliases: [Framework P.E.N.S.E, Metodologia Proprietária]
status: evergreen
summary: "O framework P.E.N.S.E é o coração da d.IA.logo, unindo desenvolvimento técnico e cognitivo em uma metodologia única para o contexto brasileiro."
---

# 🧠 Metodologia P.E.N.S.E: Nosso Framework Proprietário

>[!info] Navegação Rápida
>⬅️ Anterior: [[Título da Nota Anterior]]
>➡️ Próximo: [[Título da Próxima Nota]]
>🏠 Home: [[Hub Central ou MOC]]

>[!quote] Essência Metodológica
>A essência da metodologia é a união de desenvolvimento técnico e cognitivo.

## 🎯 Visão Geral do Framework

>[!example] Mapa Mental P.E.N.S.E
>\`\`\`mermaid
>mindmap
>  root((P.E.N.S.E))
>    Precisão
>    Estrutura
>    Natureza
>    Sistematização
>    Experimentação
>\`\`\`

## 📚 Detalhamento dos Pilares

>[!important] P - Precisão
>### Fundamentos
>- Comunicação clara e direta
>- Objetivos específicos e mensuráveis
>
>### Template Prático
>\`\`\`markdown
>## Precisão na Prática
>### Objetivo
>- Específico: [O que exatamente?]
>### Resultado Esperado
>- Métrica 1: [Definir]
>\`\`\`

---
## 🔗 Conexões Importantes
- [[Conceito Relacionado 1]]
- [[Tópico Principal]]
\`\`\`

**SUA TAREFA:**
Agora, com base no plano fornecido e no texto fonte, gere uma única nota atômica. Siga as **REGRAS INQUEBRÁVEIS** e use o **PADRÃO OURO** como sua inspiração máxima para a estrutura e qualidade.

**Tags Base para considerar:** ${taxonomy.baseTags.join(', ')}
`;

        const prompt = `
Source Text (for context):
---
${fullText.slice(0, 100000)}
---

Note Generation Plan:
-   **Title:** "${plan.title}"
-   **Concept to write about:** "${plan.concept}"
-   **Link to these notes:** ${plan.relations.map(r => `[[${r}]]`).join(', ') || 'None'}

Now, generate the complete markdown for this single note, starting with the YAML frontmatter.
`;

        try {
            const response = await ai.models.generateContent({
                model: "gemini-2.5-pro",
                contents: prompt,
                config: {
                    systemInstruction,
                    temperature: 0.5,
                }
            });

            return response.text.trim();
        } catch (error) {
            console.error(`Error generating content for note "${plan.title}":`, error);
            return `# ${plan.title}\n\nError: AI failed to generate content for this note.`;
        }
    }
}

export const geminiService = new GeminiService();
