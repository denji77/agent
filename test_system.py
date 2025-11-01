"""
Test script to verify the debate system works correctly
"""
import os
import sys

def test_imports():
    """Test that all required packages can be imported"""
    print("Testing imports...")
    
    try:
        import config
        print("  ✓ config.py")
    except Exception as e:
        print(f"  ✗ config.py: {e}")
        return False
    
    try:
        import state
        print("  ✓ state.py")
    except Exception as e:
        print(f"  ✗ state.py: {e}")
        return False
    
    try:
        import logger
        print("  ✓ logger.py")
    except Exception as e:
        print(f"  ✗ logger.py: {e}")
        return False
    
    try:
        from langgraph.graph import StateGraph, END
        print("  ✓ langgraph")
    except Exception as e:
        print(f"  ✗ langgraph: {e}")
        print("    Run: pip install langgraph")
        return False
    
    try:
        from langchain_openai import ChatOpenAI
        print("  ✓ langchain_openai")
    except Exception as e:
        print(f"  ✗ langchain_openai: {e}")
        print("    Run: pip install langchain-openai")
        return False
    
    try:
        from langchain.prompts import ChatPromptTemplate
        print("  ✓ langchain")
    except Exception as e:
        print(f"  ✗ langchain: {e}")
        print("    Run: pip install langchain")
        return False
    
    return True


def test_config():
    """Test configuration"""
    print("\nTesting configuration...")
    
    import config
    
    if not config.PERPLEXITY_API_KEY or config.PERPLEXITY_API_KEY == "your_perplexity_api_key_here":
        print("  ✗ Perplexity API key not configured")
        print("    Please set PERPLEXITY_API_KEY in .env file")
        return False
    
    print(f"  ✓ Perplexity API key configured")
    print(f"  ✓ Model: {config.MODEL_NAME}")
    print(f"  ✓ Total rounds: {config.TOTAL_ROUNDS}")
    print(f"  ✓ Agent A: {config.AGENT_A_PERSONA['name']}")
    print(f"  ✓ Agent B: {config.AGENT_B_PERSONA['name']}")
    
    return True


def test_state_initialization():
    """Test state initialization and validation"""
    print("\nTesting state management...")
    
    from state import initialize_state, validate_state
    
    # Test initialization
    state = initialize_state("Test topic")
    
    if state["topic"] != "Test topic":
        print("  ✗ State initialization failed")
        return False
    
    print("  ✓ State initialization")
    
    # Test validation
    is_valid, error = validate_state(state)
    if not is_valid:
        print(f"  ✗ State validation failed: {error}")
        return False
    
    print("  ✓ State validation")
    
    return True


def test_logger():
    """Test logger functionality"""
    print("\nTesting logger...")
    
    from logger import DebateLogger
    
    logger = DebateLogger("Test topic")
    logger.log_argument(1, "TestAgent", "Test argument")
    logger.log_memory_update(1, "Test summary")
    
    if not os.path.exists(logger.log_file):
        print("  ✗ Log file not created")
        return False
    
    print(f"  ✓ Logger functional")
    print(f"  ✓ Log file: {logger.log_file}")
    
    return True


def main():
    """Run all tests"""
    print("="*60)
    print("MULTI-AGENT DEBATE SYSTEM - TEST SUITE")
    print("="*60)
    
    tests = [
        ("Imports", test_imports),
        ("Configuration", test_config),
        ("State Management", test_state_initialization),
        ("Logger", test_logger),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"\n✗ {test_name} failed with exception: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    for test_name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status}: {test_name}")
    
    all_passed = all(result for _, result in results)
    
    if all_passed:
        print("\n✓ All tests passed! System is ready to run.")
        print("\nRun the debate system with: python main.py")
    else:
        print("\n✗ Some tests failed. Please fix the issues above.")
    
    print("="*60)
    
    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())
