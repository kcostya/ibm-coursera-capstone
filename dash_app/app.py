from datetime import datetime as dt
import json

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from sklearn.preprocessing import LabelBinarizer, LabelEncoder, StandardScaler
import pandas as pd
import pickle
from sklearn_pandas import DataFrameMapper, gen_features

from utils import ColumnSelector, preprocess, add_datepart

# Load external stylesheets to make things pretty
external_stylesheets = ['https://codepen.io/kcostya/pen/QRMJzR.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.config['suppress_callback_exceptions']=True

# Load the trained pre-processing and predicting pipeline
with open('pipeline.pickle', 'rb') as pkl:
    pipeline = pickle.load(pkl)

# DatetimeFormat returned from dash date-selector
datetimeFormat = '%Y-%m-%d'

# Booking date (today's date)
booking_date = dt.now().strftime('%m/%d/%Y')

# Dicitionary of avaiable regions and states
region_options = {
'1': ['1', '6', '11', '4'],
'2': ['2', '7', '9', '10', '13'],
'3': ['3', '5']
}

# Dictionary of states and resorts
resort_options = {
'1': ['6b86b273ff34fce19d6b804eff5a3f5747ada4eaa22f1d49c01e52ddb7875b4b',
  'c75cb66ae28d8ebc6eded002c28a8ba0d06d3a78c6b5cbf9b2ade051f0775ac4',
  '535fa30d7e25dd8a49f1536779734ec8286108d115da5045d77f3b4185d8f790',
  'c6f3ac57944a531490cd39902d0f777715fd005efac9a30622d5f5205e7f6894',
  '81b8a03f97e8787c53fe1a86bda042b6f0de9b0ec9c09357e107c99ba4d6948a',
  '48449a14a4ff7d79bb7a1b6f3d488eba397c36ef25634c111b49baf362511afc'],
 '2': ['d4735e3a265e16eee03f59718b9b5d03019c07d8b6c51f90da3a666eec13ab35',
  '6208ef0f7750c111548cf90b6ea1d0d0a66f6bff40dbef07cb45ec436263c7d6',
  '98a3ab7c340e8a033e7b37b6ef9428751581760af67bbab2b9e05d4964a8874a'],
 '3': ['9f14025af0065b30e47e23ebb3b491d39ae8ed17d33739e5ff3827ffb3634953',
  '3e1e967e9b793e908f8eae83c74dba9bcccce6a5535b4b462bd9994537bfe15c',
  'ef2d127de37b942baad06145e54b0c619a1f22327b2ebbcfbec78f5564afe39d',
  'f5ca38f748a1d6eaf726b8a42fb575c3c71f1864a8143301782de13da2d9202b',
  '7f2253d7e228b22a08bda1f09c516f6fead81df6536eb02fa991a34bb38d9be8',
  '4e07408562bedb8b60ce05c1decfe3ad16b72230967de01f640b7e4729b49fce'],
 '4': ['e7f6c011776e8db7cd330b54174fd76f7d0216b612387a5ffcfb81e6f0919683',
  '4b227777d4dd1fc61c6f884f48641d02b4d121d3fd328cb08b5531fcacdabf8a',
  '3fdba35f04dc8c462986c992bcf875546257113072a909c162f7e470e581e278'],
 '5': ['4ec9599fc203d176a301536c2e091a19bc852759b255bd6818810a42c5fed14a',
  '7902699be42c8a8e46fbbb4501726517e86b22c56a189f7625a6da49081b2451',
  '670671cd97404156226e507973f2ab8330d3022ca96e0c93bdbdb320c41adcaf',
  '39fa9ec190eee7b6f4dff1100d6343e10918d044c75eac8f9e9a2596173f80c9'],
 '6': ['b17ef6d19c7a5b1ee83b907c595526dcb1eb06db8227d650d5dda0a9f4ce8cd9',
  '49d180ecf56132819571bf39d9b7b342522a2ac6d23c1418d3338251bfe469c8'],
 '7': ['9400f1b21cb527d7fa3d3eabba93557a18ebe7a2ca4e471cfe5e4c5b4ca7f767',
  'da4ea2a5506f2693eae190d9360a1f31793c98a1adade51d93533a6f520ace1c'],
 '9': ['624b60c58c9d8bfb6ff1886c2fd605d2adeb6ea4da576068201b6c6958ce93f4',
  'ff5a1ae012afa5d4c889c50ad427aaf545d31a4fac04ffc1c4d03d403ba4250a',
  'a68b412c4282555f15546cf6e1fc42893b7e07f271557ceb021821098dd66c1b'],
 '10': ['0b918943df0962bc7a1824c0555a389347b4febdc7cf9d1254406d80ce44e3f9'],
 '11': ['e29c9c180c6279b0b02abd6a1801c7c04082cf486ec027aa13515e4f3884bb6b'],
 '13': ['8722616204217eddb39e7df969e0698aed8e599ba62ed2de1ce49b03ade0fede']
 }

# Sample input to predict the F&B spend
# (this will be updated with input from forms)
sample_input = pd.DataFrame([
{'booking_date': '02/09/16',
  'booking_type_code': 1,
  'channel_code': 1,
  'checkin_date': '08/10/16',
  'checkout_date': '21/10/18',
  'cluster_code': 'F',
  'main_product_code': 2,
  'member_age_buckets': 'D',
  'numberofadults': 2,
  'numberofchildren': 0,
  'persontravellingid': 45,
  'reservationstatusid_code': 'A',
  'resort_id': 'd4735e3a265e16eee03f59718b9b5d03019c07d8b6c51f90da3a666eec13ab35',
  'resort_region_code': 1,
  'resort_type_code': 1,
  'room_type_booked_code': 3,
  'roomnights': 3,
  'season_holidayed_code': 2.0,
  'state_code_residence': 8.0,
  'state_code_resort': 1,
  'total_pax': 2}
  ])

# Dictionary mapping state to the resort_id
resort_state_dict = {
  '0b918943df0962bc7a1824c0555a389347b4febdc7cf9d1254406d80ce44e3f9': 10,
  '39fa9ec190eee7b6f4dff1100d6343e10918d044c75eac8f9e9a2596173f80c9': 5,
  '3e1e967e9b793e908f8eae83c74dba9bcccce6a5535b4b462bd9994537bfe15c': 3,
  '3fdba35f04dc8c462986c992bcf875546257113072a909c162f7e470e581e278': 4,
  '48449a14a4ff7d79bb7a1b6f3d488eba397c36ef25634c111b49baf362511afc': 1,
  '49d180ecf56132819571bf39d9b7b342522a2ac6d23c1418d3338251bfe469c8': 6,
  '4b227777d4dd1fc61c6f884f48641d02b4d121d3fd328cb08b5531fcacdabf8a': 4,
  '4e07408562bedb8b60ce05c1decfe3ad16b72230967de01f640b7e4729b49fce': 3,
  '4ec9599fc203d176a301536c2e091a19bc852759b255bd6818810a42c5fed14a': 5,
  '535fa30d7e25dd8a49f1536779734ec8286108d115da5045d77f3b4185d8f790': 1,
  '6208ef0f7750c111548cf90b6ea1d0d0a66f6bff40dbef07cb45ec436263c7d6': 2,
  '624b60c58c9d8bfb6ff1886c2fd605d2adeb6ea4da576068201b6c6958ce93f4': 9,
  '670671cd97404156226e507973f2ab8330d3022ca96e0c93bdbdb320c41adcaf': 5,
  '6b86b273ff34fce19d6b804eff5a3f5747ada4eaa22f1d49c01e52ddb7875b4b': 1,
  '7902699be42c8a8e46fbbb4501726517e86b22c56a189f7625a6da49081b2451': 5,
  '7f2253d7e228b22a08bda1f09c516f6fead81df6536eb02fa991a34bb38d9be8': 3,
  '81b8a03f97e8787c53fe1a86bda042b6f0de9b0ec9c09357e107c99ba4d6948a': 1,
  '8722616204217eddb39e7df969e0698aed8e599ba62ed2de1ce49b03ade0fede': 13,
  '9400f1b21cb527d7fa3d3eabba93557a18ebe7a2ca4e471cfe5e4c5b4ca7f767': 7,
  '98a3ab7c340e8a033e7b37b6ef9428751581760af67bbab2b9e05d4964a8874a': 2,
  '9f14025af0065b30e47e23ebb3b491d39ae8ed17d33739e5ff3827ffb3634953': 3,
  'a68b412c4282555f15546cf6e1fc42893b7e07f271557ceb021821098dd66c1b': 9,
  'b17ef6d19c7a5b1ee83b907c595526dcb1eb06db8227d650d5dda0a9f4ce8cd9': 6,
  'c6f3ac57944a531490cd39902d0f777715fd005efac9a30622d5f5205e7f6894': 1,
  'c75cb66ae28d8ebc6eded002c28a8ba0d06d3a78c6b5cbf9b2ade051f0775ac4': 1,
  'd4735e3a265e16eee03f59718b9b5d03019c07d8b6c51f90da3a666eec13ab35': 2,
  'da4ea2a5506f2693eae190d9360a1f31793c98a1adade51d93533a6f520ace1c': 7,
  'e29c9c180c6279b0b02abd6a1801c7c04082cf486ec027aa13515e4f3884bb6b': 11,
  'e7f6c011776e8db7cd330b54174fd76f7d0216b612387a5ffcfb81e6f0919683': 4,
  'ef2d127de37b942baad06145e54b0c619a1f22327b2ebbcfbec78f5564afe39d': 3,
  'f5ca38f748a1d6eaf726b8a42fb575c3c71f1864a8143301782de13da2d9202b': 3,
  'ff5a1ae012afa5d4c889c50ad427aaf545d31a4fac04ffc1c4d03d403ba4250a': 9
  }

# Dash app layoout
app.layout = html.Div([ # big block
    html.H1('Food and Beverages Spend Prediction'),
    html.Hr(),

    html.H5('Booking date: {}'.format(booking_date)),

    html.H5('Reservation dates:'),
    dcc.DatePickerRange(
    id='date-picker-range',
    min_date_allowed = dt(2019, 5, 19),
    start_date_placeholder_text="Start Period",
    end_date_placeholder_text="End Period"
    ),

    html.Div(id='output-container-date-picker-range'),

    html.Hr(),

    html.Div([ #bigger block
    html.Div([ #smaller left
    html.H5('Number of adults'),
    dcc.Dropdown(
    id='numberadults-dropdown',
    options=[{'label': k, 'value': k} for k in range(1, 30)],
    value='2',
    clearable=False)
    ],
    style={'width': '20%', 'display': 'inline-block', 'vertical-align': 'top'}
    ),
    html.Div([ #smaller left
    html.H5('Number of children'),
    dcc.Dropdown(
    id='numberchildren-dropdown',
    options=[{'label': k, 'value': k} for k in range(0, 30)],
    value='0',
    clearable=False)
    ],
    style={'width': '20%', 'display': 'inline-block', 'vertical-align': 'top',
    'margin-left': '1em'}
    ),
    ]),
    html.Div(id='output-container-numberofpeople'),

    html.Hr(),

    html.Div([ # smaller left
    html.H5('Region'),
    dcc.RadioItems(
    id='regions-dropdown',
    options=[{'label': k, 'value': k} for k in region_options.keys()],
    value='1'
    )],
    style={'width': '10%', 'display': 'inline-block'}),

    html.Div([ # smaller block right
    html.H5('State'),
    dcc.Dropdown(id='states-dropdown', clearable=False, multi=True)
    ],
    style={
    'width': '20%', 'display': 'inline-block', 'vertical-align': 'top'
    }
    ),

    html.Div([ # smaller block right most
    html.H5('Resort'),
    dcc.Dropdown(id='resorts-dropdown', clearable=False)],
    style={'width': '50%', 'display': 'inline-block', 'vertical-align': 'top',
    'margin-left': '1em'}),

    html.Div(id='display-selected-values',
    style={'margin-top': '1em'}),

    html.Hr(),
    html.H5('Spend prediction'),
    # Hidden div inside the app that stores the intermediate value
    html.Div(id='intermediate-value', style={'display': 'none'}),

    # Display prediction
    html.Div(id='display-prediction',
    style={'font-size': 20})

])

# Dash app callbacks
@app.callback(
    Output('output-container-date-picker-range', 'children'),
    [Input('date-picker-range', 'start_date'),
     Input('date-picker-range', 'end_date')])
def update_output(start_date, end_date):
    string_prefix = "You have selected "
    if start_date is not None and end_date is not None:
        start = dt.strptime(start_date, datetimeFormat)
        end = dt.strptime(end_date, datetimeFormat)
        diff = end - start
        string_prefix = string_prefix + str(diff.days) +" nights reservation."
    if string_prefix == "You have selected ":
        return 'Select dates of the reservation'
    else:
        return string_prefix

@app.callback(
    Output('output-container-numberofpeople', 'children'),
    [Input('numberadults-dropdown', 'value'),
    Input('numberchildren-dropdown', 'value')])
def update_output(adults, children):
    string_prefix = "The reservation is for "
    return string_prefix + str(int(adults) + int(children)) + " people."

@app.callback(
    Output('states-dropdown', 'options'),
    [Input('regions-dropdown', 'value')])
def set_region_options(selected_region):
    return [{'label': i, 'value': i} for i in region_options[selected_region]]

@app.callback(
    Output('states-dropdown', 'value'),
    [Input('states-dropdown', 'options'),
     Input('resorts-dropdown', 'value')])
def set_states_value(state_options, resort_value):
    return [state_options[i]['value'] for i in range(len(state_options))]

@app.callback(
    Output('resorts-dropdown', 'options'),
    [Input('states-dropdown', 'value')])
def set_state_options(selected_states):
    resorts = sum([resort_options[x] for x in selected_states], [])
    return [{'label': i, 'value': i} for i in resorts]

@app.callback(
    Output('display-selected-values', 'children'),
    [Input('resorts-dropdown', 'value'),
     Input('regions-dropdown', 'value')])
def set_display_children(selected_resort, selected_region):
    if selected_resort:
        return u'{} is a resort in region {} and state {}'.format(
        selected_resort, selected_region, resort_state_dict[selected_resort])
    else:
        pass

@app.callback(
    Output('display-prediction', 'children'),
    [Input('date-picker-range', 'start_date'),
     Input('date-picker-range', 'end_date'),
     Input('numberadults-dropdown', 'value'),
     Input('numberchildren-dropdown', 'value'),
     Input('regions-dropdown', 'value'),
     Input('states-dropdown', 'value'),
     Input('resorts-dropdown', 'value'),])
def get_intermidiate_value(start_date, end_date,
numberadults, numberchildren,
region, state, resort):
    if not any([x is None for x in [start_date, end_date,
    numberadults, numberchildren,
    region, state, resort]]):
        # Copy from sample input
        sample_input2 = sample_input
        # Replace the fields with the ones from the forms
        sample_input2['booking_date'] = dt.strptime(booking_date, '%m/%d/%Y').strftime('%d/%m/%y')
        sample_input2['checkin_date'] = dt.strptime(start_date, '%Y-%m-%d').strftime('%d/%m/%y')
        sample_input2['checkout_date'] = dt.strptime(end_date, '%Y-%m-%d').strftime('%d/%m/%y')
        sample_input2['numberofadults'] = int(numberadults)
        sample_input2['numberofchildren'] = int(numberchildren)
        sample_input2['total_pax'] = sample_input2['numberofadults'] + sample_input2['numberofchildren']
        sample_input2['state_code_resort'] = resort_state_dict[resort]
        sample_input2['resort_region_code'] = int(region)
        sample_input2['resort_id'] = resort

        # Preprocess step
        sample_input2 = preprocess(sample_input2)
        prediction = pipeline.predict(sample_input2)[0]

        return u'{:.3f}'.format(prediction)
    else:
        return u'Fill in blanks'


# The End
if __name__ == '__main__':
    app.run_server(host='0.0.0.0', debug=True, port=8080)
