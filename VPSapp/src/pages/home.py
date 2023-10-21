#-*- coding:utf-8 -*-

import pandas as pd
import dash
from dash import dcc
from dash import html, register_page
import dash_bootstrap_components as dbc
from dash import Input, Output, callback
import plotly.graph_objects as go
import plotly.express as px


# 시기별 버블 크기 데이터
quarter = ['Q1', 'Q1', 'Q1', 'Q1', 'Q2', 'Q2', 'Q2', 'Q2', 'Q3', 'Q3', 'Q3', 'Q3']
big_cls = ["연관이슈", "정치권 대응", "정치권 대응 문제", "이슈 현황"]*3
#big_count = [447, 540, 468, 585, 1065, 1536, 955, 1092, 2092, 2202, 3550, 2173]
big_count = [44, 54, 46, 58, 106, 153, 95, 109, 209, 220, 355, 217]
home = pd.DataFrame([quarter, big_cls, big_count]).T
home.columns = ['quarter', 'big_cls', 'count']
home['idx'] = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]

layout_home = html.Div([
dbc.Container([html.Br(), html.Br(), html.Br(), html.Br()],),

    dbc.Container([
        dbc.Row(
        [dbc.Col(html.Img(id='home-temp', style={"height":"450px", "padding-right":20, "margim-right":30}), md=2),

            dbc.Col([dcc.Graph(id='home-clust'),
         html.Div([dcc.Slider(1, 3, value=1, step=1,
                              marks={1:{'label':'Q1'}, 2:{'label':'Q2'}, 3:{'label':'Q3'}},
                              id = 'home-slider')
                  ],style={"marginTop":"20px"})],
                 style={"padding-left":1, "padding-right":10, "padding-bottom":10, "padding-top":2, "marginTop":"5px"}
                 , md=4),
         dbc.Col([
             dbc.Row([dcc.Graph(id='home-donut')], style={'height':'30%'}),
            dbc.Row(id='home-cards', style={'height':'50%'})
            ],
                 style={"padding-left":10, "padding-right":10, "padding-bottom":10, "padding-top":2, "marginTop":"1px"},
                 md=6),
         ], style={"height":"500px","padding-left":1, "padding-right":10, "padding-bottom":10, "padding-top":10, "margin-left":1})
    ],fluid=True),
],)

@callback(Output('home-clust', 'figure'),Input('home-slider', 'value'))
def home_update_clust(selected_qt):
    selected_qt = 'Q'+str(selected_qt)
    data = home[home['quarter']==selected_qt]

    data['x'] = [-7.5, -4, 2.5, 7.5]
    data['y'] = [-6.5, 6, -2.5, 6.5]
    fig = go.Figure(go.Scatter(x=data['x'], y=data['y'], mode='markers+text', customdata=data['idx'],
                                   text=data['big_cls'], textposition="middle center", textfont=dict(size=15),
                                   marker=dict(size=data['count'].tolist(), color=['#2772db', '#2eb872', '#facf5a', '#ff5959']),
                                   ))

    fig.update_layout(go.Layout(paper_bgcolor='#ededed', plot_bgcolor='#ededed'))

    fig.update_xaxes(range=[-13, 13], title=None, showticklabels=False, showgrid=False)
    fig.update_yaxes(range=[-13, 13], title=None, showticklabels=False, showgrid=False)
    fig.update_layout({'margin': {'l': 10, 'b': 10, 't': 10, 'r': 10}})
    fig.update_coloraxes(showscale=False)
    fig.update_layout(showlegend=False)
    fig.update_layout(clickmode='event+select')
    return fig

