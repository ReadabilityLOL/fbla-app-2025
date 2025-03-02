from llama_cpp import Llama

model_path = "./Meta-Llama-3.1-8B-Instruct-f32.gguf"
llm = Llama(model_path=model_path, chat_format="chatml-function-calling")


def give_financial_rating(task):
    print(task)

    try:
        #update streamlit
    except Exception as error:
        print(error)


import json


def main():
    while True:
        user_input = input("You: ")

        response = llm.create_chat_completion(
            messages=[
                {
                    "role": "system",
                    "content": f"You are an AI assistant that helps users manage their financial information. Your job is to give a general trend based off of previous financial choices for the next 3 years."
                },
                {
                    "role": "user",
                    "content": user_input
                }
            ],
            tools=[{
                "type": "function",
                "function": {
                    "name": "give_financial_rating",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "future_spendings": {
                                "type": "int",
                                "description": "A percentage of how mutch your spendings are predictied to increase or decrease."
                            }
                        },
                        "required": ["future_spendings"]
                    }
                }
            }],
            tool_choice={
                "type": "function",
                "function": {
                    "name": "future_spendings"
                }
            }
        )

        ai_response = response['choices'][0]['message']

        if 'function_call' in ai_response:
            print(ai_response)
            function_call = ai_response['function_call']
            if function_call['name'] == 'AddTodo':
                args = json.loads(function_call['arguments'])
                result = add_todo(args)
                print(f"AI: {result}")
        else:
            print(f"AI: {ai_response['content']}")


if __name__ == "__main__":
    main()
