from app.evaluation import evaluate_case

def test_grounded_answer_scores_faithfully():
    result = evaluate_case("What is a CPU?", "CPU stands for Central Processing Unit", "CPU stands for Central Processing Unit")
    assert result["faithfulness_proxy"] == 1.0
    assert result["hallucination_risk_proxy"] == 0.0
