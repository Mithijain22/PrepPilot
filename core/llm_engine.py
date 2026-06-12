from langchain_community.llms import HuggingFacePipeline
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from transformers import pipeline, T5ForConditionalGeneration, T5Tokenizer
import torch

def load_llm(model_name="google/flan-t5-base"):
    
    if "flan-t5" in model_name or "t5" in model_name.lower():
        # ✅ T5 is seq2seq — needs text2text-generation
        tokenizer = T5Tokenizer.from_pretrained(model_name)
        model = T5ForConditionalGeneration.from_pretrained(
            model_name,
            torch_dtype=torch.float32  # CPU safe
        )
        pipe = pipeline(
            "text2text-generation",
            model=model,
            tokenizer=tokenizer,
            max_new_tokens=256,
            temperature=0.7,
            do_sample=True
        )
    else:
        # Mistral / LLaMA
        pipe = pipeline(
            "text-generation",
            model=model_name,
            torch_dtype=torch.float16,
            device_map="auto",
            max_new_tokens=256,
            temperature=0.7,
            do_sample=True
        )
    
    llm = HuggingFacePipeline(pipeline=pipe)
    return llm

def build_chain(llm):
    memory = ConversationBufferMemory()
    chain = ConversationChain(llm=llm, memory=memory, verbose=False)
    return chain