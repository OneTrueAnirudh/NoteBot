from datasets import load_dataset
from sentence_transformers import SentenceTransformer
from sentence_transformers.evaluation import EmbeddingSimilarityEvaluator, SimilarityFunction
import warnings

warnings.filterwarnings("ignore")  # suppresses all warnings

# Load a model
model = SentenceTransformer('all-mpnet-base-v2') # highest average score (0.8803)

# Load the STSB dataset (https://huggingface.co/datasets/sentence-transformers/stsb)
eval_dataset = load_dataset("sentence-transformers/stsb", split="validation")

# Initialize the evaluator
dev_evaluator = EmbeddingSimilarityEvaluator(
    sentences1=eval_dataset["sentence1"], # getting sentence pairs and scores from dataset
    sentences2=eval_dataset["sentence2"],
    scores=eval_dataset["score"],
    main_similarity=SimilarityFunction.COSINE,
    name="sts-dev",
)

result=dev_evaluator(model)
for key, value in result.items(): # printing individual scores
    print(f"{key}: {value}")

# calculate and print the average score
avg_score = sum(list(result.values()))/len(result)
print(f"Average Score: {avg_score:.4f}")