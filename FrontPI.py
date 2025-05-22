import customtkinter
import pg8000

# função para conectar no banco
def conectar_banco():
    try:
        conn = pg8000.connect(
            user="postgres", 
            password="123456", 
            host="localhost", 
            database="BDNOWA"
        )
        return conn
    except Exception as e:
        print("Erro ao conectar ao banco de dados:", e)
        return None



# Função para salvar os dados no banco
def salvarDadosCliente(dados):
    conn = conectar_banco()
    global cliente_id
    if conn:
        try:
            cursor = conn.cursor()
            query = """
            INSERT INTO cliente (cpf, nome, sobrenome, sexo, dtNasc, email, cidade, uf, rendaMes)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);
            """
            cursor.execute(query, dados)
            conn.commit()
            print("Dados salvos com sucesso!")
        except Exception as e:
            print("Erro ao salvar os dados no banco de dados:", e)
        finally:
            conn.close()
    else:
        print("Conexão com o banco falhou!")
# pega os dados inseridos na interface, envia para a função de cadastrar cliente e os insere no banco de dados
def cadastrarCliente():
    dados = (
        cpf.get(),
        nome.get(),
        sobrenome.get(),
        sexo_var.get(),
        dt_nascimento.get(),
        email.get(),
        cidade.get(),
        uf.get(),
        renda_mensal.get()
    )
    salvarDadosCliente(dados)
    print("Cadastro realizado, tela será atualizada.")
    atualizar_tela()


customtkinter.set_appearance_mode('dark')
customtkinter.set_default_color_theme('dark-blue')

janela = customtkinter.CTk()
janela.title('Cadastro Plataforma de investimentos NOWA')
janela.geometry('700x600')

texto= customtkinter.CTkLabel(janela, text='Bem-vindos(as) à plataforma de investimentos Nowa!')

cpf = customtkinter.CTkEntry(janela, placeholder_text= 'CPF')

nome = customtkinter.CTkEntry(janela, placeholder_text= 'Nome')

sobrenome = customtkinter.CTkEntry(janela, placeholder_text= 'Sobrenome')

sexo_texto = customtkinter.CTkLabel(janela, text='Com qual sexo se identifica?')

sexo_var = customtkinter.StringVar(value="")

dt_nascimento = customtkinter.CTkEntry(janela, placeholder_text='Data de nascimento(DD/MM/AAAA)')

email = customtkinter.CTkEntry(janela, placeholder_text= 'E-mail')

#checkbox = customtkinter.CTkCheckBox(janela, text='Masculino')

#checkbox2 = customtkinter.CTkCheckBox(janela,text='Feminino')

#sexo_label = customtkinter.CTkLabel(janela, text='Com qual sexo você se identifica?')


checkbox_masculino = customtkinter.CTkCheckBox(janela, text='Masculino', variable=sexo_var, onvalue="Masculino", offvalue="")

checkbox_feminino = customtkinter.CTkCheckBox(janela, text='Feminino', variable=sexo_var, onvalue="Feminino", offvalue="")



cidade = customtkinter.CTkEntry(janela, placeholder_text='Cidade atual')

uf = customtkinter.CTkEntry(janela, placeholder_text='UF atual')

renda_mensal = customtkinter.CTkEntry(janela, placeholder_text='Renda mensal média')

botao = customtkinter.CTkButton(janela, text= 'Login',
                                    command= cadastrarCliente)

import re


def validar_dados():
    global cpfCliente
    nome_valor = nome.get()
    email_valor = email.get()
    cpf_valor = cpf.get()
    cpfCliente = cpf.get()

#preciso fazer mais desses gets pras outras entradas, pq preciso verificar as datas também e o UF
    if not nome_valor.isalpha() or len(nome_valor) > 55:
        print("Erro: O nome deve conter apenas letras e ter até 55 caracteres.")
        return False


    if not re.match(r'^[\w\.-]+@(gmail\.com|yahoo\.com|outlook\.com|hotmail\.com)$', email_valor):
        print('Erro: O e-mail deve ser válido e pertencer aos domínios suportados.')
        return False


    if not cpf_valor.isdigit() or len(cpf_valor) != 11:
        print("Erro: O CPF deve conter exatamente 11 dígitos numéricos.")
        return False

    return True

