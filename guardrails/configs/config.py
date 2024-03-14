from nemoguardrails import LLMRails, RailsConfig
import os

with open(os.path.join(os.getcwd(), "guardrails", "configs", "files", "config.yaml")) as f:
    yaml_content = f.read()
    
with open(os.path.join(os.getcwd(), "guardrails", "configs", "files", "prompts.co")) as f:
    colang_content = f.read()
    
config = RailsConfig.from_content(
    yaml_content=yaml_content,
    colang_content=colang_content
)

guardrail_app = LLMRails(config=config)
