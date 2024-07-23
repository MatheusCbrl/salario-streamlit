import streamlit as st
import pandas as pd
import plotly.express as px
#from datetime import datetime

def calcular_salario_liquido(salario_bruto, dependentes, plano_saude_empresa, plano_saude_funcionario, outros_descontos, beneficios):
    # Cálculo do INSS
    if salario_bruto <= 1412.00:
        inss = salario_bruto * 0.075
        aliquota_inss = "7,5%"
    elif salario_bruto <= 2666.68:
        inss = salario_bruto * 0.09 - 18.18
        aliquota_inss = "9,0%"
    elif salario_bruto <= 4000.03:
        inss = salario_bruto * 0.12 - 91.00
        aliquota_inss = "12,0%"
    elif salario_bruto <= 7786.02:
        inss = salario_bruto * 0.14 - 163.82
        aliquota_inss = "14,0%"
    else:
        inss = 908.85
        aliquota_inss = "TETO"

    # Cálculo do IRRF
    base_irrf = salario_bruto - inss - (dependentes * 189.59)
    if base_irrf <= 2259.21:
        irrf = 0
        aliquota_ir = "ISENTO"
    elif base_irrf <= 2828.65:
        irrf = base_irrf * 0.075 - 169.44
        aliquota_ir = "7,5%"
    elif base_irrf <= 3751.05:
        irrf = base_irrf * 0.15 - 381.44
        aliquota_ir = "15,0%"
    elif base_irrf <= 4664.68:
        irrf = base_irrf * 0.225 - 662.77
        aliquota_ir = "22,5%"
    else:
        irrf = base_irrf * 0.275 - 896.00
        aliquota_ir = "27,5%"

    # Calculo de descontos e proventos
    total_descontos = inss + irrf + plano_saude_funcionario + outros_descontos
    salario_liquido = salario_bruto - total_descontos + beneficios

    # DataFrame para a tabela
    df = pd.DataFrame({
        'Descrição': ['Salário Bruto', 'Benefícios', 'INSS', 'IRRF', 'Plano de Saúde (Funcionário)', 'Outros Descontos', 'Total'],
        'Alíquota Aplicada': ['-', '-', aliquota_inss,aliquota_ir, '-', '-', '-'],
        'Alíquota Real': ['-', '-', f'{(inss/salario_bruto)*100:.2f}%', f'{(irrf/salario_bruto)*100:.2f}%', '-', '-', '-'],
        'Proventos': [f'{salario_bruto:.2f}', f'{beneficios:.2f}', '-', '-', '-', '-', f'{salario_liquido:.2f}'],
        'Descontos': ['-','-', f'{inss:.2f}', f'{irrf:.2f}', f'{plano_saude_funcionario:.2f}', f'{outros_descontos:.2f}', f'{total_descontos:.2f}']
    })

    return df, salario_liquido, total_descontos

def calcular_rescisao(salario_bruto, data_admissao, data_demissao, aviso_previo, ferias_vencidas, salario_familia, outros_descontos):
    # Calculos simplificados de rescisão
    # Apenas exemplos, adicionar regras reais para cada tipo de cálculo
    #data_admissao = datetime.strptime(data_admissao, "%d-%m-%Y")
    #data_demissao = datetime.strptime(data_demissao, "%d-%m-%Y")
    tempo_trabalho = (data_demissao - data_admissao).days / 30
    saldo_salario = (data_demissao.day / 30) * salario_bruto
    if aviso_previo == 'Trabalhado':
        aviso_previo = salario_bruto
    else:
        aviso_previo = 0
        
    decimo_terceiro = (tempo_trabalho / 12) * salario_bruto
    ferias_proporcionais = (tempo_trabalho / 12) * (salario_bruto + 1/3 * salario_bruto)
    ferias_vencidas = salario_bruto / 3 * (tempo_trabalho / 12)
    fgts = salario_bruto * 0.08 * tempo_trabalho
    total_rescisao = saldo_salario + aviso_previo + decimo_terceiro + ferias_proporcionais + ferias_vencidas + fgts
    #return total_rescisao, saldo_salario, aviso_previo, decimo_terceiro, ferias_proporcionais, ferias_vencidas, fgts

    # DataFrame para a tabela
    df_rescisao = pd.DataFrame({
        'Descrição': ['Salário Bruto', 'Aviso Prévio', 'FGTS', 'Décimo Terceiro', 'Férias', 'Outros Descontos', 'Total Rescisão'],
        'Valor': [f'{salario_bruto:.2f}', f'{aviso_previo:.2f}', f'{fgts:.2f}', f'{decimo_terceiro:.2f}', f'{ferias_proporcionais:.2f}', f'{outros_descontos:.2f}', f'{total_rescisao:.2f}']
    })

    return df_rescisao, total_rescisao

