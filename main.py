from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain.agents import create_tool_calling_agent,AgentExecutor


from tools import ApplicationOutput, tools
from langchain_core.messages import HumanMessage,AIMessage


llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.3,
    max_output_tokens=1500,
)

parser =PydanticOutputParser(pydantic_object= ApplicationOutput)

prompt = ChatPromptTemplate.from_messages([
        ("system","""
        You are a career assistant that helps tailor resumes and write cover letters for job applications.

Use the provided resume and job description to:

1. Understand job requirements

2. Modify the resume to align with key skills

3. Generate a professional, personalized cover letter

Always save the result using the save_application tool.

Output only valid JSON in this format:

{format_instructions)

"""),

("placeholder", "(chat_history)"),

("human", "(query)"),

("placeholder", "(agent_scratchpad)"),

]).partial(format_instructions=parser.get_format_instructions())

agent= create_tool_calling_agent(llm=llm, prompt=prompt, tools=tools)

executor= AgentExecutor(agent=agent, tools=tools, verbose=True)

chat_history=[]

while True:
  query =input("You:")
  if query.lower() in ["exit","qu5it"]:
    break 

  chat_history.append(HumanMessage(content=query))


  response =executor.invoke({
      "query":query,
      "chat_history":chat_history,
      
  })

  try:
    parsed = parser.parser(response.get("output"))
    print("\n Job Titile:",parsed.job_title)
    print("\n Cover Letter Preview:\n",parsed.cover_letter[:500],"...")
    chat_history.append(AIMessage(content=parsed.cover_letter))
  except Exception as e:
    print("\n[Error parsing output]:",e)
    print("Raw:",response.get("output"))