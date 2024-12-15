from transformers import BertTokenizer, BertForSequenceClassification, AdamW
import torch


def predict(text):
    model = BertForSequenceClassification.from_pretrained('dbmdz/bert-base-turkish-cased', num_labels=4)
    model.load_state_dict(torch.load("../results/bert_model.pth"))
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device)
    tokenizer = BertTokenizer.from_pretrained('dbmdz/bert-base-turkish-cased')
    optimizer = AdamW(model.parameters(), lr=2e-5)
    optimizer.load_state_dict(torch.load("../results/optimizer.pth"))
    inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=128).to(device)
    with torch.no_grad():
        outputs = model(**inputs)
        logits = outputs.logits

    predicted_label = torch.argmax(logits, dim=1).item()
    return predicted_label