@callback(Output('home-donut', 'figure'), Input('home-clust', 'clickData'))
def home_update_donut(clickData):
    if clickData is None:
        fig = go.Figure(go.Scatter(x=[0], y=[0], mode='text', textfont=dict(size=20),
                                   text=['좌측 그림에서 흥미로운 군집을 클릭해주세요']))
        fig.update_layout({'margin': {'l': 10, 'b': 10, 't': 1, 'r': 10}})
        fig.update_xaxes(range=[-10, 10], title=None, showticklabels=False, showgrid=False, zeroline=False)
        fig.update_yaxes(range=[-5, 5], title=None, showticklabels=False, showgrid=False, zeroline=False)
        return fig

    else:
        n = clickData['points'][0]['customdata']
        if n in [2, 6, 10]:
            if n == 2 :
                data = [124, 170, 174]
            elif n == 6 :
                data = [220, 392, 343]
            else :
                data = [643, 1814, 1093]

            labels = ["방안 지적", "대응 촉구", "이외"]
            data = pd.DataFrame([data, labels]).T
            data.columns = ['data', 'labels']

            fig = px.bar(data, x='data', y='labels', color='labels',
                         text='labels', orientation='h')
            fig.update_layout({'margin': {'l': 10, 'b': 10, 't': 1, 'r': 10}})
            fig.update_layout(showlegend=False)
            fig.update_yaxes(title=None, showgrid=True, showticklabels=False)
            fig.update_xaxes(title=None, showgrid=True, showticklabels=False)
            return fig

        elif n in [0, 4, 8]:
            if n == 0:
                data = [330, 302, 274, 259]
                labels = ['사면법', '정부대표 및 특별사절의 임명과 권한에 관한 법률', '국가배상법',
                         '수출용 원재료에 대한 관세 등 환급에 관한 특례법']

            elif n == 4:
                data = [760, 671, 609, 571]
                labels = ['사면법', '정부대표 및 특별사절의 임명과 권한에 관한 법률',
                          '수출용 원재료에 대한 관세 등 환급에 관한 특례법', '국가배상법']

            elif n == 8:
                data = [1429, 1311, 1136, 1125]
                labels = ['사면법', '정부대표 및 특별사절의 임명과 권한에 관한 법률', '국가배상법',
                          '수출용 원재료에 대한 관세 등 환급에 관한 특례법']

            data = pd.DataFrame([data, labels]).T
            data.columns = ['data', 'labels']

            fig = px.bar(data, x='data', y='labels', color='labels',
                         text='labels', orientation='h')
            fig.update_layout({'margin': {'l': 10, 'b': 10, 't': 1, 'r': 10}})
            fig.update_layout(showlegend=False)
            fig.update_yaxes(title=None, showgrid=True, showticklabels=False)
            fig.update_xaxes(title=None, showgrid=True, showticklabels=False)
            return fig

        elif n in [1, 5, 9]:
            fig = go.Figure(go.Scatter(x=[0], y=[0], mode='text', textfont=dict(size=20),
                                       text=['"정치권 대응" 관련 세부분석은 제공되지 않습니다']))
            fig.update_layout({'margin': {'l': 10, 'b': 10, 't': 1, 'r': 10}})
            fig.update_xaxes(range=[-10, 10], title=None, showticklabels=False, showgrid=False, zeroline=False)
            fig.update_yaxes(range=[-5, 5], title=None, showticklabels=False, showgrid=False, zeroline=False)
            return fig

        else :
            fig = go.Figure(go.Scatter(x=[0], y=[0], mode='text', textfont=dict(size=20),
                                       text=['"이슈 현황" 관련 세부분석은 제공되지 않습니다']))
            fig.update_layout({'margin': {'l': 10, 'b': 10, 't': 1, 'r': 10}})
            fig.update_xaxes(range=[-10, 10], title=None, showticklabels=False, showgrid=False, zeroline=False)
            fig.update_yaxes(range=[-5, 5], title=None, showticklabels=False, showgrid=False, zeroline=False)
            return fig

