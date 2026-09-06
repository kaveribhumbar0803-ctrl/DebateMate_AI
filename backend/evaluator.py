def evaluate_debate(topic, argument):
    """
    Basic debate evaluator.
    Returns scores and feedback for the user's argument.
    """

    topic_words = set(topic.lower().split())
    argument_words = set(argument.lower().split())

    # Relevance
    common_words = topic_words.intersection(argument_words)
    relevance = min(100, 50 + len(common_words) * 10)

    # Clarity
    sentences = [s.strip() for s in argument.split(".") if s.strip()]
    if len(argument.split()) >= 15:
        clarity = 85
    elif len(argument.split()) >= 8:
        clarity = 70
    else:
        clarity = 50

    # Reasoning
    reasoning_words = [
        "because", "therefore", "however",
        "although", "since", "example",
        "reason", "evidence", "result"
    ]

    reasoning_count = sum(
        word in argument.lower()
        for word in reasoning_words
    )

    reasoning = min(100, 60 + reasoning_count * 10)

    # Overall score
    overall = round(
        (relevance + clarity + reasoning) / 3
    )

    # Feedback
    if overall >= 85:
        feedback = "Excellent argument! Your response is clear, relevant, and well-reasoned."
    elif overall >= 70:
        feedback = "Good argument! Add stronger reasoning and examples to make it more convincing."
    else:
        feedback = "Your argument needs improvement. Add relevant points, reasoning, and supporting examples."

    return {
        "topic": topic,
        "argument": argument,
        "scores": {
            "relevance": relevance,
            "clarity": clarity,
            "reasoning": reasoning,
            "overall": overall
        },
        "feedback": feedback
    }