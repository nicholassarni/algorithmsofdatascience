"""
Customer Service Bot Personas using TinyTroupe
==============================================

This script demonstrates the creation and interaction of customer service bot personas
with distinct personalities using the TinyTroupe library.

PERSONA SIMULATION EVALUATION:
------------------------------
This implementation creates diverse customer service personas to test the range and
effectiveness of AI-generated personality simulation:

1. SUNNY MARTINEZ - The Enthusiastic Optimist
   - Personality Type: High extraversion, very high agreeableness, positive affect
   - Demographic: 26-year-old American female, communications background
   - Usage Context: Best for handling general inquiries and boosting customer morale
   - Expected Strengths: Warm tone, empathetic responses, de-escalation through positivity
   - Expected Limitations: May seem overly cheerful for serious/technical issues

2. ALEX CHEN - The Efficient Professional
   - Personality Type: High conscientiousness, medium extraversion, task-focused
   - Demographic: 32-year-old Canadian male, business/IT background
   - Usage Context: Best for technical troubleshooting and process-driven interactions
   - Expected Strengths: Clear instructions, systematic approach, professional demeanor
   - Expected Limitations: May lack warmth, could seem cold in emotional situations

SIMULATION QUALITY ASSESSMENT:
------------------------------
The personas are designed to test:
- Personality consistency across extended interactions
- Demographic influence on communication style (age, nationality, background)
- Professional context adherence (customer service protocols)
- Emotional range and appropriateness

ANTICIPATED RESULTS:
- Successful simulations will show distinct, consistent personality traits
- Less realistic outputs may occur when personas face scenarios outside their expertise
- Diversity test: Contrasting Sunny's warmth vs Alex's efficiency reveals range
"""

import sys
import os

# Add parent directory to path to import tinytroupe
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'tinytroupe'))

import tinytroupe
from tinytroupe.agent import TinyPerson
from tinytroupe.environment import TinyWorld

# Set API key from environment or .env file
from dotenv import load_dotenv
load_dotenv()

def create_customer_service_bots():
    """
    Load customer service bot personas from JSON specifications.

    Each persona has been carefully designed with:
    - Distinct personality traits (Big Five personality dimensions)
    - Specific communication styles and preferences
    - Professional backgrounds that inform their approach
    - Behavioral patterns consistent with their personality type
    """

    # Load Sunny - The enthusiastic, positive customer service rep
    print("Loading Sunny Martinez (Enthusiastic Optimist)...")
    sunny = TinyPerson.load_specification("./agents/sunny.agent.json")

    # Load Alex - The efficient, professional customer service rep
    print("Loading Alex Chen (Efficient Professional)...")
    alex = TinyPerson.load_specification("./agents/alex.agent.json")

    return sunny, alex


def simulate_customer_interaction(sunny, alex):
    """
    Simulate a customer service scenario where two different personas
    discuss their approaches to handling a difficult customer situation.

    CONVERSATION QUALITY EVALUATION CRITERIA:
    ----------------------------------------
    1. NATURALNESS: Do responses sound like real human conversation?
    2. CONSISTENCY: Do personas maintain their personality throughout?
    3. DEPTH: Do responses show genuine understanding vs surface-level mimicry?
    4. DIVERSITY: Do different personas produce meaningfully different responses?
    5. COHERENCE: Do responses build logically on previous statements?

    EXPECTED PATTERNS:
    - Sunny should use positive language, empathy, enthusiasm
    - Alex should be direct, solution-focused, professional
    - Both should stay in-character even when challenged

    POTENTIAL LIMITATIONS:
    - AI may occasionally break character
    - Responses might become repetitive in extended conversations
    - Subtle personality traits may not always manifest clearly
    - Cultural/demographic nuances may be simplified
    """

    print("\n" + "="*70)
    print("CUSTOMER SERVICE TEAM DISCUSSION SIMULATION")
    print("="*70)
    print("\nScenario: Two customer service representatives discuss handling")
    print("a frustrated customer who received a defective product.\n")

    # Create a shared world where both agents can interact
    world = TinyWorld("Customer Service Team Room", [sunny, alex])
    world.make_everyone_accessible()

    # INTERACTION 1: Sunny initiates the conversation
    print("\n--- INTERACTION 1: Sunny initiates ---")
    sunny.listen("Hi Alex! I just had a really challenging call with a frustrated customer "
                 "who received a broken product. How do you usually handle those situations? "
                 "I tried to stay positive but they were pretty upset!")

    # Run the world to let agents process and respond
    world.run(2)

    # Display Sunny's interaction history
    print("\n[SUNNY'S PERSPECTIVE]")
    sunny.pp_current_interactions()

    # INTERACTION 2: Alex responds with his approach
    print("\n\n--- INTERACTION 2: Alex responds ---")
    alex.listen("Sunny asked me about handling frustrated customers with defective products. "
                "I should share my systematic approach.")

    world.run(2)

    # Display Alex's interaction history
    print("\n[ALEX'S PERSPECTIVE]")
    alex.pp_current_interactions()

    # INTERACTION 3: Sunny responds to Alex's approach
    print("\n\n--- INTERACTION 3: Sunny's reaction ---")
    sunny.listen("Alex just shared his approach. Respond to his method and share how "
                 "your approach might differ in terms of emotional support.")

    world.run(2)

    print("\n[SUNNY'S FOLLOW-UP]")
    sunny.pp_current_interactions()

    # INTERACTION 4: Alex provides final thoughts
    print("\n\n--- INTERACTION 4: Alex's final perspective ---")
    alex.listen("Sunny mentioned emotional support. Respond with your thoughts on "
                "balancing efficiency with empathy.")

    world.run(2)

    print("\n[ALEX'S FINAL THOUGHTS]")
    alex.pp_current_interactions()

    print("\n" + "="*70)
    print("SIMULATION COMPLETE")
    print("="*70)

    return sunny, alex


