def load_scores(filename="scores.txt", max_scores=5):   # Загрузка рекордов из файла
    scores = []
    try:
        with open(filename, "r") as f:
            scores = [int(line.strip()) for line in f if line.strip().isdigit()]
    except FileNotFoundError:
        pass
    scores.sort(reverse=True)
    return scores[:max_scores]

def save_score(score, filename="scores.txt"):
    scores = load_scores(filename)
    scores.append(score)
    scores = sorted(scores, reverse=True)[:5]
    with open(filename, "w") as f:
        for s in scores:
            f.write(str(s) + "\n")