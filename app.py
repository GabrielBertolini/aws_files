import uuid
import boto3
import streamlit as st

# ======================================
# CONFIGURAÇÃO
# ======================================

BUCKET = "resultado-plagio"
PASTA = "interface_envio"

# Cliente AWS
s3 = boto3.client(
    "s3",
    aws_access_key_id=st.secrets["AWS_ACCESS_KEY_ID"],
    aws_secret_access_key=st.secrets["AWS_SECRET_ACCESS_KEY"],
    region_name=st.secrets["AWS_REGION"],
)

# ======================================
# CONFIGURAÇÃO DA PÁGINA
# ======================================

st.set_page_config(
    page_title="Upload de Documentos",
    page_icon="📄",
    layout="centered"
)

st.title("📄 Upload de Documentos")

st.write(
    "Selecione um arquivo PDF para enviá-lo ao servidor."
)

# ======================================
# UPLOAD
# ======================================

arquivo = st.file_uploader(
    "Escolha um PDF",
    type=["pdf"]
)

if arquivo is not None:

    st.write(f"**Arquivo selecionado:** {arquivo.name}")

    if st.button("Enviar"):

        with st.spinner("Enviando arquivo..."):

            nome = f"{uuid.uuid4()}_{arquivo.name}"

            key = f"{PASTA}/{nome}"

            s3.upload_fileobj(
                arquivo,
                BUCKET,
                key,
                ExtraArgs={
                    "ContentType": "application/pdf",
                    "ContentDisposition": "inline"
                }
            )

            url = s3.generate_presigned_url(
                "get_object",
                Params={
                    "Bucket": BUCKET,
                    "Key": key,
                    "ResponseContentDisposition": "inline"
                },
                ExpiresIn=604800  # 7 dias
            )

        st.success("✅ Upload realizado com sucesso!")

        st.divider()

        st.subheader("Informações")

        st.write(f"**Arquivo:** {arquivo.name}")

        st.write(f"**Bucket:** {BUCKET}")

        st.write(f"**Pasta:** {PASTA}")

        st.divider()

        st.subheader("Link")

        st.code(url)

        st.link_button(
            "👁 Abrir PDF",
            url,
            use_container_width=True
        )