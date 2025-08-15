import os
from langchain.agents import tool, initialize_agent, AgentType
from langchain_google_genai import ChatGoogleGenerativeAI

# ✅ Set your Gemini API key
os.environ["GOOGLE_API_KEY"] = "AIzaSyCrIWWepOcPB3YMfWLjsU7HfEoPEgJyZdw"

# ✅ Folder where files can be safely deleted
SAFE_FOLDER = "delete-zone"

# ✅ Tool: Delete only from SAFE_FOLDER
@tool
def delete_file(filename: str) -> str:
    """
    Deletes a file from the delete-zone folder.
    Only accepts basic file names like 'test.txt'.
    """
    try:
        # Validation
        if ".." in filename or "/" in filename or "\\" in filename:
            return "❌ Invalid filename. Use simple names like 'log.txt'."

        # Construct safe full path
        file_path = os.path.join(SAFE_FOLDER, filename)
        full_path = os.path.abspath(file_path)

        if not os.path.isfile(full_path):
            return f"❌ File not found in {SAFE_FOLDER}: {filename}"

        # Delete the file
        os.remove(full_path)
        return f"✅ File '{filename}' deleted from '{SAFE_FOLDER}'"
    except Exception as e:
        return f"❌ Error: {e}"

# ✅ Load Gemini Model
llm = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0.3)

# ✅ Agent Setup
tools = [delete_file]
agent = initialize_agent(tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)

# ✅ Invoke agent
response = agent.invoke({"input": "Delete log.txt"})
print(response)
