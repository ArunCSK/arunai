/**
 * Self-evolving agent loop as a VS Code Chat Participant.
 *
 * package.json needs a "chatParticipants" contribution point registering
 * an id, e.g. "self-evolving.solver", matching the id used below.
 *
 * There's no built-in "loop until done" primitive in the Chat/Language Model
 * API, so — same shape as the Claude Agent SDK example — we drive the
 * ACT -> EVALUATE -> EVOLVE cycle ourselves with a `while` loop, streaming
 * each iteration back to the user via `stream`.
 */

import * as vscode from 'vscode';

const MAX_ITERATIONS = 5;
const COMPLETION_TOKEN = 'DONE';

async function askModel(
    model: vscode.LanguageModelChat,
    prompt: string,
    token: vscode.CancellationToken
): Promise<string> {
    const messages = [vscode.LanguageModelChatMessage.User(prompt)];
    const response = await model.sendRequest(messages, {}, token);
    let text = '';
    for await (const fragment of response.text) {
        text += fragment;
    }
    return text;
}

const handler: vscode.ChatRequestHandler = async (
    request: vscode.ChatRequest,
    _context: vscode.ChatContext,
    stream: vscode.ChatResponseStream,
    token: vscode.CancellationToken
) => {
    const goal = request.prompt;
    const model = request.model; // the model the user picked in the Chat view

    let candidate = '';
    let feedback = '';

    for (let iteration = 1; iteration <= MAX_ITERATIONS; iteration++) {
        stream.progress(`Iteration ${iteration}: generating...`);

        // ACT: generate or revise, folding in the prior critique (evolved state)
        const actPrompt =
            iteration === 1
                ? `Goal:\n${goal}\n\nProduce a solution. Output only the result.`
                : `Goal:\n${goal}\n\nPrevious attempt:\n${candidate}\n\n` +
                `Feedback to address:\n${feedback}\n\n` +
                `Produce an improved version. Output only the result.`;

        candidate = await askModel(model, actPrompt, token);
        stream.markdown(`**Attempt ${iteration}:**\n\n\`\`\`\n${candidate}\n\`\`\`\n`);

        // EVALUATE: separate call, structured verdict so it can't rationalize in the same breath
        stream.progress(`Iteration ${iteration}: checking against the goal...`);
        const evalPrompt =
            `Goal:\n${goal}\n\nCandidate:\n${candidate}\n\n` +
            `If it fully satisfies the goal, respond with exactly "${COMPLETION_TOKEN}". ` +
            `Otherwise, respond with concrete feedback on what to fix (no other text).`;
        const verdict = (await askModel(model, evalPrompt, token)).trim();

        if (verdict === COMPLETION_TOKEN) {
            stream.markdown(`\n✅ Goal satisfied after ${iteration} iteration(s).`);
            return { metadata: { iterations: iteration } };
        }

        // EVOLVE: carry the critique into the next pass
        feedback = verdict;
        stream.markdown(`_Feedback:_ ${feedback}\n\n---\n`);
    }

    stream.markdown(`\n⚠️ Reached the ${MAX_ITERATIONS}-iteration cap without a DONE verdict.`);
    return { metadata: { iterations: MAX_ITERATIONS, maxedOut: true } };
};

export function activate(context: vscode.ExtensionContext) {
    const participant = vscode.chat.createChatParticipant('self-evolving.solver', handler);
    participant.iconPath = new vscode.ThemeIcon('sync');
    context.subscriptions.push(participant);
}