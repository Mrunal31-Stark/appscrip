try:
    print("Testing duckduckgo_search import...")
    from duckduckgo_search import DDGS
    print("duckduckgo_search imported successfully.")
    
    print("Testing config import...")
    from app.config import settings
    print(f"Config loaded. Project: {settings.PROJECT_NAME}")
    
    print("Testing main app import...")
    from app.main import app
    print("Main app imported successfully.")

except Exception as e:
    print(f"CRITICAL ERROR: {e}")
    import traceback
    traceback.print_exc()
