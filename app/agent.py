from langchain.agents import create_openai_tools_agent, AgentExecutor
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.prompts import MessagesPlaceholder
from langchain.schema import SystemMessage

from app.tools.stock_tools import StockPriceTool
from app.config import OPENAI_API_KEY, DEFAULT_MODEL

def create_stock_agent(model_name=None):
    """Create a LangChain agent for stock analysis"""
    
    if not model_name:
        model_name = DEFAULT_MODEL
    
    llm = ChatOpenAI(
        api_key=OPENAI_API_KEY,
        model=model_name,
        temperature=0.1
    )
    
    tools = [StockPriceTool()]
    
    system_message = SystemMessage(
        content="""You are a helpful stock market analysis assistant. 
        You can fetch stock prices and provide investment recommendations.
        
        When providing a recommendation:
        1. Consider recent price trends
        2. Look at key financial metrics
        3. Provide a clear BUY/SELL/HOLD recommendation
        4. Briefly explain your reasoning
        
        Always format currency values appropriately and be precise with numbers.
        """
    )
    
    prompt = [
        system_message,
        MessagesPlaceholder(variable_name="chat_history"),
        MessagesPlaceholder(variable_name="input"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ]
    
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    
    agent = create_openai_tools_agent(llm, tools, prompt)
    
    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools,
        memory=memory,
        verbose=True,
        handle_parsing_errors=True
    )
    
    return agent_executor

def get_stock_recommendation(ticker, model_name=None):
    """Get stock information and recommendation for a specific ticker"""
    agent = create_stock_agent(model_name)
    
    response = agent.invoke({
        "input": f"Get me the latest price information for {ticker} and provide an investment recommendation (buy/sell/hold) with brief reasoning."
    })
    
    return response["output"]