# Configuração da interface do Streamlit
def main():
    st.set_page_config(page_title="Calculadora",page_icon=":books:")
    st.title("Cálculo de Salário Líquido e Rescisão de Contrato :books:")  

    with st.sidebar:
        st.markdown(
            "## Como Usar:\n"
            "1. Insira o valor de salário bruto\n"
            "2. Adicione as informações que achar necessária e clique em calcular! 💬\n")
        st.markdown("---")
        # Inputs do usuário para o salário líquido
        
        st.title('Salário Líquido')
        with st.expander('Informar os dados:'):
            salario_bruto = st.number_input('Salário Bruto', min_value=0.0, value = 0.00, format="%.2f")
            dependentes = st.number_input('Número de Dependentes', min_value=0, step=1)
            plano_saude_empresa = st.number_input('Plano de Saúde (Empresa)', min_value=0.0, format="%.2f")
            plano_saude_funcionario = st.number_input('Plano de Saúde (Funcionário)', min_value=0.0, format="%.2f")
            outros_descontos = st.number_input('Outros Descontos', min_value=0.0, format="%.2f")
            beneficios = st.number_input('Benefícios', min_value=0.0, format="%.2f")
        st.markdown("---")
        st.title('Cálculo de Rescisão')
        with st.expander('Informar os dados:'):
            data_admissao = st.date_input('Data de Admissão')
            data_demissao = st.date_input('Data de Demissão')
            aviso_previo = st.selectbox("Tipo de Aviso Prévio", ["Trabalhado", "Indenizado"])
            tem_ferias_vencidas = st.checkbox("Possui Férias Vencidas?")
            ferias_vencidas = st.slider("Dias de Férias Vencidas", 1, 30) if tem_ferias_vencidas else 0
            salario_familia = st.number_input('Salário-Família', value=0.00)
            outros_descontos_rescisao = st.number_input('Outros Descontos', value=0.00)
        st.markdown("---")
        with st.expander('Informações Importantes📄'):
            st.write('INSS: Contribuição ao Instituto Nacional do Seguro Social.')
            st.write('IR: Imposto de Renda.')
            st.write('FGTS: Fundo de Garantia do Tempo de Serviço.')
            st.write('Aviso Prévio: Indenização em caso de demissão sem justa causa.')
            st.write('13º Salário: Abono anual proporcional ao tempo de serviço.')
            st.write('Férias Vencidas: Pagamento proporcional às férias não gozadas.')
        st.markdown("---")
        st.write('Eng. IA: Matheus Cabral.')
        
    col1, col2 = st.columns(2)   
    #st.header('Cálculo de Salário Líquido')
    if col1.button('Calcular Salário Líquido'):
        df, salario_liquido, total_descontos = calcular_salario_liquido(salario_bruto, dependentes, plano_saude_empresa, plano_saude_funcionario, outros_descontos, beneficios)
        st.subheader('Resultados')
        st.success('Cálculo realizado com sucesso!')
    
        #cards tipo BI
        col1, col2, col3 = st.columns(3)
        col1.metric(label="Salário Bruto", value=f'R$ {salario_bruto:.2f}', delta='100%')
        col2.metric(label="Total Descontos", value=f'R$ {total_descontos:.2f}', delta=f'-{total_descontos *100 / salario_bruto :.2f}%')
        col3.metric(label="Salário Liquido", value=f'R$ {salario_liquido:.2f}', delta=f'{salario_liquido *100 / salario_bruto :.2f}%')
        #Tabela de Calculos
        with st.container():
            st.dataframe(data=df, use_container_width=True)
        #st.write(df)
        
        #Gráfico
        fig = px.pie(
            values=[f'{salario_liquido:.2f}', f'{total_descontos:.2f}'], 
            names=['Salário Líquido', 'Total Descontos'], 
            color_discrete_sequence=["#008000", "#ff3d00"],
            height=400,
            width=400)
        st.plotly_chart(fig)
        # Inputs do usuário para a rescisão de contrato
    #st.header('Cálculo de Rescisão de Contrato')
    if col2.button('Calcular Rescisão'):
        if data_demissao > data_admissao:
            df_rescisao, total_rescisao = calcular_rescisao(salario_bruto, data_admissao, data_demissao, aviso_previo, ferias_vencidas, salario_familia, outros_descontos_rescisao)
            st.subheader('Resultados da Rescisão')
            st.success('Cálculo de rescisão realizado com sucesso!')
            st.write(df_rescisao)
            #cards tipo BI
            st.metric(label="Total a Receber", value=f'R$ {total_rescisao:.2f}', delta='100%',help='Valor final a receber não somando fgts(multa 40%)')


if __name__ == '__main__':
    main()