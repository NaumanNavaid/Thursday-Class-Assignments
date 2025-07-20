from agents import Runner, set_tracing_disabled
from handoff_agent.main import triage_agent
import asyncio
from openai.types.responses import ResponseTextDeltaEvent
from my_config.gemini_config import run_config

# Disable tracing for cleaner output
set_tracing_disabled(True)

async def main():
    """Enhanced main function with better event handling and handoff visibility"""
    print("🤖 Welcome to the Multi-Agent Assistant!")
    print("=" * 50)
    
    try:
        prompt = input("💬 Enter your prompt: ")
        
        if not prompt.strip():
            print("❌ Please enter a valid prompt")
            return
        
        print(f"\n🔍 Processing your request: \"{prompt}\"")
        print("-" * 50)
        
        # Start the streaming runner
        res = Runner.run_streamed(
            starting_agent=triage_agent, 
            input=prompt,
            run_config=run_config
        )
        
        current_agent = "Triage Agent"
        response_text = ""
        handoff_occurred = False
        
        print(f"🤖 {current_agent}: ", end="", flush=True)
        
        async for event in res.stream_events():
            # Handle agent handoffs
            if event.type == "agent_handoff_event":
                handoff_occurred = True
                new_agent = event.data.to_agent.name
                print(f"\n\n🔄 **HANDOFF DETECTED**")
                print(f"   From: {current_agent}")
                print(f"   To: {new_agent}")
                print(f"   Reason: Specialized expertise required")
                print("-" * 50)
                print(f"🤖 {new_agent}: ", end="", flush=True)
                current_agent = new_agent
            
            # Handle text streaming
            elif event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
                delta = event.data.delta
                print(delta, end="", flush=True)
                response_text += delta
            
            # Handle tool calls (for math and weather operations)
            elif event.type == "tool_call_event":
                tool_name = getattr(event.data, 'tool_name', 'Unknown Tool')
                print(f"\n🔧 Using tool: {tool_name}")
                print("   ", end="", flush=True)
            
            # Handle tool results
            elif event.type == "tool_result_event":
                print("✅ Tool completed")
                print(f"🤖 {current_agent}: ", end="", flush=True)
        
        # Final summary
        print(f"\n\n" + "=" * 50)
        print(f"✅ **Response Completed**")
        print(f"   Final Agent: {current_agent}")
        print(f"   Response Length: {len(response_text)} characters")
        if handoff_occurred:
            print(f"   Handoffs: ✅ Routed to specialist")
        else:
            print(f"   Handoffs: ❌ Handled by triage agent")
        print("=" * 50)
        
    except KeyboardInterrupt:
        print(f"\n\n⚠️  Session interrupted by user")
    except Exception as e:
        print(f"\n❌ Error occurred: {e}")
        import traceback
        traceback.print_exc()

async def interactive_session():
    """Interactive chat session with multiple queries"""
    print("🤖 Multi-Agent Assistant - Interactive Mode")
    print("Commands: 'quit'/'exit' to stop, 'clear' to clear screen")
    print("=" * 50)
    
    session_count = 0
    
    while True:
        try:
            session_count += 1
            print(f"\n💬 Session #{session_count}")
            prompt = input("You: ")
            
            if prompt.lower() in ['quit', 'exit', 'q']:
                print("👋 Thank you for using the Multi-Agent Assistant!")
                break
            elif prompt.lower() == 'clear':
                import os
                os.system('cls' if os.name == 'nt' else 'clear')
                session_count = 0
                continue
            elif not prompt.strip():
                print("❌ Please enter a valid prompt")
                continue
            
            print(f"\n🔍 Analyzing: \"{prompt}\"")
            print("-" * 30)
            
            res = Runner.run_streamed(
                starting_agent=triage_agent,
                input=prompt,
                run_config=run_config
            )
            
            current_agent = "Triage Agent"
            handoff_count = 0
            
            print(f"🤖 {current_agent}: ", end="", flush=True)
            
            async for event in res.stream_events():
                if event.type == "agent_handoff_event":
                    handoff_count += 1
                    new_agent = event.data.to_agent.name
                    print(f"\n\n🔄 Handoff #{handoff_count}: {current_agent} → {new_agent}")
                    print("-" * 30)
                    print(f"🤖 {new_agent}: ", end="", flush=True)
                    current_agent = new_agent
                
                elif event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
                    print(event.data.delta, end="", flush=True)
                
                elif event.type == "tool_call_event":
                    tool_name = getattr(event.data, 'tool_name', 'Unknown')
                    print(f"\n🔧 {tool_name}: ", end="", flush=True)
            
            print(f"\n✅ Completed by {current_agent}")
            
        except KeyboardInterrupt:
            print(f"\n👋 Session ended by user")
            break
        except Exception as e:
            print(f"\n❌ Error in session #{session_count}: {e}")

def run_sync_demo():
    """Demo of synchronous execution for comparison"""
    print("🔄 Running synchronous demo...")
    
    test_queries = [
        "Help me with Next.js routing",
        "Calculate 15 * 25",
        "What's the weather in London?",
        "Create a Python function to sort a list"
    ]
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n📝 Test {i}: {query}")
        print("-" * 40)
        
        try:
            result = Runner.run_sync(
                starting_agent=triage_agent,
                input=query,
                run_config=run_config
            )
            
            print(f"✅ Result: {getattr(result, 'output', str(result))[:100]}...")
            # Handoff count not available in RunResult
            
        except Exception as e:
            print(f"❌ Error: {e}")

# Main execution
if __name__ == "__main__":
    print("🚀 Multi-Agent System Startup")
    print("\nChoose execution mode:")
    print("1. Single Query (default)")
    print("2. Interactive Session")
    print("3. Sync Demo")
    
    try:
        choice = input("\nEnter choice (1-3, or press Enter for 1): ").strip()
        
        if choice == "2":
            asyncio.run(interactive_session())
        elif choice == "3":
            run_sync_demo()
        else:
            # Default: single query mode
            asyncio.run(main())
            
    except KeyboardInterrupt:
        print("\n👋 Startup cancelled by user")
    except Exception as e:
        print(f"❌ Startup error: {e}")