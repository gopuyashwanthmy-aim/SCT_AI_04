# LLM Evaluation Report

## Method
Offline lexical-overlap proxies are used for answer relevance, faithfulness, and hallucination risk. These are baselines, not semantic judge metrics.

| ID | Relevance proxy | Faithfulness proxy | Hallucination-risk proxy |
|---|---:|---:|---:|
| EVAL-01 | 0.111 | 1.000 | 0.000 |
| EVAL-02 | 0.500 | 1.000 | 0.000 |
| EVAL-03 | 0.111 | 1.000 | 0.000 |
| EVAL-04 | 0.200 | 1.000 | 0.000 |
| EVAL-05 | 0.182 | 1.000 | 0.000 |

## Limitations
Lexical overlap can miss paraphrases and cannot prove factual correctness. For stronger evaluation, add DeepEval or Ragas with a documented judge model and labeled dataset.
