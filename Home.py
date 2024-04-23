from streamlit_gsheets import GSheetsConnection
import streamlit as st
from streamlit import session_state as ss

st.set_page_config(
    page_title='Busca OLX',
    page_icon='🏠',
    layout='wide')

#@st.cache_data
def ldData(data):
    Sheet0 = st.secrets['gsheets']['Sheet1']
    cnnct = st.connection('gsheets', type=GSheetsConnection)
    ss['df'] = cnnct.read(spreadsheet=Sheet0, worksheet=data, usecols=list(range(16)), ttl=0)
    ss['df'] = ss['df'].dropna(how='all')
    return ss['df']

ss['df'] = ldData('olx')

bairros = list(set(ss['df']['bairro']))
bairros.append('Todas as opções')

tipo = list(set(ss['df']['casa_apt']))
tipo.append('Todas as opções')

g = list(set(ss['df']['garagem']))

st.write('Filtrar')

brr = st.selectbox('Bairros para filtrar', options=bairros, index=len(bairros)-1)
und = st.selectbox('Tipo de unidade', options=tipo, index=len(tipo)-1)
vlr = st.number_input('Filtrar por valor total (Aluguel + Cond + IPTU)', min_value=min(ss['df']['soma']), max_value=max(ss['df']
['soma']), step=float(100))
grgm = st.selectbox('Pelo menos', options=g, index=len(g)-1)

ld = st.button('carregar', type='primary')
if ld:
    if brr != 'Todas as opções':
        ss['df'] = ss['df'][ss['df']['bairro'] == brr ]

    if und != 'Todas as opções':
        ss['df'] = ss['df'][ss['df']['casa_apt'] == und ]

    if vlr:
        ss['df'] = ss['df'][ss['df']['soma'] <= vlr ]

    if grgm:
        ss['df'] = ss['df'][ss['df']['garagem'] <= grgm ]
 
    st.data_editor(
        ss['df'],
        num_rows='fixed',
        use_container_width=True,
        column_config={
            'link': st.column_config.LinkColumn('Link', disabled=True),
            'a+c+i_R$': st.column_config.Column('Alug + Cond + IPTU', disabled=True),
            'area': st.column_config.Column('Área', disabled=True),
            'q+b':st.column_config.Column('Quar. e Ban.', disabled=True),
            'vantagens_casa': st.column_config.Column('Básico', disabled=True),
            'vantagens_cond': st.column_config.Column('Comodidades', disabled=True),
            },
        column_order=['link', 'a+c+i_R$', 'area','q+b', 'vantagens_casa','vantagens_cond'],
        hide_index=True,
        key=99,)
