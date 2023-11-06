import streamlit as st
from final import query_db  # Importing necessary function from final.py

def main():
    st.title('Query Farmers Data using Natural Language')

    # Static sidebar content
    st.sidebar.image("231.png", width=400)
    st.sidebar.caption("Sample Dataset")
    st.sidebar.title("Custom Commands")

    # Scrollable sidebar content for commands
    with st.sidebar:
        # Using beta_expander to create a scrollable section
        with st.expander("Commands", expanded=True):
            command_options = ('Describe the crop_yield table.',
                               'Describe the fertilizer table.',
                               'Which crops had production greater than 30000 in Telangana?',
                               'Which crops had production greater than 30000 in Assam?',
                               'What is average pH value of rice?',
                               'What is the yearly temperature of Bihar?', 'What is the highest N value observed?',
                               'What crops have pH value greater than 6?', 'What is the average N value of Maize?',
                               'What is the Kharif temperature of Telangana?',
                               'What is the highest yearly rainfall value?',
                               'Which crop has the highest P value?',
                               'What is the total production of GroundNut in Andhra Pradesh?',
                               'What is the total production of ragi in Andhra Pradesh?',
                               'What is the average temperature of Karnataka?')
            for cmd in command_options:
                if st.button(cmd):
                    process_user_input(cmd)

    # Initialize session_state for chat_history if it doesn't exist
    if 'chat_history' not in st.session_state:
        st.session_state['chat_history'] = []

    user_input = st.text_input('You:', key='user_input')

    if st.button('Submit'):
        process_user_input(user_input)

    # Display chat history
    st.write("Chat History:")
    for entry in st.session_state['chat_history']:
        st.markdown(
            f"<div style='margin: 10px; padding: 10px; border-radius: 5px; border: 1px solid #ccc;'>"
            f"<p style='margin: 0;'><b>User:</b> <b>{entry['query']}</b></p>"
            f"<p style='margin: 0;'><b>Bot:</b> {entry['response']}</p>"
            f"</div>",
            unsafe_allow_html=True
        )

def process_user_input(user_input):
    # Query the database and update the chat history
    response_data = query_db(user_input)
    response = response_data['response']
    # Update session_state for chat_history
    st.session_state['chat_history'].append({
        'query': user_input,
        'response': response
    })

if __name__ == '__main__':
    main()
