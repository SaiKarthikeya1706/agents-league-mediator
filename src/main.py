import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

class PolicyArbitrator:
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")
        # Load the policy
        with open("policy.txt", "r") as f:
            self.policy_context = f.read()

    def resolve_conflict(self, department, request_details):
        # We now inject the policy_context into the prompt
        prompt = f"""
        Act as an expert policy arbitrator.
        
        INTERNAL POLICY:
        {self.policy_context}
        
        CONFLICT TO RESOLVE:
        {department} is requesting {request_details}.
        
        INSTRUCTIONS:
        1. Compare the request against the INTERNAL POLICY.
        2. If the request violates policy, identify the specific requirements needed for an exception.
        3. Use professional, firm, and strategic language.
        """
        response = self.llm.invoke(prompt)
        return response.content

def main():
    arbitrator = PolicyArbitrator()
    result = arbitrator.resolve_conflict("Sales", "30% discount for a key client")
    print(f"\n--- Arbitration Decision ---\n{result}")

if __name__ == "__main__":
    main()