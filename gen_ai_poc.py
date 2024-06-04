# Python Dash App to Demo the AWS Bedrock & LLM Models in meetings

import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
from requests.exceptions import RequestException
import requests

app = dash.Dash(__name__)

# Layout of the app
app.layout = html.Div([
    html.H1("API Caller with Dash"),

    html.Div([
        # Button to toggle the drawer
        html.Button("Toggle Drawer", id="toggle-drawer-button", n_clicks=0),
    ], style={'width': '100%', 'margin-bottom': '20px'}),

    html.Div([
        # Drawer for the left panel
        html.Div([
            # Text input for API URL
            dcc.Input(id='url-input', type='text', placeholder='Enter API URL', style={'width': '100%'}),
            html.Br(),  # Add line break
            html.Br(),  # Add line break

            # USE CASE DROPDOWN
            dcc.Dropdown(id='use-case-dropdown', options=[{'label': 'Text Generation', 'value': 'UC1'},
                                                          {'label': 'Text Summarization', 'value': 'UC2'},
                                                          {'label': 'Text Classification', 'value': 'UC3'},
                                                          {'label': 'Q&A', 'value': 'UC4'}, ],
                         multi=False, placeholder='Select Use Case'),
            html.Br(),  # Add line break

            # FLOW TYPE DROPDOWN
            dcc.Dropdown(id='flow-dropdown', options=[{'label': 'Flow 1', 'value': '1'},
                                                      {'label': 'Flow 2', 'value': '2'},
                                                      {'label': 'Flow 3', 'value': '3'}],
                         multi=False, placeholder='Select Flow'),
            html.Br(),  # Add line break

            # MODEL DROPDOWN
            dcc.Dropdown(id='model-dropdown', options=[{'label': 'Titan Large', 'value': 'Titan Large'},
                                                       {'label': 'AI21 Grande', 'value': 'AI21 Grande'},
                                                       {'label': 'AI21 Jumbo', 'value': 'AI21 Jumbo'},
                                                       {'label': 'Claude Instant', 'value': 'Claude Instant'},
                                                       {'label': 'Claude v1', 'value': 'Claude v1'},
                                                       {'label': 'Claude v2', 'value': 'Claude v2'}],
                         multi=False, placeholder='Select Model'),
            html.Br(),  # Add line break

            # DEPARTMENT DROPDOWN
            dcc.Dropdown(id='department-dropdown', options=[{'label': 'Service Desk', 'value': 'Service Desk'},
                                                           {'label': 'Maintenance', 'value': 'Maintenance'},
                                                           {'label': 'Finance', 'value': 'Finance'}],
                         multi=False, placeholder='Select Department'),
            html.Br(),  # Add line break

            # QUESTIONS DROPDOWN
            dcc.Dropdown(id='questions-dropdown',
                         options=[{'label': 'How do I use a hotspot on my iphone?', 'value': 'Q1'},
                                  {'label': 'What is the error for this error code: 12345?', 'value': 'Q2'}],
                         multi=False, placeholder='Select Question'),
            html.Br(),  # Add line break

            # IS_CONVERSATION DROPDOWN
            dcc.Checklist(id='conversation-checkbox',
                          options=[{'label': 'Enable Conversation', 'value': 'conversation'}]),
            html.Br(),  # Add line break

        ], id="drawer", style={'width': '30%', 'float': 'left', 'margin-right': '10px', 'display': 'none'}),

        # Panel on the right-hand side
        html.Div([
            # Chat UI to display API results
            dcc.Textarea(
                id='chat-output',
                value='',
            ),

            # Input text box for user to type in a query
            dcc.Input(id='user-query-input', type='text', placeholder='Type your query here',
                      style={'width': '100%', 'margin-top': '10px'}),

            # Submit button
            html.Button(id='submit-button', n_clicks=0, children='Submit'),

            # Clear Chat button
            html.Button(id='clear-chat-button', n_clicks=0, children='Clear Chat', style={'float': 'right'}),
        ], style={'width': '65%', 'float': 'left'}),

    ], style={'margin': '20px'})
])

# Callback to toggle the drawer
@app.callback(
    Output("drawer", "style"),
    [Input("toggle-drawer-button", "n_clicks")],
    [State("drawer", "style")],
)
def toggle_drawer(n, style):
    return {'display': 'block' if n % 2 == 1 else 'none'}

# Callback to handle API call and update chat UI
@app.callback(
    [Output('chat-output', 'value'),
     Output('clear-chat-button', 'n_clicks')],
    [Input('submit-button', 'n_clicks'),
     Input('clear-chat-button', 'n_clicks')],
    [State('url-input', 'value'),
     State('department-dropdown', 'value'),
     State('model-dropdown', 'value'),
     State('flow-dropdown', 'value'),
     State('questions-dropdown', 'value'),
     State('use-case-dropdown', 'value'),
     State('conversation-checkbox', 'value'),
     State('user-query-input', 'value')]  # Include user query input value in the callback
)
def update_chat(submit_clicks, clear_clicks, url, department, model, flow, question, use_case, conversation_enabled,
                user_query):
    ctx = dash.callback_context

    if ctx.triggered_id == 'submit-button.n_clicks':
        try:
            # Construct API parameters based on user input
            api_params = {
                "model_name": model,
                "use_case": use_case,
                "query": question,
                "domain": department,
                "prompt_type": "0",
                "unique_cache_key": "KEY REMOVED",
                "flow_type": flow,
                "is_file_uploaded": False,  # fileUploaded,
                "file_path": "https://google.com",
                "is_conversation": 'conversation' in conversation_enabled,
            }

            # Make API call using requests library
            response = requests.post(url, data=api_params)  # Use POST instead of GET for including data in the request
            response.raise_for_status()  # Raise an error for unsuccessful HTTP responses

            # Update chat UI with API response
            chat_text = f"API Response:\n{response.text}"
            return chat_text, dash.no_update

        except RequestException as e:
            # Handle exceptions (e.g., network errors, HTTP errors)
            error_message = f"Error making API request: {e}"
            return error_message, dash.no_update

    elif ctx.triggered_id == 'clear-chat-button.n_clicks':
        # Clear chat
        return '', clear_clicks + 1

    # Return an empty string if the button is not clicked yet
    return '', dash.no_update

if __name__ == '__main__':
    app.run_server(debug=True)