def evaluate_conversation_quality(sunny, alex):
    """
    Post-simulation evaluation of persona performance.

    EVALUATION FRAMEWORK:
    --------------------
    This function should analyze (manually or automatically):

    1. CONSISTENCY METRICS:
       - Did Sunny maintain optimistic/enthusiastic tone throughout?
       - Did Alex stay professional and solution-focused?
       - Were personality traits evident in word choice and style?

    2. AUTHENTICITY METRICS:
       - Do responses sound natural or artificial/scripted?
       - Are there realistic conversational elements (acknowledgment, questions, etc.)?
       - Do personas show understanding of context?

    3. DIVERSITY METRICS:
       - How different are Sunny's vs Alex's responses?
       - Do differences align with personality specifications?
       - Can you identify each persona by communication style alone?

    4. DEPTH METRICS:
       - Do responses show genuine reasoning or just pattern matching?
       - Are there insights that go beyond surface-level customer service advice?
       - Do personas demonstrate expertise consistent with their backgrounds?

    5. LIMITATION IDENTIFICATION:
       - Where did personas break character or become inconsistent?
       - Were there awkward phrasings or unnatural transitions?
       - Did responses become repetitive or formulaic?

    INSIGHTS GENERATED:
    ------------------
    Different persona types should generate different insights:
    - Sunny: Emotional intelligence, customer psychology, relationship building
    - Alex: Process optimization, technical problem-solving, efficiency

    Less useful outputs might include:
    - Generic advice that could come from any persona
    - Inconsistent personality expression
    - Failure to maintain role-appropriate boundaries
    """

    print("\n" + "="*70)
    print("CONVERSATION QUALITY EVALUATION")
    print("="*70)

    print("\n📊 EVALUATION CRITERIA:")
    print("\n1. NATURALNESS: Assess if the conversation flows like real human dialogue")
    print("   - Look for: Natural transitions, acknowledgments, questions")
    print("   - Red flags: Robotic responses, unnatural phrasing\n")

    print("2. PERSONALITY CONSISTENCY: Check if personas maintained their character")
    print("   - Sunny should show: Enthusiasm, positivity, empathy, warmth")
    print("   - Alex should show: Professionalism, efficiency, directness, logic")
    print("   - Red flags: Out-of-character statements, personality shifts\n")

    print("3. DEPTH OF INSIGHTS: Evaluate the quality of advice/perspectives")
    print("   - Look for: Specific strategies, nuanced understanding, expertise")
    print("   - Red flags: Generic advice, surface-level responses\n")

    print("4. DIVERSITY OF APPROACHES: Compare how different personas respond")
    print("   - Expected: Clearly distinct approaches based on personality")
    print("   - Red flags: Similar responses despite different personas\n")

    print("5. CONTEXTUAL COHERENCE: Check if responses build on previous messages")
    print("   - Look for: References to prior statements, logical progression")
    print("   - Red flags: Ignoring context, repetitive points\n")

    print("="*70)
    print("\n💡 MANUAL REVIEW INSTRUCTIONS:")
    print("Review the conversation above and assess:")
    print("- Which persona was more convincing and why?")
    print("- Were there moments where the simulation felt less realistic?")
    print("- Did personality differences lead to meaningfully different insights?")
    print("- Would these personas be useful for actual customer service training?")
    print("\n" + "="*70)


def main():
    """
    Main execution function.

    EXPECTED OUTCOMES:
    -----------------
    SUCCESSFUL SIMULATION will demonstrate:
    ✓ Clear personality differentiation between Sunny and Alex
    ✓ Consistent behavior aligned with persona specifications
    ✓ Natural conversational flow and context awareness
    ✓ Diverse insights based on different personality types
    ✓ Realistic customer service knowledge and approaches

    LESS SUCCESSFUL SIMULATION may show:
    ✗ Personality convergence (personas sound similar)
    ✗ Inconsistent character maintenance
    ✗ Artificial or stilted language
    ✗ Generic responses lacking personality-specific insights
    ✗ Context confusion or illogical responses

    USE CASES FOR EVALUATION:
    ------------------------
    - Training data generation for customer service AI
    - Testing different communication approaches
    - Understanding personality impact on customer satisfaction
    - Developing customer service best practices
    - Creating realistic chatbot personas
    """

    print("\n" + "="*70)
    print("TINYTROUPE CUSTOMER SERVICE BOT SIMULATION")
    print("="*70)
    print("\nThis simulation creates AI personas with distinct personalities")
    print("to explore how different communication styles affect customer service.\n")

    # Create the personas
    sunny, alex = create_customer_service_bots()

    print("\n✓ Personas loaded successfully!")
    print(f"  - {sunny.name}: {sunny.get('occupation')['title']}")
    print(f"  - {alex.name}: {alex.get('occupation')['title']}")

    # Run the simulation
    print("\nStarting simulation...")
    sunny, alex = simulate_customer_interaction(sunny, alex)

    # Provide evaluation framework
    evaluate_conversation_quality(sunny, alex)

    print("\n✓ Simulation and evaluation complete!")
    print("\nNote: This conversation will be documented in CONVERSATION_EXAMPLE.md")


if __name__ == "__main__":
    main()
