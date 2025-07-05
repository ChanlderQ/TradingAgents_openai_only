import time
import json


def create_research_manager(llm, memory):
    def research_manager_node(state) -> dict:
        history = state["investment_debate_state"].get("history", "")
        market_research_report = state["market_report"]
        sentiment_report = state["sentiment_report"]
        news_report = state["news_report"]
        fundamentals_report = state["fundamentals_report"]

        investment_debate_state = state["investment_debate_state"]

        curr_situation = f"{market_research_report}\n\n{sentiment_report}\n\n{news_report}\n\n{fundamentals_report}"
        past_memories = memory.get_memories(curr_situation, n_matches=2)

        past_memory_str = ""
        for i, rec in enumerate(past_memories, 1):
            past_memory_str += rec["recommendation"] + "\n\n"

        prompt = f"""As the portfolio manager and debate facilitator, your role is to critically evaluate this round of debate and make a definitive decision: align with the bear analyst, the bull analyst, or choose Hold only if it is strongly justified based on the arguments presented.

Summarize the key points from both sides concisely, focusing on the most compelling evidence or reasoning. Your recommendation—Buy, Sell, or Hold—must be clear and actionable. Avoid defaulting to Hold simply because both sides have valid points; commit to a stance grounded in the debate's strongest arguments.

Additionally, develop a detailed investment plan for the trader. This should include:

Your Recommendation: A decisive stance supported by the most convincing arguments.
Rationale: An explanation of why these arguments lead to your conclusion.
Strategic Actions: Concrete steps for implementing the recommendation.
Take into account your past mistakes on similar situations. Use these insights to refine your decision-making and ensure you are learning and improving. Present your analysis conversationally, as if speaking naturally, without special formatting. 

Here are your past reflections on mistakes:
\"{past_memory_str}\"

Here is the debate:
Debate History:
{history}"""
        response = llm.invoke(prompt)
        full_response_content = response.content

        # Extract Bull and Bear's latest arguments from history
        bull_arguments = []
        bear_arguments = []
        for line in history.split('\n'):
            if line.startswith("Bull Analyst:"):
                bull_arguments.append(line.replace("Bull Analyst:", "").strip())
            elif line.startswith("Bear Analyst:"):
                bear_arguments.append(line.replace("Bear Analyst:", "").strip())

        # Get the latest arguments
        latest_bull_argument = bull_arguments[-1] if bull_arguments else "No recent bull arguments."
        latest_bear_argument = bear_arguments[-1] if bear_arguments else "No recent bear arguments."

        # Construct the condensed summary
        condensed_summary = f"**Investment Debate Summary**\n\n"
        condensed_summary += f"**Bull Analyst Key Point:** {latest_bull_argument}\n\n"
        condensed_summary += f"**Bear Analyst Key Point:** {latest_bear_argument}\n\n"
        condensed_summary += f"**Research Manager's Conclusion:** {full_response_content}"

        new_investment_debate_state = {
            "judge_decision": full_response_content,
            "history": investment_debate_state.get("history", ""),
            "bear_history": investment_debate_state.get("bear_history", ""),
            "bull_history": investment_debate_state.get("bull_history", ""),
            "current_response": full_response_content,
            "count": investment_debate_state["count"],
        }

        return {
            "investment_debate_state": new_investment_debate_state,
            "investment_plan": condensed_summary,
        }

    return research_manager_node
