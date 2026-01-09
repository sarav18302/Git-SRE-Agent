from unsloth import FastLanguageModel
from src.config import Config
from src.engine.agent import SREAgent
import os

def run_pipeline():
    print("🚀 Initializing Git-SRE Autonomous System...")
    
    # 1. Load Model with Config
    model, tokenizer = FastLanguageModel.from_pretrained(
        model_name=Config.BASE_MODEL,
        max_seq_length=Config.MAX_SEQ_LENGTH,
        load_in_4bit=True,
    )
    FastLanguageModel.for_inference(model)

    # 2. Setup Sandbox
    if not os.path.exists("./sandbox"): os.makedirs("./sandbox")
    
    # 3. Initialize Agent
    agent = SREAgent(model, tokenizer)
    
    # 4. Run Task
    task = "Restore the repository history after an accidental hard reset."
    success = agent.execute_recovery(task)
    
    if success:
        print("✅ Task Completed Autonomously.")
    else:
        print("❌ Agent failed to resolve the issue.")

if __name__ == "__main__":
    run_pipeline()