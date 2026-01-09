import subprocess
from src.engine.guardrails import GitGuardrail

class SREAgent:
    def __init__(self, model, tokenizer, sandbox_dir="./sandbox"):
        self.model = model
        self.tokenizer = tokenizer
        self.sandbox = sandbox_dir

    def run_step(self, instruction, observation):
        prompt = f"### Instruction:\n{instruction}\n\n### Observation:\n{observation}\n\n### Thought (SRE Reasoning):"
        inputs = self.tokenizer([prompt], return_tensors="pt").to("cuda")
        outputs = self.model.generate(**inputs, max_new_tokens=150)
        return self.tokenizer.decode(outputs[0], skip_special_tokens=True)

    def execute_recovery(self, goal):
        obs = "System scan: Repository in broken state."
        
        for i in range(3):
            print(f"--- Agent Attempt {i+1} ---")
            raw_response = self.run_step(goal, obs)
            
            try:
                # Extract Action from response
                command = raw_response.split("### Action (CLI Command):")[1].split("###")[0].strip()
                
                # Validate with Guardrail
                is_safe, msg = GitGuardrail.validate(command)
                if not is_safe:
                    print(msg)
                    obs = msg
                    continue

                # Execute in Sandbox
                print(f"🛠️ Executing: {command}")
                result = subprocess.run(command, shell=True, cwd=self.sandbox, capture_output=True, text=True)
                obs = (result.stdout + result.stderr).strip()
                
                if "HEAD is now at" in obs or "Success" in obs:
                    print("🎉 Recovery Successful!")
                    return True
            except Exception as e:
                obs = f"Error parsing/executing: {str(e)}"
        
        return False