texto.pack(padx= '10', pady= '10')
cpf.pack(padx='10', pady='10', anchor='w')
nome.pack(padx='10', pady='10', anchor='w')
sobrenome.pack(padx='10', pady='10', anchor='w')
sexo_texto.pack(padx='10', pady='10', anchor='w')
checkbox_feminino.pack(padx='10', pady='10', anchor='w')
checkbox_masculino.pack(padx='10', pady='10', anchor='w')
dt_nascimento.pack(padx='10', pady='10', anchor='w')
email.pack(padx= '10', pady= '10', anchor='w')
cidade.pack(padx='10', pady='10', anchor='w')
uf.pack(padx='10', pady='10', anchor='w')
renda_mensal.pack(padx='10', pady='10', anchor='w')
botao.pack(padx='10', pady='10')


def atualizar_tela():

    # Função para salvar os dados no banco
    def salvarRespostas(respostas):
        conn = conectar_banco()
        if conn:
            try:
                cursor = conn.cursor()
                query = """
                INSERT INTO respostas (nivelEduc, objetivo, horizonte, conhecimento, tolerancia, liquidez, ativos, diversificar, startup, informacao, idCliente, idInvest)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
                """
                cursor.execute(query, respostas)
                conn.commit()
            except Exception as e:
                print("Erro ao salvar os dados no banco de dados:", e)
            finally:
                conn.close()
        else:
            print("Conexão com o banco falhou!")

    
    def calcPontuacao(nivel_educacao_var, objetivos_var, horizonte_var, nivel_conhecimento_var, tolerancia_risco_var, liquidez_var, preferencia_var, diversidade_var, startup_var, info_var):
        pontuacao = 0

        if nivel_educacao_var == "Ensino fundamental":
            pontuacao += 1
        elif nivel_educacao_var == "Ensino médio":
            pontuacao += 1
        elif nivel_educacao_var == "Ensino superior incompleto":
            pontuacao += 2
        elif nivel_educacao_var == "Ensino superior completo":
            pontuacao += 2
        elif nivel_educacao_var == "Pós-graduação":
            pontuacao += 3

        if objetivos_var == "Aposentadoria":
            pontuacao += 1
        elif objetivos_var == "Compra de imóveis":
            pontuacao += 1
        elif objetivos_var == "Educação dos filhos":
            pontuacao += 1
        elif objetivos_var == "Viagens e lazer":
            pontuacao += 2
        elif objetivos_var == "Crescimento de patrimônio":
            pontuacao += 3

        if horizonte_var == "Menos de 1 ano":
            pontuacao += 1
        elif horizonte_var == "1-3 anos":
            pontuacao += 1
        elif horizonte_var == "3-5 anos":
            pontuacao += 2
        elif horizonte_var == "5-10 anos":
            pontuacao += 2
        elif horizonte_var == "Mais de 10 anos":
            pontuacao += 3

        if nivel_conhecimento_var == 'Iniciante':
            pontuacao += 1
        elif nivel_conhecimento_var == 'Intermediário':
            pontuacao += 2
        elif nivel_conhecimento_var == 'Avançado':
            pontuacao += 3

        if tolerancia_risco_var == 'Baixa':
            pontuacao += 1
        elif tolerancia_risco_var == 'Moderada':
            pontuacao += 2
        elif tolerancia_risco_var == 'Alta':
            pontuacao += 3
        
        if liquidez_var == 'Alta liquidez':
            pontuacao += 1
        elif liquidez_var == 'Menor liquidez para maiores retornos':
            pontuacao += 2
        elif liquidez_var == 'Não tenho preferência':
            pontuacao += 3

        if preferencia_var == 'Ativos tangíveis (ex: imóveis)':
            pontuacao += 2
        elif preferencia_var == 'Ativos digitais e financeiros (ex: ações, criptoativos)':
            pontuacao += 3
        elif preferencia_var == 'Ambos':
            pontuacao += 3
        elif preferencia_var == 'Nenhum':
            pontuacao += 1

        if diversidade_var == 'Sim, altamente importante':
            pontuacao += 3
        elif diversidade_var == 'Sim, moderadamente importante':
            pontuacao += 2
        elif diversidade_var == 'Não, prefiro focar em poucos setores':
            pontuacao += 1
        elif diversidade_var == 'Não tenho certeza':
            pontuacao += 1

        if startup_var == 'Sim, estou muito interessado':
            pontuacao += 3
        elif diversidade_var == 'Sim, mas com cautela':
            pontuacao += 2
        elif diversidade_var == 'Não, prefiro empresas estabelecidas':
            pontuacao += 1
        elif diversidade_var == 'Não tenho interesse':
            pontuacao += 1

        if info_var == 'Sim, é crucial para mim':
            pontuacao += 3
        elif diversidade_var == 'Sim, mas apenas ocasionalmente':
            pontuacao += 2
        elif diversidade_var == 'Não, confio no gestor de investimentos':
            pontuacao += 1
        elif diversidade_var == 'Não, prefiro uma abordagem simplificada':
            pontuacao += 1

        if pontuacao <= 10:
            pontuacao = 1
        elif pontuacao <= 20:
            pontuacao = 2
        elif pontuacao <= 30:
            pontuacao = 3

        return pontuacao


    def buscarID():
        conn = conectar_banco()
        if conn:
            try:
                cursor = conn.cursor()
                query = """
                SELECT idCliente FROM cliente ORDER BY dtCad DESC LIMIT 1;
                """
                cursor.execute(query)
                resultado = cursor.fetchone()
                # print("ID: ", resultado)
                return resultado
            except Exception as e:
                print("Erro ao buscar o id", e)
            finally:
                conn.close()
        else:
            print("falhou!")

