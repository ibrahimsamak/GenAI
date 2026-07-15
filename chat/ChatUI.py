import gradio as gr


class ChatUI:
    """Gradio front-end for a ChatEngine. Owns layout and presentation only —
    all retrieval/LLM work is delegated to the injected engine.
    """

    def __init__(self, engine, title="# Ask me anything about your resume!"):
        self.engine = engine
        self.title = title

    def _on_submit(self, message, history):
        # Ask the engine, then format the chat history and the context panel (presentation lives here).
        answer, docs = self.engine.answer(message)
        history = history + [{"role": "user", "content": message}, {"role": "assistant", "content": answer}]
        retrieved = "<h2>Relevant Context</h2>" + "".join(f"<p>{doc.page_content}</p>" for doc in docs)
        return history, retrieved

    def build(self):
        # Assemble the Gradio Blocks layout and wire the submit handler.
        with gr.Blocks() as demo:
            gr.Markdown(self.title)
            with gr.Row():
                # Left: the conversation.
                with gr.Column(scale=3):
                    chatbot = gr.Chatbot(height=650, label="Conversation")
                    msg = gr.Textbox(placeholder="Ask anything...", show_label=False)

                # Right: the retrieved context.
                with gr.Column(scale=2):
                    retrieved = gr.HTML(value="<h2>Relevant Context</h2>", label="Retrieved Chunks")

            msg.submit(
                fn=self._on_submit, inputs=[msg, chatbot], outputs=[chatbot, retrieved]
            ).then(fn=lambda: "", outputs=[msg])
        return demo

    def launch(self, **kwargs):
        # Build and serve the app (extra kwargs forwarded to Gradio's launch()).
        self.build().launch(inbrowser=True, theme=gr.themes.Soft(), **kwargs)
