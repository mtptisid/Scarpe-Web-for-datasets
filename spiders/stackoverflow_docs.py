import requests
import os

def fetch_stackoverflow_data(tag, pages=1, output_dir="datasets/stackoverflow"):
    base_url = "https://api.stackexchange.com/2.3/questions"
    params = f"?order=desc&sort=activity&tagged={tag}&site=stackoverflow"
    os.makedirs(output_dir, exist_ok=True)
    
    for page in range(1, pages + 1):
        url = f"{base_url}{params}&page={page}"
        response = requests.get(url)
        data = response.json()
        
        for item in data['items']:
            question_id = item['question_id']
            title = item['title']
            body = item.get('body', '')
            
            # Fetch answers
            answers_url = f"https://api.stackexchange.com/2.3/questions/{question_id}/answers?order=desc&sort=activity&site=stackoverflow"
            answers_response = requests.get(answers_url)
            answers_data = answers_response.json()
            answers = [answer.get('body', '') for answer in answers_data['items']]
            
            # Save to file
            filename = f"{tag}_{question_id}.txt"
            filepath = os.path.join(output_dir, filename)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(f"Title: {title}\n\nQuestion: {body}\n\nAnswers:\n")
                for i, answer in enumerate(answers, 1):
                    f.write(f"Answer {i}: {answer}\n\n")
            print(f"Saved: {filepath}")

# Example usage
fetch_stackoverflow_data('vmware', pages=2)  # Fetch VMware-related questions
fetch_stackoverflow_data('linux', pages=2)   # Fetch Linux-related questions