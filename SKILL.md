---
name: lecture-pdf-teacher
description: Read uploaded PDF courseware, extract and understand its content, explain every major concept from the perspective of an experienced university teacher, automatically save a detailed Markdown note beside the original PDF, delete temporary draft files, and give only a brief chat summary of the saved notes. Use when the user asks to analyze, teach, explain in Chinese, summarize-and-teach, or produce notes from PDF lecture slides/courseware, especially when they want detailed teacher-style explanations, LaTeX-formatted symbols and formulas in the .md file, and a concise completion summary in chat.
---

# Lecture PDF Teacher

## Workflow

1. Identify the source PDF path from the user message or attached file context.
2. Use the host agent's native PDF text extraction or OCR capability to read the courseware. If the host provides a dedicated PDF skill or tool, use it; otherwise use any available parser. Prefer text extraction first; use OCR only when pages are scanned or mostly image-based.
3. Inspect enough page structure to preserve the courseware order: title, section headings, slide/page sequence, equations, diagrams, examples, and exercises.
4. Teach the material in Chinese by default unless the user asks for another language.
5. Compose the full explanation as the canonical Markdown note body for the saved file. The chat response should not reproduce the note in full.
6. Format all mathematical symbols, variables, equations, derivations, and units using LaTeX in Markdown.
7. Save the full explanation as a Markdown file in the same directory as the original PDF.
8. Delete any temporary Markdown draft file created only to pass content into the save script before completing the task.
9. In the final chat response, briefly describe what the saved note covers, report the exact saved Markdown path, and mention any extraction limitations. Do not paste the complete note content unless the user explicitly asks for it.

## Host Agent Compatibility

Keep the workflow independent of a particular agent, tool name, or user interface.

- When the host agent supports automatic Agent Skills discovery, install this folder according to that agent's skill-directory rules.
- When automatic discovery is unavailable, provide the path to this folder and ask the agent to read `SKILL.md` before processing the PDF.
- Use the host agent's available PDF extraction and OCR tools. Do not assume that a tool named `pdf` or a specific MCP server exists.
- Run `scripts/save_lecture_notes.py` with the host environment's Python 3 command, such as `python` or `python3`.
- Treat `agents/openai.yaml` as optional OpenAI/Codex interface metadata. The core workflow is defined by `SKILL.md` and must remain usable when that file is ignored.

## Teaching Style

Act as an experienced university teacher, not as a brief summarizer.

- Explain all substantive content in the PDF, following the original order.
- For each chapter, section, or slide group, state the learning objective, prerequisite ideas, key concepts, formulas, reasoning steps, and common misunderstandings.
- Explain equations by naming variables, assumptions, physical or mathematical meaning, derivation logic when visible, and how to use the formula.
- Explain diagrams, tables, and flowcharts in words. If a visual cannot be extracted precisely, state what can be inferred and avoid inventing unseen details.
- Connect abstract ideas to intuitive examples, classroom-style analogies, or typical engineering/science applications when helpful.
- Preserve important terms from the slides. When useful, include bilingual term pairs, for example `center-of-mass equations of motion`.
- If the PDF contains exercises or examples, solve or explain their method unless the user asks only for conceptual lecture notes.
- Mark uncertain OCR or extraction results explicitly instead of guessing.

## LaTeX Formula Style

Match the style of polished course notes: all mathematical notation in the saved Markdown file must be Markdown-compatible LaTeX.

- Use inline LaTeX for variables and short expressions: `$x(t)$`, `$X(j\omega)$`, `$t<0$`, `$\omega_c$`, `$\mathrm{rad/s}$`.
- Use display LaTeX for standalone definitions, transform pairs, formulas, and important results:

```markdown
$$
X(j\omega)=\int_{-\infty}^{+\infty}x(t)e^{-j\omega t}\,dt
$$
```

- Use `aligned` for multi-line derivations:

