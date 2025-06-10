# import os
# import openai
# from dotenv import load_dotenv

# load_dotenv()
# client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# def query_llm(prompt, model="gpt-4o", temperature=0.2):
#     try:
#         response = client.chat.completions.create(
#             model=model,
#             messages=[{"role": "user", "content": prompt}],
#             temperature=temperature
#         )
#         return response.choices[0].message.content.strip()
#     except Exception as e:
#         return f"LLM Error: {str(e)}"


#code without API, This file is only used if LLM is required in the future, as of now it is not required
def query_llm(prompt):
    # Not used in local-only mode
    return "LLM not used. All responses are from structured data."

