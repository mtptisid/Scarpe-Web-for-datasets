# 🔥 Red Hat Technical Documentation Dataset

## 📌 Overview  

This dataset contains **55,741** entries of **Red Hat Enterprise Linux (RHEL) technical documentation**, covering:  
- **System administration guides**  
- **Network configurations**  
- **Virtualization setups**  
- **Enterprise software best practices**  

🎯 **Goal:** Train and fine-tune **a domain-specific LLM** that can outperform existing models in answering **Red Hat & Linux system administration queries**.

## 📊 Dataset Details  

- **Total Entries:** 55,741  
- **Size:** ~752MB (compressed)  
- **License:** CC BY-SA 4.0  
- **Task Categories:**  
  - ✅ **Text Retrieval**  
  - ✅ **Question Answering**  
  - ✅ **Text Generation**  
- **Tags:** `redhat`, `linux`, `system-administration`, `enterprise`  

## 📁 Dataset Structure  

```
| Column      | Data Type  | Description |
|------------|-----------|-------------|
| `title`    | `string`  | Title of the document/guide |
| `content`  | `string`  | Full text of the document |
| `commands` | `list`    | Relevant Linux commands extracted from the document |
| `url`      | `string`  | Original documentation link |
```

### **Example Entry**
```
{
    "title": "Configuring SELinux Policies",
    "content": "SELinux (Security-Enhanced Linux) provides...",
    "commands": ["setenforce 1", "getenforce", "sestatus"],
    "url": "https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux"
}
```

## 🚀 **Why This Dataset?**  

This dataset is ideal for:  
✅ **Fine-tuning LLMs** to provide **accurate** Linux-related answers.  
✅ **Training a Retrieval-Augmented Generation (RAG) model** for enterprise documentation search.  
✅ **Developing an AI-powered system administration assistant** to help troubleshoot and configure Red Hat systems.  

---

## 🔥 **Next-Level Performance: Custom Attention Mechanism**  

We are developing a **custom attention mechanism** specifically optimized for **Red Hat documentation**.  
### **Why?**  
Most LLMs struggle with long-form, technical content. Our new attention mechanism will:  
✔ **Focus on critical system commands**  
✔ **Prioritize relevant documentation sections**  
✔ **Improve accuracy & reduce hallucination in answers**  

**Expected Impact:** This LLM will **answer Red Hat/Linux queries better than any existing model**!  

---

## 🏗 **How to Train/Fine-Tune the Model**  

### **1️⃣ Load the Dataset in Python**  

```
from datasets import load_dataset

dataset = load_dataset("mtpti5iD/redhat-docs_dataset")
print(dataset["train"][0])
```

### **2️⃣ Fine-Tune LLaMA-2 / Mistral / Gemini**  

Using `transformers`:  

```
from transformers import AutoModelForCausalLM, AutoTokenizer, TrainingArguments, Trainer

model_name = "meta-llama/Llama-2-7b-chat-hf"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

# Tokenize dataset
def tokenize_function(examples):
    return tokenizer(examples["content"], padding="max_length", truncation=True)

tokenized_datasets = dataset.map(tokenize_function, batched=True)

# Training setup
training_args = TrainingArguments(
    output_dir="./results",
    evaluation_strategy="epoch",
    save_strategy="epoch",
    per_device_train_batch_size=2
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_datasets["train"],
    eval_dataset=tokenized_datasets["validation"]
)

trainer.train()
```

---

## 🔗 **Resources & Links**  

- **Dataset**: [Hugging Face 🤗](https://huggingface.co/datasets/mtpti5iD/redhat-docs_dataset)  
- **GitHub Repository**: [GitHub 🔗](https://github.com/mtptisid/Scarpe-Web-for-datasets/)  
- **Fine-Tuning Guide**: [Notebook Colab 📒](https://colab.research.google.com/drive/1M54O5QVMivuCf1peK1kFy-4-YHX-_i4o?usp=sharing) [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1M54O5QVMivuCf1peK1kFy-4-YHX-_i4o?usp=sharing)

---