```markdown
$$
\begin{aligned}
Y(j\omega)
&=H(j\omega)X(j\omega)\\
&=\frac{1}{j\omega}X(j\omega)+\pi X(0)\delta(\omega)
\end{aligned}
$$
```

- Use `cases` for piecewise definitions:

```markdown
$$
H(j\omega)=
\begin{cases}
1, & |\omega|\le \omega_c\\
0, & |\omega|>\omega_c
\end{cases}
$$
```

- Use LaTeX commands for Greek letters, operators, and special functions: `$\omega$`, `$\tau$`, `$\delta(t)$`, `$\operatorname{sinc}(\theta)$`, `$\mathcal{F}\{x(t)\}$`.
- Use `\left(`, `\right)`, `\frac{}`, `\sqrt{}`, `\sum`, `\int`, `\lim`, and superscripts/subscripts where appropriate.
- Use `\mathrm{}` for units and non-variable labels inside math, such as `$\mathrm{Hz}$`, `$\mathrm{rad/s}$`, and `$\mathrm{DC}$`.
- Avoid plain-text math like `x(t) -> X(jw)`, `omega_c`, `sin(wt)/(pi t)`, or `H1*H2` when it represents a formula. Write `$x(t)\leftrightarrow X(j\omega)$`, `$\omega_c$`, `$\sin(\omega t)/(\pi t)$`, and `$H_1(j\omega)H_2(j\omega)$` instead.
- When the PDF extraction produces garbled formula text, reconstruct the formula only when it is clear from context or visible page content. Otherwise mark it as uncertain.

## Chat Response Style

Keep the chat response concise. The detailed teaching content belongs in the saved Markdown note.

- Summarize the note in a few short paragraphs or bullets: topic, main sections covered, key formulas/concepts included, and suggested study focus.
- Do not use LaTeX math delimiters or LaTeX commands in the chat response. Avoid `$...$`, `$$...$$`, `\omega`, `\frac{}`, `aligned`, `cases`, matrices, and multi-line derivations in chat.
- If a formula or symbol must be mentioned in chat, write it as plain text, for example `H(jw)`, `omega_c`, `x(t) -> X(jw)`, `sin(wt)/(pi t)`, or `H1(jw)H2(jw)`.
- Put all properly formatted LaTeX formulas, derivations, and symbol tables in the saved Markdown file instead of the chat response.

## Markdown Output

Create a polished study-note document, not a raw transcript. The saved Markdown note is the full teaching output; the chat response is only a concise completion summary.

Use this structure when applicable. Write section titles in Chinese in the final notes unless the user requests another language.

```markdown
# <courseware title or PDF stem> lecture notes

## Courseware overview

## Learning objectives

## Detailed explanation

### Part 1: ...

## Key formulas and concepts

## Common mistakes and study advice

## Review outline
```

Include page or slide references like `page 3` when the source location is known. Keep the explanation detailed enough that the user can study from the Markdown without reopening the PDF. Use LaTeX formatting consistently throughout the note, including symbol explanations, formula tables, examples, and exercises.

## Saving The File

Use the bundled `scripts/save_lecture_notes.py` helper to write the Markdown file beside the source PDF.

Recommended command:

```bash
python scripts/save_lecture_notes.py --pdf "<path-to-source.pdf>" --content-file "<path-to-temp-notes.md>"
```

If the host uses a different Python command, substitute it for `python`.

The script creates a file named `<original-pdf-stem>_讲解笔记.md` in the original PDF directory.

If that file already exists, the script writes a numbered filename such as `<stem>_讲解笔记_2.md` unless `--overwrite` is passed.

Create the temporary `content-file` outside the PDF directory when possible, such as in the current workspace or OS temp directory. If a temporary Markdown file is created in the PDF directory, delete it after the final note file is saved. Before finishing, confirm that only the final note file remains in the PDF directory.

Do not finish with only a file path. The final answer must include a brief summary of the saved note, the exact saved output path, confirmation that temporary Markdown drafts were deleted when applicable, and any extraction limitations. Do not include the complete note content in chat unless the user explicitly requests it.
