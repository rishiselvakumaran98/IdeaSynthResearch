import openai
import json
import dotenv

# Ensure you've set your OpenAI API key in the environment or replace with your key directly:
openai.api_key = dotenv.get_key('.env', 'OPENAI_API_KEY')

def extract_paper_insights(full_text: str, model: str = "gpt-4o-mini") -> dict:
    """
    Prompt an LLM to extract key sections from the full text of a paper:
      - Proposed design and solution
      - Evaluation method
      - Contribution and impact
      - Limitations and future works

    Returns a dictionary with those fields.
    """
    system_message = (
        "You are a helpful assistant specialized in analyzing academic papers. "
        "Given the full text of a research paper, extract and summarize the following sections:\n"
        "1. Proposed Design and Solution\n"
        "2. Evaluation Method\n"
        "3. Contribution and Impact\n"
        "4. Limitations and Future Works\n"
        "Return the result as a JSON object with keys: "
        "design_solution, evaluation_method, contribution_impact, limitations_future_works."
    )

    user_message = f"Here is the full text of the paper:\n\n{full_text}"

    response = openai.ChatCompletion.create(
        model=model,
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_message}
        ],
        temperature=0.0,  # deterministic output
        max_tokens=1024
    )

    # Parse the JSON from the assistant
    content = response.choices[0].message.content.strip()
    try:
        insights = json.loads(content)
    except json.JSONDecodeError:
        # If parsing fails, return raw content
        insights = {"error": "Failed to parse JSON", "raw_output": content}

    return insights

if __name__ == "__main__":
    # Example usage: read your full-text file
    with open("KnownNet_Research_Paper.tei.xml", "r", encoding="utf-8") as f:
        paper_text = f.read()

    insights = extract_paper_insights(paper_text)
    print(json.dumps(insights, indent=2))
