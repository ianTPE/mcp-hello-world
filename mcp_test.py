"""
A simple test script that simulates MCP interaction with a model.
"""
import json
from mcp_hello import create_thinking_message, create_tool_use_message, create_observation_message

def simulate_model_response(mcp_message):
    """Simulate how a model would respond to an MCP message."""
    
    content_type = mcp_message["content"]["type"]
    
    if content_type == "mcp:thinking":
        # Model processes internal thinking
        print("MODEL INTERNAL: Processing thinking directive")
        print(f"MODEL INTERNAL: {mcp_message['content']['contents']}")
        
        # Return a response to user
        return "I've considered this carefully and here's my response."
        
    elif content_type == "mcp:tool_use":
        tool_name = mcp_message["content"]["tool"]["name"]
        tool_input = mcp_message["content"]["tool"]["input"]
        
        print(f"MODEL INTERNAL: Calling external tool '{tool_name}'")
        
        # Simulate tool execution
        if tool_name == "calculator":
            expression = tool_input["expression"]
            print(f"MODEL INTERNAL: Calculating '{expression}'")
            
            try:
                # Note: In real applications, avoid using eval() for user input
                calc_result = eval(expression)
            except Exception as e:
                calc_result = f"Error: {e}"
            
            # Create an observation message
            tool_response = create_observation_message(tool_name, calc_result)
            
            print(f"MODEL INTERNAL: Got tool result: {json.dumps(tool_response)}")
            # Process the observation message
            return simulate_model_response(tool_response)
    
    elif content_type == "mcp:observation":
        tool_name = mcp_message["content"]["tool"]
        result = mcp_message["content"]["result"]
        print(f"MODEL INTERNAL: Received observation from tool '{tool_name}'")
        print(f"MODEL INTERNAL: Result: {result}")
        return f"The result of the calculation is {result['value']}."
    
    return "I don't know how to process that directive."

def main():
    print("=== MCP TEST SIMULATOR ===\n")
    
    # Test the thinking directive
    print("1. Testing 'thinking' directive")
    thinking_message = create_thinking_message("I need to analyze this data")
    print(f"Sending to model: {json.dumps(thinking_message, indent=2)}")
    response = simulate_model_response(thinking_message)
    print(f"MODEL OUTPUT TO USER: {response}\n")
    
    # Test the tool use directive
    print("2. Testing 'tool_use' directive")
    tool_message = create_tool_use_message("2 + 2 * 3")
    print(f"Sending to model: {json.dumps(tool_message, indent=2)}")
    response = simulate_model_response(tool_message)
    print(f"MODEL OUTPUT TO USER: {response}")

if __name__ == "__main__":
    main()