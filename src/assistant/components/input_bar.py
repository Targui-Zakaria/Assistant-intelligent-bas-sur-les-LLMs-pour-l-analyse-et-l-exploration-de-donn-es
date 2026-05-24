"""Barre de saisie unifiée : PDF + message (style ChatGPT)."""
import streamlit as st

from src.assistant.services.pdf_service import extract_text_from_pdf
from src.assistant.utils.session import get_pdf_document, set_pdf_document


def handle_pdf_upload(uploaded) -> None:
    if uploaded is None:
        return
    last = st.session_state.get("_last_pdf_id")
    file_id = f"{uploaded.name}_{uploaded.size}"
    if last == file_id:
        return
    st.session_state._last_pdf_id = file_id
    try:
        text, pages = extract_text_from_pdf(uploaded.getvalue())
        if not text.strip():
            st.warning("Le PDF ne contient pas de texte extractible.")
            return
        set_pdf_document(uploaded.name, text, pages)
        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": (
                    f"**PDF importé :** `{uploaded.name}` "
                    f"({pages} page(s), {len(text)} caractères). "
                    f"Vous pouvez poser des questions sur ce document."
                ),
                "dataframe": None,
                "sql": None,
                "success": True,
                "show_sql": False,
                "show_download": False,
            }
        )
        st.rerun()
    except Exception as exc:
        st.error(f"Impossible de lire le PDF : {exc}")


def render_input_bar(pipeline: dict, example: str | None) -> None:
    doc = get_pdf_document()

    st.markdown('<div class="input-bar-shell">', unsafe_allow_html=True)

    if doc:
        st.markdown(
            f'<p class="input-bar-pdf-tag">PDF : {doc["name"]}</p>',
            unsafe_allow_html=True,
        )

    row = st.container()
    with row:
        c_attach, c_chat = st.columns([0.55, 11.45], gap="small", vertical_alignment="center")

        with c_attach:
            st.markdown('<div class="pdf-attach-wrap">', unsafe_allow_html=True)
            uploaded = st.file_uploader(
                "PDF",
                type=["pdf"],
                label_visibility="collapsed",
                key="pdf_uploader",
                help="Importer un PDF",
            )
            st.markdown("</div>", unsafe_allow_html=True)
            handle_pdf_upload(uploaded)

        with c_chat:
            prompt = st.chat_input("Message à l'assistant…")
            if example and not prompt:
                prompt = example
            if prompt:
                from src.assistant.components.chat import process_user_input

                process_user_input(prompt, pipeline)

    st.markdown("</div>", unsafe_allow_html=True)
