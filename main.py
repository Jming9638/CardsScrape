import time
import pandas as pd
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

model = AutoModelForSeq2SeqLM.from_pretrained("google/flan-t5-large")
tokenizer = AutoTokenizer.from_pretrained("google/flan-t5-large")

questions = [
    ["cashback", "what are the cashback offers?"],
    ["discounts", "list out all the discounts from the statement"],
    ["reward_point", "what are the reward point offers?"],
    ["shopping", "what are the shopping benefits?"],
    ["dining", "what are the dining/food offers?"],
    ["golf_benefits", "what are the golf benefits?"],
    ["travel_benefits", "what are the travel benefits?"]
]


def main():
    data = pd.read_csv('./results.csv')
    details = data['details'].to_list()
    
    total_run = len(details) * len(questions)
    print(f"Total run: {total_run}")
    
    start_time = time.time()
    run = 0
    for new_col, ques in questions:
        answers = []
        for detail in details:
            run += 1
            prompt = f"""{detail}\n\nAnswer this question based on the article: {ques}\nlist down the answer according to the article."""
            inputs = tokenizer(prompt, return_tensors="pt")
            outputs = model.generate(**inputs, max_new_tokens=64)
            answer = ", ".join(tokenizer.batch_decode(outputs, skip_special_tokens=True))
            answers.append(answer)
            
            print(f"Progress: {run}/{total_run}......")
            time.sleep(0.2)
            
        data[new_col] = answers
        print(f"Category: {new_col} done.")
        print()

    data.to_csv("./featured_results.csv", index=False)
    end_time = time.time()
    time_used = round((end_time - start_time) / 60, 2)
    print(f"Success, done. Time used: {time_used} min")


if __name__ == "__main__":
    main()
