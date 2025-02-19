import streamlit as st
import pandas as pd
from pages.Jogadores import update_data
from dotenv import load_dotenv
import os
# Definindo titulo da Página
st.set_page_config(page_title="Canto do Mestre", page_icon="🎲")
with st.sidebar.expander("ℹ️ Página do Mestre"): 
    st.write(
        "Esta página é exclusiva para o Mestre, permitindo a edição dos dados dos personagens, "
        "além de adicionar ou remover personagens na campanha. "
        "Por questões de segurança e integridade dos dados, o acesso é restrito e só pode ser feito mediante login."
    )
st.markdown(
    """
    <h1 style="text-align: center;">🚫 YOU SHALL NOT PASS 🧙🏻‍♂</h1>
    """,
    unsafe_allow_html=True
)
# Armazenando o usuário e a senha em variáveis
user = os.getenv("USER")
password = os.getenv("PASSWORD")

def main():

    caminho_arquivo_um = 'Projeto-RPG-Controlador/datasets/Pasta1.xlsx'
    caminho_arquivo_dois = 'datasets/Pasta1.xlsx'
    try:
        df = pd.read_excel(caminho_arquivo_um)
    except:
        df = pd.read_excel(caminho_arquivo_dois)

    df.columns = [
        'Jogador', 'Personagem', 'Idade', 'Altura', 'Sexo', 'História', 
        'Personalidade', 'Inventário', 'Peso/Max', 'Peso/Atual', 'Foto', 'Vida', 'Carga'
    ]
    st.dataframe(df)

    # Opções para o usuário: Adicionar ou Editar personagem
    action = st.selectbox("Escolha uma ação", ["Adicionar Novo Personagem", "Editar Personagem Existente"])

    if action == "Adicionar Novo Personagem":
        # Formulário para adicionar novo personagem
        st.header("Adicionar Novo Personagem")
        
        jogador = st.text_input("Jogador")
        personagem = st.text_input("Personagem")
        idade = st.number_input("Idade", min_value=0)
        altura = st.number_input("Altura", min_value=0.0)

        # Mapeamento do sexo
        sexo_opcoes = ["Masculino", "Feminino"]
        sexo_mapeamento = {"Masculino": "m", "Feminino": "f"}
        sexo_visual = st.selectbox("Sexo", sexo_opcoes)
        sexo_final = sexo_mapeamento[sexo_visual]

        historia = st.text_area("História")
        personalidade = st.text_area("Personalidade")
        inventario = st.text_area("Inventário")
        peso_max = st.number_input("Peso Máximo", min_value=0.0)
        peso_atual = st.number_input("Peso Atual", min_value=0.0)
        foto = st.text_input("Foto (URL ou caminho)")
        vida = st.number_input("Vida", min_value=0)
        carga = st.number_input("Carga", min_value=0)
        
        if st.button("Adicionar Personagem"):
            # Adiciona o novo personagem à tabela
            novo_personagem = {
                'Jogador': jogador,
                'Personagem': personagem,
                'Idade': idade,
                'Altura': altura,
                'Sexo': sexo_final,
                'História': historia,
                'Personalidade': personalidade,
                'Inventário': inventario,
                'Peso/Max': peso_max,
                'Peso/Atual': peso_atual,
                'Foto': foto,
                'Vida': vida,
                'Carga': carga
            }
            
            # Transformando o dicionário em um DataFrame de uma linha
            novo_personagem_df = pd.DataFrame([novo_personagem])

            # Concatenando o novo personagem ao DataFrame existente
            df = pd.concat([df, novo_personagem_df], ignore_index=True)
            
            # Salvar no Excel
            try:
                df.to_excel(caminho_arquivo_um, index=False)
            except:
                df.to_excel(caminho_arquivo_dois, index=False)
            st.success("Novo personagem adicionado com sucesso!")

    elif action == "Editar Personagem Existente":
        st.header("Editar ou Excluir Personagem Existente")
        
        # Escolher o personagem para editar
        personagens = df['Personagem'].tolist()
        personagem_edit = st.selectbox("Escolha um personagem para editar ou excluir", personagens)
        personagem_data = df[df['Personagem'] == personagem_edit].iloc[0]

        novo_nome = st.text_input("Nome do Personagem", value=personagem_edit)
        jogador = st.text_input("Jogador", value=personagem_data['Jogador'])
        idade = st.number_input("Idade", min_value=0, value=personagem_data['Idade'])
        altura = st.number_input("Altura", min_value=0.0, value=float(personagem_data['Altura']))
        sexo_opcoes = ["Masculino", "Feminino"]
        sexo_mapeamento = {"m": "Masculino", "f": "Feminino"}
        sexo_visual = sexo_mapeamento.get(personagem_data["Sexo"], "Masculino")
        sexo_escolhido = st.selectbox("Sexo", sexo_opcoes, index=sexo_opcoes.index(sexo_visual))
        sexo_final = {v: k for k, v in sexo_mapeamento.items()}[sexo_escolhido]

        historia = st.text_area("História", value=personagem_data['História'])
        personalidade = st.text_area("Personalidade", value=personagem_data['Personalidade'])
        inventario = st.text_area("Inventário", value=personagem_data['Inventário'])
        peso_max = st.number_input("Peso Máximo", min_value=0.0, value=float(personagem_data['Peso/Max']))
        peso_atual = st.number_input("Peso Atual", min_value=0.0, value=float(personagem_data['Peso/Atual']))
        foto = st.text_input("Foto (URL ou caminho)", value=personagem_data['Foto'])
        vida = st.number_input("Vida", min_value=0, value=personagem_data['Vida'])
        carga = st.number_input("Carga", min_value=0, value=personagem_data['Carga'])
        
        if st.button("Salvar Alterações"):
            # Verificar se o novo nome já existe e evitar duplicatas
            if novo_nome != personagem_edit and novo_nome in df['Personagem'].values:
                st.error("Já existe um personagem com esse nome. Escolha outro nome.")
            else:
                # Atualiza os dados do personagem no DataFrame
                df.loc[df['Personagem'] == personagem_edit, 'Personagem'] = novo_nome
                df.loc[df['Personagem'] == novo_nome, 'Jogador'] = jogador
                df.loc[df['Personagem'] == novo_nome, 'Idade'] = idade
                df.loc[df['Personagem'] == novo_nome, 'Altura'] = altura
                df.loc[df['Personagem'] == novo_nome, 'Sexo'] = sexo_final
                df.loc[df['Personagem'] == novo_nome, 'História'] = historia
                df.loc[df['Personagem'] == novo_nome, 'Personalidade'] = personalidade
                df.loc[df['Personagem'] == novo_nome, 'Inventário'] = inventario
                df.loc[df['Personagem'] == novo_nome, 'Peso/Max'] = peso_max
                df.loc[df['Personagem'] == novo_nome, 'Peso/Atual'] = peso_atual
                df.loc[df['Personagem'] == novo_nome, 'Foto'] = foto
                df.loc[df['Personagem'] == novo_nome, 'Vida'] = vida
                df.loc[df['Personagem'] == novo_nome, 'Carga'] = carga
                
                # Salvar no Excel
                try:
                    df.to_excel(caminho_arquivo_um, index=False)
                except:
                    df.to_excel(caminho_arquivo_dois, index=False)
                st.success(f"Informações de {novo_nome} atualizadas com sucesso!")
                update_data()
        
        if st.button("Excluir Personagem"):
            df = df[df['Personagem'] != personagem_edit]
            try:
                df.to_excel(caminho_arquivo_um, index=False)
            except:
                df.to_excel(caminho_arquivo_dois, index=False)
            st.success(f"Personagem {personagem_edit} excluído com sucesso!")
            update_data()

def login():
    # Campos para o usuário e a senha
    username = st.text_input("Usuário")
    pwd = st.text_input("Senha", type="password")

    # Verificando as credenciais
    if st.button("Login"):
        if username == user and pwd == password:
            st.session_state.logged_in = True
            st.success("Login bem-sucedido!")
            st.rerun()
        else:
            st.session_state.logged_in = False
            st.error("Usuário ou senha incorretos!")

# Verificando se o usuário está logado
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# Exibindo a tabela somente se o usuário estiver logado
if st.session_state.logged_in:
    main()
else:
    login()

# Adicionar o texto no final
st.sidebar.markdown("Desenvolvido por [Rafael Junior de Campos](https://github.com/rafaeljrcampos)")