from langchain.chat_models import ChatOpenAI # importing the chat model
from langchain.prompts import PromptTemplate # for creating chat templates
from langchain.memory import ConversationSummaryBufferMemory # to store and rreply based in temporary user based convo
from langchain.chains import ConversationChain # for chaining user queries and models and memory stored

# OpenAI's api-key
api_key = "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"

# model name
llm_model = "gpt-3.5-turbo"

# having this as a global variable, reducing the necessity of reloading the model on and on and on
chat_model = ChatOpenAI(temperature=0.6, model=llm_model, openai_api_key="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") # make it semi-creative, so temp is kinda low

# memory to keep track on convo between human and AI - 
memory = ConversationSummaryBufferMemory(llm=chat_model, max_token_limit=100)
# creating a chain to store convos between user and AI, in memory and reply based on it
conversation = ConversationChain( 
    llm=chat_model, memory = memory, verbose=False # this is just a combination of memory - model - prompt
)
# ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''' #

chat_prompt = """
System: You are a Medical/Healthcare expert, who resolve user queries on\
        Biological, Medical and healtcare related issues.

reply to user queries delimited by triple backticks

IMPORTANT:
    -> Have normal conversations
    -> be friendly to humans and greet them
    -> resolve queries with responses in simple english
    -> if user queries are very out from the context\
       reply "Can't help you with it, Please Stick to asking queries from ayurveda and\
       sanskrit slokas"
    -> restrict the response within 30-60 words, reply as short as possible
    -> prescribe exercised, diets, drugs and other treaments too

user query: ```{query}```
"""

prescription_prompt = """
System: You are a professional Medical/Healthcare expert\
        based on the symptoms given (delimited by triple backticks)

Task: 
    -> prescribe medicines and other treatments like\
       yoga, diet and more
    -> feel free to use medicinal terms as this would be given\
       to a pharmacist
    -> since we have specified the users that this is ai generated and not\
       as precise as an actual doctors precription, its not necessary to metion that\
       this is AI generated.
    -> generate a prescription of length no more than 120 words
    -> be precise about the content being generated
    -> take your time, lets think step by step

!!! Important: Dont exceed the response length over 100 words !!!

symptoms:```
    {symptoms}
```
"""

# prompt template for above prompt
chat_template = PromptTemplate.from_template(chat_prompt)
prescription_template = PromptTemplate.from_template(prescription_prompt)
# ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''' #

def doTempalte(template, **variables) -> str:
    '''
    kwargs -> variables
    ensure exact variables in give in template is fed
    else an error message will be displayed
    '''
    
    return template.format(**variables)



def get_completion(prompt):

    ai_response = conversation.predict(input=prompt)

    return ai_response # returning the response from llm

# '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''' #
def mainCall(query):
    # feeding in template, getting respone, summarizing and storing it in memory
    return get_completion(doTempalte(chat_template, query=query))


def generate_prescription(symptoms: str):
    return get_completion(doTempalte(prescription_template, symptoms=symptoms))

if __name__ == "__main__":
    
    
    # x = input("Please enter your query: ")
    # print("\n")
    # while x!="stall":
    #     print("AI:", get_completion(doTempalte(chat_template, query=x)), end="\n\n----------------------------------------------------------\n\n")
    #     x = input("User: ")
    #     print("\n")    
    # print(generate_prescription("for the past two years, sinusitis has been a constant battle. My nose feels perpetually blocked, headaches are a daily struggle, and a never-ending postnasal drip is driving me crazy. The fatigue is relentless, and now, this facial tenderness is a new layer of discomfort. I've tried all the usual remedies, but nothing provides a lasting solution. It's impacting my daily life, and I'm ready to kick this sinusitis to the curb. Any thoughts on how we can tackle this and get me back to feeling normal?"))
    ...