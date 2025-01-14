"""
This script defines a PromptTemplate class that assists in generating 
conversation/prompt templates. The script facilitates formatting prompts 
for inference and training by combining various context elements and user inputs.
"""


import dataclasses
from typing import Dict, Union


@dataclasses.dataclass
class PromptTemplate:
    """A class that manages prompt templates"""

    # The name of this template
    name: str
    # The template of the system prompt
    system_template: str = "{system_message}"
    # The template for the system context
    context_template: str = "{user_context}{news_context}"
    # The template of the user question
    question_template: str = "{question}"
    # The template of the system answer
    answer_template: str = "{answer}"
    # The system message
    system_message: str = ""
    # Separator
    sep: str = "\n"
    eos: str = ""

    @property
    def train_raw_template(self):
        """Training prompt template format"""
        system = self.system_template.format(system_message=self.system_message)
        context = f"{self.sep}{self.context_template}"
        question = f"{self.sep}{self.question_template}"
        answer = f"{self.sep}{self.answer_template}"

        return f"{system}{context}{question}{answer}{self.eos}"

    @property
    def infer_raw_template(self):
        """Inference prompt template format"""
        system = self.system_template.format(system_message=self.system_message)
        context = f"{self.sep}{self.context_template}"
        question = f"{self.sep}{self.question_template}"

        return f"{system}{context}{question}{self.eos}"

    def format_train(self, sample: Dict[str, str]) -> Dict[str, Union[str, Dict]]:
        """Formats the data sample to a training sample"""
        prompt = self.train_raw_template.format(
            user_context=sample["about_me"],
            news_context=sample["context"],
            question=sample["question"],
            answer=sample["response"],
        )
        return {"prompt": prompt, "payload": sample}

    def format_infer(self, sample: Dict[str, str]) -> Dict[str, Union[str, Dict]]:
        """Formats the data sample to a testing sample"""
        prompt = self.infer_raw_template.format(
            user_context=sample["about_me"],
            news_context=sample["context"],
            question=sample["question"],
        )
        return {"prompt": prompt, "payload": sample}


# Global Templates registry
templates: Dict[str, PromptTemplate] = {}


def register_llm_template(template: PromptTemplate):
    """Register a new template to the global templates registry"""
    templates[template.name] = template


def get_llm_template(name: str) -> PromptTemplate:
    """Returns the template assigned to the given name"""
    return templates[name]


##### Register Templates #####
# - FALCON (spec: https://huggingface.co/tiiuae/falcon-7b/blob/main/tokenizer.json)
register_llm_template(
    PromptTemplate(
        name="falcon",
        system_template=">>INTRODUCTION<< {system_message}",
        system_message="You are a helpful assistant, with financial expertise.",
        context_template=">>CONTEXT<< {user_context}{news_context}",
        question_template=">>QUESTION<< {question}",
        answer_template=">>ANSWER<< {answer}",
        sep="\n",
        eos="<|endoftext|>",
    )
)