@callback(Output('home-cards', 'children'),Input('home-clust', 'clickData'))
def home_update_cards(clickData):
    if clickData is None:
        cards = dbc.Card([dbc.CardBody([html.P("")])],
                         style={"margin-top": 40, "margin-left": 20, "margin-right": 50, "margin-bottom": 10})
        return cards

    else:
        n = clickData['points'][0]['customdata']
        if n == 2:
            cards = dbc.Card([
                    dbc.CardBody(
                        [html.P([dbc.Button(['전세사기 대책'], n_clicks=0, disabled=True, size='sm',
                                            style={"background-color": "#862B0D", "outline": False, "border-radius": "10px"}), ' ',
                                 dbc.Button(['임대보증금 반환 보험 사고 집중'], n_clicks=0, disabled=True, size='sm',
                                             style={"background-color": "#862B0D", "outline":False, "border-radius": "10px"}), ' ',
                                    dbc.Button(['HUG 사장 사임 및 감사'], n_clicks=0, disabled=True, size='sm',
                                            style={"background-color": "#862B0D", "outline":False, "border-radius": "10px"})]),
                         html.Hr(),
                         html.H4('핵심 요약문'),
                         html.P(
                             '국회 국토교통위원회의 국정감사에서는 전세사기 문제에 대한 즉각적인 대책 마련이 필요하다는 의견이 제기되었습니다. 특히, 임대보증금 반환 보험 사고가 5개 법인에서 90% 이상 집중 발생하였으나, 이에 대한 회수율은 약 35%로 불충분하다는 지적이 있습니다. 또한, 전세 보증 사고 건수와 금액이 급증하는 가운데 주택도시보증공사(HUG)의 회수율은 하락하는 추세를 보여 문제의 심각성을 더욱 부각시켰습니다. 마지막으로, HUG 사장의 중도 사임과 관련하여 국토부가 표적 감사를 통해 압박을 가하였나라는 의혹이 제기되었습니다. 이에 따라 감사 과정과 그 결과에 대한 정확성과 공정성을 요구하는 목소리가 높아지고 있습니다.'
                         )],
                    )
                ], style={"margin": 20})
            return cards

        elif n == 6:
            cards = dbc.Card([
                dbc.CardBody(
                    [html.P([dbc.Button(['전세사기 피해자 구제'], n_clicks=0, disabled=True, size='md',
                                            style={"background-color": "#862B0D", "outline": False, "border-radius": "10px"}), '   ',
                             dbc.Button(['감사원 공익감사 청구'], n_clicks=0, disabled=True, size='md',
                                        style={"background-color": "#862B0D", "outline": False, "border-radius": "10px"}),]),
                    html.P([dbc.Button(['긴급 지원 주택 임시거주기간 연장 및 저리 대환 대출 요건 완화'], n_clicks=0, disabled=True, size='md',
                            style={"background-color": "#862B0D", "outline": False, "border-radius": "10px"}),]),
                     html.Hr(),
                     html.H4('핵심 요약문'),
                     html.P(
                         '전세사기 피해자들과 시민단체들은 정부에 적극적인 피해 구제를 촉구하고 있습니다. 그들은 긴급 지원 주택의 임시 거주 기간을 연장하고, 저리 대환 대출의 요건을 완화하는 것 등을 요구하며, 전세 사기 문제를 사회적 재난으로 인식하고 이에 맞는 대책을 마련할 것을 촉구하였습니다. 또한, 참여연대는 전세대출 규제 강화와 정보 격차 해소, 등록임대사업자 관리·감독 강화 등이 필요함을 지적하며 금융당국과 국토부, 그리고 일부 지자체에 대한 감사원 공익감사를 청구했습니다. 이는 무분별한 전세대출 거품과 과도한 보증 한도가 방치되어 전세 사기와 깡통 주택이 양산된 것에 대한 책임 소재를 명확히 하려는 시도로 볼 수 있습니다.'                 )],
                )
            ], style={"margin": 20})
            return cards

        elif n == 10:
            cards = dbc.Card([
                dbc.CardBody(
                    [html.P([dbc.Button(['전세사기 피해자 지원 특별법'], n_clicks=0, disabled=True, size='md',
                                            style={"background-color": "#862B0D", "outline": False, "border-radius": "10px"}),]),
                     html.P([dbc.Button(['보증금반환채권 매입'], n_clicks=0, disabled=True, size='md',
                                            style={"background-color": "#862B0D", "outline": False, "border-radius": "10px"}), '  ',
                             dbc.Button(['공공임대주택 예산 확대'], n_clicks=0, disabled=True, size='md',
                                        style={"background-color": "#862B0D", "outline": False, "border-radius": "10px"})
                             ]),
                     html.Hr(),
                     html.H4('핵심 요약문'),
                     html.P(
                         "전전세사기 피해자 지원단체들과 전문가들은 정부가 추진하는 ‘전세사기 피해자 지원 특별법’에 대한 평가가 엇갈리고 있습니다. 그들은 경매 유예와 피해주택 공공매입 방침을 긍정적으로 평가하면서도, 이와 병행하여 보증금 반환 채권의 매입과 공공임대주택 예산 확대를 함께 이루어져야 한다고 주장하였습니다. 또한, 전문가들은 '빚내서 집 사라'는 기존 정책이 전세 대출 폭증을 일으키는 원인이 되었다며, 이런 점을 반영하여 정책 개선이 필요하다는 의견을 제시하였습니다."
                         )],
                )
            ], style={"margin": 20})
            return cards

        elif n == 0:
            cards = dbc.Card([dbc.CardImg(src='assets/img6.jpg', style={"width":"100%"})], style={"margin": 20},
                             className="border-0 bg-transparent")
            return cards

        elif n == 4:
            cards = dbc.Card([dbc.CardImg(src='assets/img7.jpg', style={"width":"100%"})], style={"margin": 20},
                             className="border-0 bg-transparent")
            return cards

        elif n == 8:
            cards = dbc.Card([dbc.CardImg(src='assets/img8.jpg', style={"width":"100%"})], style={"margin": 20},
                             className="border-0 bg-transparent")
            return cards

        else:
            cards = dbc.Card([dbc.CardBody([html.P("")])],
                             style={"margin-top": 40, "margin-left":20, "margin-right":50, "margin-bottom":10})
            return cards

@callback(Output('home-temp', 'src'), Input('home-slider', 'value'))
def home_upadate_temp(selected_qt):
    src = 'assets/home_'+str(selected_qt)+'.png'
    return src

'''@callback(Output('home-words', 'src'), Input('home-slider', 'value'))
def nurse_upadate_wd(selected_qt):
    src = selected_qt + 5
    src = 'assets/img'+str(src)+'.jpg'
    return src
'''

register_page(
    __name__,
    name='Home',
    top_nav=True,
    path='/',
    layout=layout_home
)
