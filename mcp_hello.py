import json

def create_thinking_message(user_input):
    """建立一則 mcp:thinking 訊息，表示模型內部思考"""
    return {
        "type": "mcp:directive",
        "version": "0.1",
        "content": {
            "type": "mcp:thinking",
            "contents": user_input
        }
    }

def create_tool_use_message(user_input):
    """建立一則 mcp:tool_use 訊息，這裡預設工具為計算器"""
    return {
        "type": "mcp:directive",
        "version": "0.1",
        "content": {
            "type": "mcp:tool_use",
            "tool": {
                "name": "calculator",
                "input": {
                    "expression": user_input
                }
            }
        }
    }

def create_observation_message(tool_name, result_value):
    """建立一則 mcp:observation 訊息，表示從工具獲得的結果"""
    return {
        "type": "mcp:directive",
        "version": "0.1",
        "content": {
            "type": "mcp:observation",
            "tool": tool_name,
            "result": {
                "value": result_value
            }
        }
    }

def simulate_model_response(mcp_message):
    """
    模擬模型對 MCP 訊息的處理：
      - mcp:thinking：模擬模型內部思考後回覆
      - mcp:tool_use：模擬呼叫工具（例如計算器）並將結果封裝成 observation 後再處理
      - mcp:observation：模擬模型接收到工具回應後，進一步處理
    """
    content_type = mcp_message["content"]["type"]
    
    if content_type == "mcp:thinking":
        print("MODEL INTERNAL: Processing thinking directive")
        print(f"MODEL INTERNAL: {mcp_message['content']['contents']}")
        # 模型內部思考完，回傳最終對使用者的回答
        return "I've considered this carefully and here's my response."
    
    elif content_type == "mcp:tool_use":
        tool_name = mcp_message["content"]["tool"]["name"]
        tool_input = mcp_message["content"]["tool"]["input"]
        print(f"MODEL INTERNAL: Calling external tool '{tool_name}'")
        
        if tool_name == "calculator":
            expression = tool_input["expression"]
            print(f"MODEL INTERNAL: Calculating '{expression}'")
            try:
                # 注意：實際應用中不要直接使用 eval() 來處理使用者輸入
                calc_result = eval(expression)
            except Exception as e:
                calc_result = f"Error: {e}"
            
            # 封裝成 observation 訊息
            tool_response = create_observation_message(tool_name, calc_result)
            print(f"MODEL INTERNAL: Got tool result: {json.dumps(tool_response)}")
            # 模型接著處理 observation 訊息
            return simulate_model_response(tool_response)
    
    elif content_type == "mcp:observation":
        tool_name = mcp_message["content"]["tool"]
        result = mcp_message["content"]["result"]
        print(f"MODEL INTERNAL: Received observation from tool '{tool_name}'")
        print(f"MODEL INTERNAL: Result: {result}")
        return f"I received the result from {tool_name}: {result['value']}"
    
    else:
        return "I don't know how to process that directive."

def interactive_chat():
    """
    互動式聊天模擬器：
      - 使用者輸入文字，根據內容判斷產生 mcp:thinking 或 mcp:tool_use 訊息
      - 模型根據訊息流程處理，包含工具調用及觀察結果
    """
    print("=== MCP INTERACTIVE CHAT ===")
    print("Type 'quit' to exit.\n")
    
    while True:
        user_input = input("You: ").strip()
        if user_input.lower() == "quit":
            print("Bye!")
            break
        
        # 判斷使用者輸入是否包含數學運算符號，簡單假設是數學算式
        if any(op in user_input for op in ["+", "-", "*", "/"]):
            mcp_message = create_tool_use_message(user_input)
        else:
            mcp_message = create_thinking_message(user_input)
        
        print("Sending to model:")
        print(json.dumps(mcp_message, indent=2))
        
        response = simulate_model_response(mcp_message)
        print(f"MODEL: {response}\n")

if __name__ == "__main__":
    interactive_chat()
