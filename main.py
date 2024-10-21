import flet as ft
import pyrebase
import os


# Configuração do Firebase
firebaseConfig = {
    'apiKey': "AIzaSyD_o1TaA7m4ZKRGLzvnyoaC0yCKK9CqTXM",
    'authDomain': "board-07.firebaseapp.com",
    'projectId': "board-07",
    'storageBucket': "board-07.appspot.com",
    'databaseURL': "https://board-07-default-rtdb.firebaseio.com",
    'messagingSenderId': "164500572156",
    'appId': "1:164500572156:web:e8d11936ab8db3d65c1479",
    'measurementId': "G-MLW62WTQFX"
}

"""# Configuração do Firebase usando variáveis de ambiente
# Configuração do Firebase usando variáveis de ambiente
firebaseConfig = {
    'apiKey': os.getenv('FIREBASE_API_KEY'),
    'authDomain': os.getenv('FIREBASE_AUTH_DOMAIN'),
    'projectId': os.getenv('FIREBASE_PROJECT_ID'),
    'storageBucket': os.getenv('FIREBASE_STORAGE_BUCKET'),
    'databaseURL': os.getenv('FIREBASE_DATABASE_URL'),
    'messagingSenderId': os.getenv('FIREBASE_MESSAGING_SENDER_ID'),
    'appId': os.getenv('FIREBASE_APP_ID'),
    'measurementId': os.getenv('FIREBASE_MEASUREMENT_ID')
}"""

# Inicializar o Firebase
firebase = pyrebase.initialize_app(firebaseConfig)
db = firebase.database()

# Função para salvar no Firebase com verificações e logs
def salvar_no_firebase(caminho, dados):
    try:
        #print(f"Tentando gravar no caminho: {caminho}")
        #print(f"Dados a serem gravados: {dados}")
        db.child(caminho).set(dados)
        #print("Gravação bem-sucedida!")
    except Exception as e:
        print(f"Erro ao gravar: {e}")

# Função para ler os dados do Firebase
def ler_dados_firebase():
    try:
        dados = db.child("modulos").get().val()
        if dados:
            #print("Dados lidos do Firebase:")
            #print(dados)
            return dados
        else:
            print("Nenhum dado encontrado no Firebase.")
            return {}
    except Exception as e:
        print(f"Erro ao ler dados do Firebase: {e}")
        return {}

# Função para exibir a tela inicial com as lições
def exibir_licoes(page, modulos):
    page.controls.clear()
    page.add(ft.Text("Selecione uma Lição", size=24, weight="bold", text_align=ft.TextAlign.CENTER))

    if modulos:
        for modulo_id, modulo in modulos.items():
            if 'licoes' in modulo and isinstance(modulo['licoes'], list):  # Verificar se a chave 'licoes' existe e é uma lista
                for idx, licao in enumerate(modulo['licoes']):
                    # Criar links para cada lição
                    def criar_licao_link(licao=licao, modulo_id=modulo_id, idx=idx):
                        return ft.TextButton(
                            text=f"Lição: {licao['licao']}",
                            on_click=lambda e: exibir_conteudo_licao(page, modulo_id, idx, licao)
                        )
                    page.add(criar_licao_link())
            else:
                page.add(ft.Text(f"O módulo '{modulo_id}' não contém lições válidas.", color="red"))
    else:
        page.add(ft.Text("Nenhuma lição encontrada.", text_align=ft.TextAlign.CENTER))

    page.update()

# Função para exibir o conteúdo da lição selecionada
def exibir_conteudo_licao(page, modulo_id, idx_licao, licao):
    page.controls.clear()

    page.add(ft.Text(f"Lição: {licao['licao']}", size=24, weight="bold", text_align=ft.TextAlign.CENTER))

    # Criar dicionários para manter os campos de entrada e garantir que os valores sejam capturados corretamente
    campos_perguntas = {}
    campos_respostas = {}
    campo_resposta_correta = {}
    campo_comentario = {}

    # Gerar campos editáveis para cada pergunta
    for idx_pergunta, pergunta in enumerate(licao['perguntas']):
        # Criar campo para a pergunta e armazená-lo no dicionário
        pergunta_input = ft.TextField(value=pergunta['pergunta'], label="Pergunta", width=400)
        campos_perguntas[idx_pergunta] = pergunta_input

        # Criar campos de respostas e armazená-los no dicionário
        respostas_inputs = [
            ft.TextField(value=resposta, label=f"Resposta {i+1}", width=300)
            for i, resposta in enumerate(pergunta['respostas'])
        ]
        campos_respostas[idx_pergunta] = respostas_inputs

        # Campo de resposta correta e comentário
        resposta_correta_input = ft.TextField(value=pergunta['resposta_correta'], label="Resposta Correta", width=300)
        comentario_input = ft.TextField(value=pergunta['comentario'], label="Comentário", multiline=True, width=400)

        campo_resposta_correta[idx_pergunta] = resposta_correta_input
        campo_comentario[idx_pergunta] = comentario_input

        def salvar_alteracoes(e, idx=idx_pergunta):
            # Coletar os novos valores digitados pelo usuário
            nova_pergunta = campos_perguntas[idx].value
            novas_respostas = [r.value for r in campos_respostas[idx]]
            nova_resposta_correta = campo_resposta_correta[idx].value
            novo_comentario = campo_comentario[idx].value

            # Gerar dados atualizados
            dados_atualizados = {
                "pergunta": nova_pergunta,
                "respostas": novas_respostas,
                "resposta_correta": nova_resposta_correta,
                "comentario": novo_comentario
            }

            # Log dos dados antes de salvar
            #print(f"Dados atualizados para a pergunta {idx} na lição {idx_licao}: {dados_atualizados}")

            # Gravar dados no Firebase
            caminho = f"modulos/{modulo_id}/licoes/{idx_licao}/perguntas/{idx}"
            salvar_no_firebase(caminho, dados_atualizados)

            # Exibir mensagem de sucesso
            snack_bar = ft.SnackBar(ft.Text("Correção salva com sucesso!"))
            page.overlay.append(snack_bar)
            snack_bar.open = True
            page.update()

        # Adicionar campos e botão de salvar
        page.add(
            ft.Column([
                pergunta_input,
                *respostas_inputs,
                resposta_correta_input,
                comentario_input,
                ft.ElevatedButton("Salvar Correções", on_click=salvar_alteracoes, width=200)
            ], alignment="center", horizontal_alignment="center", spacing=10)
        )

    # Botão de retorno
    page.add(ft.ElevatedButton("Voltar às Lições", on_click=lambda e: exibir_licoes(page, ler_dados_firebase()), width=200))

    page.update()

# Função principal do Flet
def main(page: ft.Page):
    page.title = "Correção de Perguntas"
    page.scroll = "auto"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    modulos = ler_dados_firebase()
    exibir_licoes(page, modulos)

# Função para rodar o app

ft.app(target=main, view=ft.AppView.WEB_BROWSER)#abrir no navegador
