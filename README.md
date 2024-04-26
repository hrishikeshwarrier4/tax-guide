# TaxMate: Smart Solutions for Smart Taxpayers

TaxMate is a responsive chatbot designed to assist users with their tax-related queries by leveraging the power of a Large Language Model (LLM) integrated with a vector database. This application provides tax guidance by understanding user queries through natural language processing and retrieving relevant information from a structured tax guide dataset.

## Features
•	Natural Language Query Handling: Users can ask questions in plain English and receive tax advice that is contextually relevant.

•	Semantic Search: Employs a vector database to fetch semantically similar documents based on the user's query, ensuring accurate and useful responses.

•	Interactive Chat Interface: Built using Streamlit, the interface is user-friendly and facilitates easy interaction with the chatbot.

•	Session Management: Maintains user session state to provide continuity in conversation, enhancing user experience.

## Prerequisites
•	Python 3.8 or later

•	pip for Python package management

•	Install the requirements.txt file

•	Access to OpenAI API (API key required)

## Installation
1.	Clone the repository

    git clone https://github.com/hrishikeshwarrier4/taxmate.git

    cd taxmate 

3.	Install required Python packages

    pip install -r requirements.txt 

## Setup
1.	API Key Configuration: You need to set up your OpenAI API key in the environment variables or directly in the script.

    export OPENAI_API_KEY='your-openai-api-key' 

2.	Data Preparation: Ensure that your tax guide documents are stored in the directory specified by the data_directory variable in the script. These documents should be in PDF format.

3.	Vector Database Initialization: Run the script once to initialize the vector database and populate it with embeddings from your documents.

## Running the Application
Launch the application by running:

streamlit run main.py

Navigate to localhost:8501 in your web browser to interact with the TaxMate chatbot.

## Usage
Once the application is running:

•	You will be greeted by the chat interface.

•	Simply type your tax-related query into the chat input box and press enter.

•	The chatbot will process your query and return a response based on the information available in the tax guide documents.

## Contributing
We welcome contributions to TaxMate! If you have suggestions or improvements, please fork the repository and submit a pull request.

## License
This project is licensed under the MIT License - see the LICENSE file for details.