# pega os dados inseridos na interface, envia para a função de cadastrar respostas e os insere no banco de dados
    def cadastrarRespostas(): # essa função deve ser chamada no botao para cadastrar as respostas

        idCliente = buscarID()
        idCliente = int(idCliente[0])
        # print(idCliente)

        tipoInvestidor = calcPontuacao(nivel_educacao_var.get(),
            objetivos_var.get(),
            horizonte_var.get(),
            nivel_conhecimento_var.get(),
            tolerancia_risco_var.get(),
            liquidez_var.get(),
            preferencia_var.get(),
            diversidade_var.get(),
            startup_var.get(),
            info_var.get())
    
        # print("debug:", nivel_educacao_var.get(),
        #     objetivos_var.get(),
        #     horizonte_var.get(),
        #     nivel_conhecimento_var.get(),
        #     tolerancia_risco_var.get(),
        #     liquidez_var.get(),
        #     preferencia_var.get(),
        #     diversidade_var.get(),
        #     startup_var.get(),
        #     info_var.get(),
        #     idCliente,
        #     tipoInvestidor
        #     )


        respostas = (
            nivel_educacao_var.get(),
            objetivos_var.get(),
            horizonte_var.get(),
            nivel_conhecimento_var.get(),
            tolerancia_risco_var.get(),
            liquidez_var.get(),
            preferencia_var.get(),
            diversidade_var.get(),
            startup_var.get(),
            info_var.get(),
            idCliente,
            tipoInvestidor
            )
        def nova_interface():

            for widget in barra_rolagem.winfo_children():
                widget.destroy()
            
            barra_rolo = customtkinter.CTkScrollableFrame(barra_rolagem, width=600, height=600)
            barra_rolo.pack(pady=20, padx=10, fill="both", expand=True)
            
            apresentar_perfil = customtkinter.CTkLabel(barra_rolo, text="Parabéns! O seu perfil de investidor é:")
            apresentar_perfil.pack(padx=10, pady=10)
            
            conn = conectar_banco()
            
            if conn:
                
                try:
                    cursor = conn.cursor()
                    
                    query_cliente = "SELECT MAX(idCliente) FROM cliente;"
                    cursor.execute(query_cliente)
                    ultimo_id_cliente = cursor.fetchone()[0]

                    # Consulta para obter o perfil e fundo associados ao último cliente
                    query_perfil = """
                    SELECT 
                        c.nome || ' ' || c.sobrenome AS nome_cliente,
                        ti.nomeTipo AS tipo_investidor,
                        fi.descricao AS fundo_investimento
                    FROM 
                        cliente c
                    JOIN 
                        respostas r ON c.idCliente = r.idCliente
                    JOIN 
                        tipoInvest ti ON r.idInvest = ti.idInvest
                    JOIN 
                        fundoInvest fi ON ti.idInvest = fi.idInvest
                    WHERE 
                        c.idCliente = %s;
                    """

                    # Executa a consulta com o ID do último cliente
                    cursor.execute(query_perfil, (ultimo_id_cliente,))
                    resultado = cursor.fetchone()

                    if resultado:
                        nome_cliente = resultado[0]
                        tipo_investidor = resultado[1]
                        fundo_investimento = resultado[2]

                        # Exibição do perfil do investidor em uma nova Label
                        perfil_label = customtkinter.CTkLabel(
                            barra_rolo, 
                            text=f"{nome_cliente}, o seu perfil é: {tipo_investidor}\nFundo recomendado: {fundo_investimento}"
                        )
                        perfil_label.pack(padx=10, pady=10)
                    else:
                        # Mensagem caso não haja resultados
                        perfil_label = customtkinter.CTkLabel(
                            barra_rolo, 
                            text="Nenhum cliente encontrado."
                        )
                        perfil_label.pack(padx=10, pady=10)

                except Exception as e:
                    print(f"Erro ao executar a consulta: {e}")
                finally:
                    conn.close()


                rec_investimento = customtkinter.CTkLabel(barra_rolo, text= 'Aqui estão alguns fundos de investimento recomendados para seu perfil!:')
                rec_investimento.pack(padx='10', pady='10')

                conn = conectar_banco()
                if conn:
                    try:
                        cursor = conn.cursor()

                        # Consulta para obter o último ID de cliente cadastrado
                        query_cliente = "SELECT MAX(idCliente) FROM cliente;"
                        cursor.execute(query_cliente)
                        ultimo_id_cliente = cursor.fetchone()[0]

                        # Consulta para obter o fundo de investimento recomendado
                        query_fundo = """
                        SELECT fi.descricao AS fundo_investimento
                        FROM cliente c JOIN respostas r ON c.idCliente = r.idCliente
                        JOIN tipoInvest ti ON r.idInvest = ti.idInvest
                        JOIN fundoInvest fi ON ti.idInvest = fi.idInvest
                        WHERE c.idCliente = %s;
                        """
                        cursor.execute(query_fundo, (ultimo_id_cliente,))
                        resultados = cursor.fetchall()

                        if resultados:
                            for linha in resultados:
                                fundo = linha[0]

                                fundo_label = customtkinter.CTkLabel(barra_rolo, text=f"- {fundo}")
                                fundo_label.pack(padx=10, pady=5)
                        else:
                            
                            fundo_label = customtkinter.CTkLabel(
                                barra_rolo, 
                                text="Nenhum fundo de investimento encontrado."
                            )
                            fundo_label.pack(padx=10, pady=10)

                    except Exception as e:
                        print(f"Erro ao executar a consulta: {e}")
                    finally:
                        conn.close()
        salvarRespostas(respostas)
        print(respostas)
        print("Respostas salvas, tela será atualizada.")
        nova_interface()


    for widget in janela.winfo_children():
        widget.destroy()

    barra_rolagem = customtkinter.CTkScrollableFrame(janela, width=600, height= 500)
    barra_rolagem.pack(padx='20', pady='20', fill= 'both', expand=True)


    nivel_educacao = customtkinter.CTkLabel(barra_rolagem, text='Qual é o seu nível de educação?')
    nivel_educacao.pack(padx='10', pady='10', anchor='w')
    
    nivel_educacao_var = customtkinter.StringVar(value="")
    
    educacao_checkbox1 = customtkinter.CTkCheckBox(barra_rolagem, text='Ensino fundamental', variable=nivel_educacao_var, onvalue="Ensino fundamental", offvalue="")
    educacao_checkbox1.pack(padx='10', pady='10', anchor='w')


    educacao_checkbox2 = customtkinter.CTkCheckBox(barra_rolagem, text='Ensino médio', variable=nivel_educacao_var, onvalue="Ensino médio", offvalue="")
    educacao_checkbox2.pack(padx='10', pady='10', anchor='w')


    educacao_checkbox3 = customtkinter.CTkCheckBox(barra_rolagem, text='Ensino superior incompleto', variable=nivel_educacao_var, onvalue="Ensino superior incompleto", offvalue="")
    educacao_checkbox3.pack(padx='10', pady='10', anchor='w')


    educacao_checkbox4 = customtkinter.CTkCheckBox(barra_rolagem, text= 'Ensino superior completo', variable=nivel_educacao_var, onvalue="Ensino superior completo", offvalue="")
    educacao_checkbox4.pack(padx='10', pady='10', anchor ='w')


    educacao_checkbox5 = customtkinter.CTkCheckBox(barra_rolagem, text= 'Pós-graduação', variable=nivel_educacao_var, onvalue="Pós-graduação", offvalue="")
    educacao_checkbox5.pack(padx='10', pady='10', anchor='w')

    objetivos_invetir = customtkinter.CTkLabel(barra_rolagem, text= 'Qual é o seu principal objetivo ao investir?')
    objetivos_invetir.pack(padx='10', pady='10', anchor='w')

    objetivos_var = customtkinter.StringVar(value="")

    objetivos_checkbox1 = customtkinter.CTkCheckBox(barra_rolagem, text='Aposentadoria', variable=objetivos_var, onvalue="Aposentadoria", offvalue="")
    objetivos_checkbox1.pack(padx='10', pady='10', anchor='w')

    objetivos_checkbox2 = customtkinter.CTkCheckBox(barra_rolagem, text='Compra de imóveis', variable=objetivos_var, onvalue="Compra de imóveis", offvalue="")
    objetivos_checkbox2.pack(padx='10', pady='10', anchor='w')

    objetivos_checkbox3 = customtkinter.CTkCheckBox(barra_rolagem, text='Educação dos filhos', variable=objetivos_var, onvalue="Educação dos filhos", offvalue="")
    objetivos_checkbox3.pack(padx='10', pady='10', anchor='w')

    objetivos_checkbox4 = customtkinter.CTkCheckBox(barra_rolagem, text='Viagens e lazer', variable=objetivos_var, onvalue="Viagens e lazer", offvalue="")
    objetivos_checkbox4.pack(padx='10', pady='10', anchor='w')


    objetivos_checkbox5 = customtkinter.CTkCheckBox(barra_rolagem, text='Crescimento de patrimônio', variable=objetivos_var, onvalue="Crescimento de patrimônio", offvalue="")
    objetivos_checkbox5.pack(padx='10', pady='10', anchor='w')

    horizonte_investimento = customtkinter.CTkLabel(barra_rolagem, text= 'Qual é o seu horizonte de investimento?')
    horizonte_investimento.pack(padx='10', pady='10', anchor='w')

    horizonte_var = customtkinter.StringVar(value="")

    horizontecheckbox1 = customtkinter.CTkCheckBox(barra_rolagem, text='Menos de 1 ano', variable=horizonte_var, onvalue="Menos de 1 ano", offvalue="")
    horizontecheckbox1.pack(padx='10', pady='10', anchor='w')

    horizontecheckbox2 = customtkinter.CTkCheckBox(barra_rolagem, text='1-3 anos', variable=horizonte_var, onvalue="1-3 anos", offvalue="")
    horizontecheckbox2.pack(pady='10', padx='10', anchor='w')

    horizontecheckbox3 = customtkinter.CTkCheckBox(barra_rolagem, text='3-5 anos', variable=horizonte_var, onvalue="3-5 anos", offvalue="")
    horizontecheckbox3.pack(pady='10', padx='10', anchor='w')

    horizontecheckbox4 = customtkinter.CTkCheckBox(barra_rolagem, text='5-10 anos', variable=horizonte_var, onvalue="5-10 anos", offvalue="")
    horizontecheckbox4.pack(padx='10', pady='10', anchor='w')

    horizontecheckbox5 = customtkinter.CTkCheckBox(barra_rolagem, text='Mais de 10 anos', variable=horizonte_var, onvalue="Mais de 10 anos", offvalue="")
    horizontecheckbox5.pack(padx='10', pady='10', anchor='w')

    nivel_conhecimento = customtkinter.CTkLabel(barra_rolagem, text= 'Qual é o seu nível de conhecimento sobre investimentos?')
    nivel_conhecimento.pack(pady='10', padx='10', anchor='w')

    nivel_conhecimento_var = customtkinter.StringVar(value="")

    conhecimentocheckbox1 = customtkinter.CTkCheckBox(barra_rolagem, text= 'Iniciante', variable= nivel_conhecimento_var, onvalue= 'Iniciante', offvalue="")
    conhecimentocheckbox1.pack(pady='10', padx='10', anchor='w')

    conhecimentocheckbox2 = customtkinter.CTkCheckBox(barra_rolagem, text= 'Intermediário', variable= nivel_conhecimento_var, onvalue= 'Intermediário', offvalue= "")
    conhecimentocheckbox2.pack(padx='10', pady='10', anchor='w')

    conhecimentocheckbox3 = customtkinter.CTkCheckBox(barra_rolagem, text= 'Avançado', variable= nivel_conhecimento_var, onvalue= 'Avançado', offvalue= "")
    conhecimentocheckbox3.pack(padx='10', pady='10', anchor= 'w')

    tolerancia_risco = customtkinter.CTkLabel(barra_rolagem, text= 'Qual é o seu nível de tolerância ao risco em investimentos?')
    tolerancia_risco.pack(padx='10', pady='10', anchor='w')

    tolerancia_risco_var = customtkinter.StringVar(value= "")

    riscocheckbox1 = customtkinter.CTkCheckBox(barra_rolagem, text= 'Baixa', variable= tolerancia_risco_var, onvalue= 'Baixa', offvalue="")
    riscocheckbox1.pack(padx='10', pady='10', anchor= 'w')

    riscocheckbox2 = customtkinter.CTkCheckBox(barra_rolagem, text= 'Moderada', variable= tolerancia_risco_var, onvalue= 'Moderada', offvalue="")
    riscocheckbox2.pack(padx='10', pady='10', anchor='w')

    riscocheckbox3 = customtkinter.CTkCheckBox(barra_rolagem, text= 'Alta', variable= tolerancia_risco_var, onvalue= 'Alta', offvalue= "")
    riscocheckbox3.pack(padx='10', pady='10', anchor='w')

    liquidez_investimento = customtkinter.CTkLabel(barra_rolagem, text= 'Você prefere investimentos com alta liquidez ou está disposto a investir em produtos com menor liquidez para obter maiores retornos?')
    liquidez_investimento.pack(padx='10', pady='10', anchor='w')

    liquidez_var = customtkinter.StringVar(value="")

    liquidezcheckbox1 = customtkinter.CTkCheckBox(barra_rolagem, text= 'Alta liquidez', variable= liquidez_var, onvalue= 'Alta liquidez', offvalue= "")
    liquidezcheckbox1.pack(padx='10', pady='10', anchor='w')

    liquidezcheckbox2 = customtkinter.CTkCheckBox(barra_rolagem, text= 'Menor liquidez para maiores retornos', variable= liquidez_var, onvalue= 'Menor liquidez para maiores retornos', offvalue= "")
    liquidezcheckbox2.pack(padx='10', pady='10', anchor='w')

    liquidezcheckbox3 = customtkinter.CTkCheckBox(barra_rolagem, text= 'Não tenho preferência', variable= liquidez_var, onvalue= 'Não tenho preferência', offvalue= "")
    liquidezcheckbox3.pack(padx='10', pady='10', anchor='w')

    preferencia_investimentos = customtkinter.CTkLabel(barra_rolagem, text=' Você prefere investir em ativos que você possa tocar e ver, como imóveis, ou prefere ativos digitais e financeiros?')
    preferencia_investimentos.pack(padx='10', pady='10', anchor='w')

    preferencia_var = customtkinter.StringVar(value= "")

    preferenciacheckbox1 = customtkinter.CTkCheckBox(barra_rolagem, text= 'Ativos tangíveis (ex: imóveis)', variable= preferencia_var, onvalue= 'Ativos tangíveis (ex: imóveis)', offvalue= "")
    preferenciacheckbox1.pack(padx='10', pady='10', anchor='w')

    preferenciacheckbox2 = customtkinter.CTkCheckBox(barra_rolagem, text= 'Ativos digitais e financeiros (ex: ações, criptoativos)', variable= preferencia_var, onvalue= 'Ativos digitais e financeiros (ex: ações, criptoativos)', offvalue= "")
    preferenciacheckbox2.pack(padx='10', pady='10', anchor='w')

    preferenciacheckbox3 = customtkinter.CTkCheckBox(barra_rolagem, text= 'Ambos', variable= preferencia_var, onvalue= 'Ambos', offvalue= "")
    preferenciacheckbox3.pack(padx='10', pady='10', anchor='w')

    preferenciacheckbox4 = customtkinter.CTkCheckBox(barra_rolagem, text= 'Nenhum', variable= preferencia_var, onvalue= 'Nenhum', offvalue= "")
    preferenciacheckbox4.pack(padx='10', pady='10', anchor='w')

    diversidade_investimentos = customtkinter.CTkLabel(barra_rolagem, text= 'Você considera importante diversificar seus investimentos entre diferentes setores e mercados?')
    diversidade_investimentos.pack(padx='10', pady='10', anchor='w')

    diversidade_var = customtkinter.StringVar(value="")

    diversidadecheckbox1 = customtkinter.CTkCheckBox(barra_rolagem, text='Sim, altamente importante', variable= diversidade_var, onvalue= 'Sim, altamente importante', offvalue="")
    diversidadecheckbox1.pack(padx='10', pady='10', anchor='w')

    diversidadecheckbox2 = customtkinter.CTkCheckBox(barra_rolagem, text='Sim, moderadamente importante', variable= diversidade_var, onvalue= 'Sim, moderadamente importante', offvalue= "")
    diversidadecheckbox2.pack(padx='10', pady='10', anchor='w')
    

    diversidadecheckbox3= customtkinter.CTkCheckBox(barra_rolagem, text='Não, prefiro focar em poucos setores', variable= diversidade_var, onvalue= 'Não, prefiro focar em poucos setores', offvalue= "")
    diversidadecheckbox3.pack(padx='10', pady='10', anchor='w')
    
    
    diversidadecheckbox4= customtkinter.CTkCheckBox(barra_rolagem, text= 'Não tenho certeza', variable= diversidade_var, onvalue= 'Não tenho certeza', offvalue="")
    diversidadecheckbox4.pack(padx='10', pady='10', anchor='w')

    startup_investimento = customtkinter.CTkLabel(barra_rolagem, text= 'Você tem interesse em investimentos em startups ou empresas em estágio inicial?')
    startup_investimento.pack(padx='10', pady='10', anchor='w')

    startup_var= customtkinter.StringVar(value= "")

    startupcheckbox1= customtkinter.CTkCheckBox(barra_rolagem, text= 'Sim, estou muito interessado', variable= startup_var, onvalue= 'Sim, estou muito interessado', offvalue= "")
    startupcheckbox1.pack(padx='10', pady='10', anchor='w')

    startupcheckbox2 = customtkinter.CTkCheckBox(barra_rolagem, text= 'Sim, mas com cautela', variable= startup_var, onvalue= 'Sim, mas com cautela', offvalue= "")
    startupcheckbox2.pack(padx='10', pady='10', anchor='w')

    startupcheckbox3 = customtkinter.CTkCheckBox(barra_rolagem, text= 'Não, prefiro empresas estabelecidas', variable= startup_var, onvalue= 'Não, prefiro empresas estabelecidas', offvalue= "")
    startupcheckbox3.pack(padx='10', pady='10', anchor='w')
    

    startupcheckbox4 = customtkinter.CTkCheckBox(barra_rolagem, text= 'Não tenho interesse', variable= startup_var, onvalue= 'Não tenho interesse', offvalue= "")
    startupcheckbox4.pack(padx='10', pady='10', anchor='w')


    info_investimentos = customtkinter.CTkLabel(barra_rolagem, text= 'Você considera importante ter acesso a informações detalhadas e análises sobre seus investimentos?')
    info_investimentos.pack(padx='10', pady='10', anchor='w')

    info_var = customtkinter.StringVar(value= "")

    infocheckbox1 = customtkinter.CTkCheckBox(barra_rolagem, text= 'Sim, é crucial para mim', variable= info_var, onvalue= 'Sim, é crucial para mim', offvalue= "" )
    infocheckbox1.pack(padx='10', pady='10', anchor='w')

    infocheckbox2 = customtkinter.CTkCheckBox(barra_rolagem, text= 'Sim, mas apenas ocasionalmente', variable= info_var, onvalue= 'Sim, mas apenas ocasionalmente', offvalue= "")
    infocheckbox2.pack(padx='10', pady='10', anchor='w')

    infocheckbox3 = customtkinter.CTkCheckBox(barra_rolagem, text= 'Não, confio no gestor de investimentos', variable= info_var, onvalue= 'Não, confio no gestor de investimentos', offvalue= "")
    infocheckbox3.pack(padx='10', pady='10', anchor='w')

    infocheckbox4 = customtkinter.CTkCheckBox(barra_rolagem, text= 'Não, prefiro uma abordagem simplificada', variable= info_var, onvalue= 'Não, prefiro uma abordagem simplificada', offvalue= "")
    infocheckbox4.pack(padx='10', pady='10', anchor='w')

    





    #usar esse botão para iniciar a função de calcular o resultado do perfil dps
    avancar_tela = customtkinter.CTkButton(barra_rolagem, text= 'Avançar para próxima página',
                                            command= cadastrarRespostas)
    avancar_tela.pack(padx='10', pady='10')




janela.mainloop()